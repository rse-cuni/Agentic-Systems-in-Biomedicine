from __future__ import annotations

import json
import re
import time
from typing import Any

import requests

from langflow.custom import Component
from langflow.io import (
    BoolInput,
    IntInput,
    MessageTextInput,
    MultilineInput,
    Output,
    SecretStrInput,
    StrInput,
)

try:
    from langflow.schema import Data
except ImportError:
    from langflow.schema.data import Data


class ClinVarLookupComponent(Component):
    display_name = "ClinVar Lookup"
    description = "Alias-aware ClinVar search via NCBI E-utilities with exact-match scoring."
    icon = "search"
    name = "ClinVarLookup"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="Primary Query",
            info="Free-text primary query, e.g. 'BRCA1 c.68_69delAG hereditary breast ovarian cancer'",
            tool_mode=True,
            required=True,
        ),
        StrInput(
            name="gene",
            display_name="Gene",
            value="",
            info="Optional gene symbol, e.g. BRCA1",
            tool_mode=True,
        ),
        StrInput(
            name="variant",
            display_name="Variant",
            value="",
            info="Optional preferred variant string, e.g. c.68_69delAG",
            tool_mode=True,
        ),
        MultilineInput(
            name="alias_queries",
            display_name="Alias Queries",
            value="",
            info="Optional alternate searches. Use one per line, or pass a JSON list.",
            tool_mode=True,
        ),
        StrInput(
            name="condition",
            display_name="Condition",
            value="",
            info="Optional disease or phenotype context",
            tool_mode=True,
            advanced=True,
        ),
        IntInput(
            name="retmax_per_query",
            display_name="Max Results Per Query",
            value=5,
            required=True,
            advanced=True,
        ),
        IntInput(
            name="max_total_records",
            display_name="Max Total Records",
            value=15,
            required=True,
            advanced=True,
        ),
        BoolInput(
            name="include_raw",
            display_name="Include Raw Record",
            value=False,
            advanced=True,
        ),
        StrInput(
            name="email",
            display_name="NCBI Email",
            value="",
            info="Recommended by NCBI for API usage",
            advanced=False,
        ),
        SecretStrInput(
            name="api_key",
            display_name="NCBI API Key",
            value="",
            advanced=False,
        ),
    ]

    outputs = [
        Output(name="results", display_name="Results", method="lookup"),
    ]

    ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    REQUEST_DELAY_SEC = 0.34
    MAX_RETRIES = 3

    def _ncbi_params(self, extra: dict[str, Any]) -> dict[str, Any]:
        params = dict(extra)
        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    def _normalize_text(self, value: str) -> str:
        if not value:
            return ""
        value = value.lower().strip()
        value = value.replace(">", " ")
        value = re.sub(r"[^a-z0-9]+", "", value)
        return value

    def _normalize_variant_alias(self, value: str) -> list[str]:
        value = value.strip()
        if not value:
            return []

        aliases = [value]

        hgvs_del = re.match(r"^(c\.\d+(?:_\d+)?)del([ACGT]+)$", value, flags=re.IGNORECASE)
        if hgvs_del:
            aliases.append(f"{hgvs_del.group(1)}del")

        protein_fs = re.match(r"^(p\.[A-Za-z]{3}\d+[A-Za-z]{3}fs.*)$", value)
        if protein_fs:
            aliases.append(value.replace("Ter", "*"))

        deduped: list[str] = []
        for alias in aliases:
            if alias and alias not in deduped:
                deduped.append(alias)
        return deduped

    def _parse_alias_queries(self) -> list[str]:
        raw = (self.alias_queries or "").strip()
        if not raw:
            return []

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass

        aliases = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                aliases.append(line)
        return aliases

    def _request_with_retry(self, url: str, params: dict[str, Any]) -> requests.Response:
        last_error: Exception | None = None

        for attempt in range(self.MAX_RETRIES):
            if attempt == 0:
                time.sleep(self.REQUEST_DELAY_SEC)
            else:
                time.sleep(self.REQUEST_DELAY_SEC * (attempt + 1))

            try:
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    wait_time = float(retry_after) if retry_after else (attempt + 1) * 1.5
                    time.sleep(wait_time)
                    last_error = RuntimeError(
                        "NCBI rate limit reached (HTTP 429). "
                        "Add an NCBI API key or reduce request frequency."
                    )
                    continue

                response.raise_for_status()
                return response
            except requests.HTTPError as exc:
                last_error = exc
                if exc.response is None or exc.response.status_code != 429:
                    raise
            except requests.RequestException as exc:
                last_error = exc
                if attempt == self.MAX_RETRIES - 1:
                    raise

        if last_error is not None:
            raise last_error
        raise RuntimeError("ClinVar request failed without a captured error.")

    def _build_queries(self) -> list[str]:
        queries: list[str] = []

        def add(value: str) -> None:
            value = value.strip()
            if value and value not in queries:
                queries.append(value)

        add(self.query)

        gene = self.gene.strip()
        variant = self.variant.strip()
        condition = self.condition.strip()

        for alias in self._normalize_variant_alias(variant):
            if gene:
                add(f"{gene} {alias}")
            else:
                add(alias)
            if condition:
                add(f"{gene} {alias} {condition}".strip())

        for alias in self._parse_alias_queries():
            add(alias)
            if gene and gene.lower() not in alias.lower():
                add(f"{gene} {alias}")
            if condition and condition.lower() not in alias.lower():
                add(f"{alias} {condition}")

        return queries

    def _esearch_ids(self, query: str) -> list[str]:
        response = self._request_with_retry(
            self.ESEARCH_URL,
            self._ncbi_params(
                {
                    "db": "clinvar",
                    "term": query,
                    "retmode": "json",
                    "retmax": self.retmax_per_query,
                    "sort": "relevance",
                }
            ),
        )
        return response.json().get("esearchresult", {}).get("idlist", [])

    def _esummary(self, ids: list[str]) -> dict[str, Any]:
        response = self._request_with_retry(
            self.ESUMMARY_URL,
            self._ncbi_params(
                {
                    "db": "clinvar",
                    "id": ",".join(ids),
                    "retmode": "json",
                }
            ),
        )
        return response.json().get("result", {})

    def _extract_clinsig(self, raw: dict[str, Any]) -> str:
        germline = raw.get("germline_classification", {}) or {}
        clinical = raw.get("clinical_significance", {}) or {}

        for key in ("description", "clinical_significance_description"):
            if germline.get(key):
                return str(germline[key])
        for key in ("description", "clinical_significance_description"):
            if clinical.get(key):
                return str(clinical[key])

        return ""

    def _extract_review_status(self, raw: dict[str, Any]) -> str:
        germline = raw.get("germline_classification", {}) or {}
        clinical = raw.get("clinical_significance", {}) or {}

        for key in ("review_status", "reviewStatus"):
            if germline.get(key):
                return str(germline[key])
        for key in ("review_status", "reviewStatus"):
            if clinical.get(key):
                return str(clinical[key])

        if raw.get("review_status"):
            return str(raw["review_status"])
        return ""

    def _extract_conditions(self, raw: dict[str, Any]) -> list[str]:
        conditions: list[str] = []

        for trait in raw.get("trait_set", []) or []:
            if isinstance(trait, dict):
                name = trait.get("trait_name") or trait.get("name")
                if name and name not in conditions:
                    conditions.append(str(name))

        for key in ("condition", "conditions"):
            value = raw.get(key)
            if isinstance(value, str) and value.strip() and value not in conditions:
                conditions.append(value.strip())

        return conditions

    def _flatten_strings(self, value: Any, sink: list[str]) -> None:
        if isinstance(value, str):
            if value.strip():
                sink.append(value.strip())
            return
        if isinstance(value, dict):
            for nested in value.values():
                self._flatten_strings(nested, sink)
            return
        if isinstance(value, list):
            for nested in value:
                self._flatten_strings(nested, sink)

    def _candidate_strings(self, raw: dict[str, Any]) -> list[str]:
        strings: list[str] = []
        self._flatten_strings(raw, strings)
        strings.append(json.dumps(raw, ensure_ascii=True))
        return strings

    def _score_record(
        self,
        raw: dict[str, Any],
        queries: list[str],
        gene: str,
        variant: str,
        aliases: list[str],
    ) -> tuple[int, bool, list[str]]:
        strings = self._candidate_strings(raw)
        blob = " || ".join(strings)
        blob_norm = self._normalize_text(blob)

        gene_norm = self._normalize_text(gene)
        variant_norm = self._normalize_text(variant)
        alias_norms = [self._normalize_text(item) for item in aliases if item.strip()]

        score = 0
        reasons: list[str] = []

        if gene_norm and gene_norm in blob_norm:
            score += 20
            reasons.append("gene_match")

        if variant_norm and variant_norm in blob_norm:
            score += 45
            reasons.append("variant_match")

        for alias_raw, alias_norm in zip(aliases, alias_norms):
            if alias_norm and alias_norm in blob_norm:
                score += 35
                reasons.append(f"alias_match:{alias_raw}")

        title_norm = self._normalize_text(str(raw.get("title") or ""))
        if gene_norm and gene_norm in title_norm:
            score += 10
            reasons.append("title_gene_match")
        if variant_norm and variant_norm in title_norm:
            score += 30
            reasons.append("title_variant_match")

        for query in queries:
            query_norm = self._normalize_text(query)
            if query_norm and query_norm in blob_norm:
                score += 5
                reasons.append(f"query_match:{query}")

        clinsig = self._extract_clinsig(raw).lower()
        if "pathogenic" in clinsig:
            score += 5
            reasons.append("pathogenic_signal")

        exact_match = False
        if gene_norm and gene_norm in blob_norm:
            if (variant_norm and variant_norm in blob_norm) or any(
                alias_norm and alias_norm in blob_norm for alias_norm in alias_norms
            ):
                exact_match = True
                score += 25
                reasons.append("exact_match")

        return score, exact_match, reasons

    def lookup(self) -> Data:
        try:
            queries = self._build_queries()
            if not queries:
                return Data(data={"error": "No queries available for ClinVar lookup."})

            gene = self.gene.strip()
            variant = self.variant.strip()
            parsed_aliases = self._parse_alias_queries()
            auto_aliases = self._normalize_variant_alias(variant)
            all_aliases = []
            for alias in auto_aliases + parsed_aliases:
                if alias and alias not in all_aliases:
                    all_aliases.append(alias)

            diagnostics: list[dict[str, Any]] = []
            all_ids: list[str] = []

            for query in queries:
                ids = self._esearch_ids(query)
                diagnostics.append({"query": query, "ids": ids})
                for uid in ids:
                    if uid not in all_ids:
                        all_ids.append(uid)
                if len(all_ids) >= self.max_total_records:
                    break

            all_ids = all_ids[: self.max_total_records]

            if not all_ids:
                self.status = "No ClinVar candidates found."
                return Data(
                    data={
                        "query": self.query,
                        "gene": gene,
                        "variant": variant,
                        "queries_tried": queries,
                        "diagnostics": diagnostics,
                        "exact_match_found": False,
                        "count": 0,
                        "top_match": None,
                        "records": [],
                    }
                )

            payload = self._esummary(all_ids)
            records: list[dict[str, Any]] = []

            for uid in payload.get("uids", []):
                raw = payload.get(uid, {})
                score, exact_match, score_reasons = self._score_record(
                    raw=raw,
                    queries=queries,
                    gene=gene,
                    variant=variant,
                    aliases=all_aliases,
                )

                record = {
                    "uid": uid,
                    "title": raw.get("title"),
                    "accession": raw.get("accession"),
                    "object_type": raw.get("obj_type"),
                    "clinical_significance": self._extract_clinsig(raw),
                    "review_status": self._extract_review_status(raw),
                    "conditions": self._extract_conditions(raw),
                    "score": score,
                    "exact_match": exact_match,
                    "score_reasons": score_reasons,
                }

                if self.include_raw:
                    record["raw"] = raw

                records.append(record)

            records.sort(
                key=lambda record: (
                    not record["exact_match"],
                    -int(record["score"]),
                    str(record.get("title") or ""),
                )
            )

            top_match = records[0] if records else None
            exact_match_found = bool(top_match and top_match.get("exact_match"))

            result = {
                "query": self.query,
                "gene": gene,
                "variant": variant,
                "aliases_used": all_aliases,
                "queries_tried": queries,
                "diagnostics": diagnostics,
                "count": len(records),
                "exact_match_found": exact_match_found,
                "top_match": top_match,
                "records": records,
            }

            if exact_match_found:
                self.status = f"Exact ClinVar match found: {top_match.get('title', 'unknown')}"
            else:
                self.status = "ClinVar candidates found, but no confident exact match."

            return Data(data=result)

        except Exception as exc:
            self.status = "ClinVar lookup failed."
            return Data(
                data={
                    "error": str(exc),
                    "query": self.query,
                    "gene": self.gene,
                    "variant": self.variant,
                }
            )

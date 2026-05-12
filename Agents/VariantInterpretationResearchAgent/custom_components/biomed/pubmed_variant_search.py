from __future__ import annotations

import time
import xml.etree.ElementTree as ET

import requests

from langflow.custom import Component
from langflow.io import IntInput, MessageTextInput, Output, SecretStrInput, StrInput

try:
    from langflow.schema import Data
except ImportError:
    from langflow.schema.data import Data


class PubMedVariantSearchComponent(Component):
    display_name = "PubMed Variant Search"
    description = "Search PubMed and return titles, PMIDs, journals, years, and abstracts."
    icon = "book-open"
    name = "PubMedVariantSearch"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="Query",
            info="e.g. 'BRCA1 c.68_69delAG hereditary breast cancer'",
            tool_mode=True,
            required=True,
        ),
        IntInput(
            name="retmax",
            display_name="Max Results",
            value=5,
            required=True,
        ),
        StrInput(
            name="email",
            display_name="NCBI Email",
            value="",
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
        Output(name="results", display_name="Results", method="search"),
    ]

    REQUEST_DELAY_SEC = 0.34
    MAX_RETRIES = 3

    def _ncbi_params(self, extra: dict) -> dict:
        params = dict(extra)
        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    def _text(self, element) -> str:
        if element is None:
            return ""
        return " ".join("".join(element.itertext()).split())

    def _request_with_retry(self, url: str, params: dict) -> requests.Response:
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
        raise RuntimeError("PubMed request failed without a captured error.")

    def search(self) -> Data:
        try:
            esearch = self._request_with_retry(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                self._ncbi_params(
                    {
                        "db": "pubmed",
                        "term": self.query,
                        "retmode": "json",
                        "retmax": self.retmax,
                        "sort": "relevance",
                    }
                ),
            )
            ids = esearch.json().get("esearchresult", {}).get("idlist", [])

            if not ids:
                self.status = "No PubMed matches found."
                return Data(data={"query": self.query, "count": 0, "articles": []})

            efetch = self._request_with_retry(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
                self._ncbi_params(
                    {
                        "db": "pubmed",
                        "id": ",".join(ids),
                        "retmode": "xml",
                    }
                ),
            )

            root = ET.fromstring(efetch.text)
            articles = []

            for article in root.findall(".//PubmedArticle"):
                pmid = self._text(article.find(".//PMID"))
                title = self._text(article.find(".//ArticleTitle"))
                journal = self._text(article.find(".//Journal/Title"))
                year = self._text(article.find(".//PubDate/Year")) or self._text(article.find(".//ArticleDate/Year"))

                abstract_parts = []
                for node in article.findall(".//Abstract/AbstractText"):
                    label = node.attrib.get("Label", "").strip()
                    text = self._text(node)
                    abstract_parts.append(f"{label}: {text}" if label else text)

                articles.append(
                    {
                        "pmid": pmid,
                        "title": title,
                        "journal": journal,
                        "year": year,
                        "abstract": " ".join(part for part in abstract_parts if part).strip(),
                    }
                )

            self.status = f"Found {len(articles)} PubMed article(s)."
            return Data(
                data={
                    "query": self.query,
                    "count": len(articles),
                    "pmids": ids,
                    "articles": articles,
                }
            )
        except Exception as exc:
            return Data(data={"error": str(exc), "query": self.query})

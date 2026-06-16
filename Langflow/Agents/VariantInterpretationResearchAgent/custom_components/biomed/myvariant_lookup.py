from __future__ import annotations

import requests

from langflow.custom import Component
from langflow.io import IntInput, MessageTextInput, Output, StrInput

try:
    from langflow.schema import Data
except ImportError:
    from langflow.schema.data import Data


class MyVariantLookupComponent(Component):
    display_name = "MyVariant Lookup"
    description = "Query MyVariant.info for annotation enrichment."
    icon = "database"
    name = "MyVariantLookup"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="Query",
            info="rsID, HGVS, or free-text variant query",
            tool_mode=True,
            required=True,
        ),
        IntInput(
            name="size",
            display_name="Max Hits",
            value=5,
            required=True,
        ),
        StrInput(
            name="fields",
            display_name="Fields",
            value="clinvar,dbsnp,gnomad_genome,gnomad_exome,cadd",
            advanced=True,
        ),
    ]

    outputs = [
        Output(name="results", display_name="Results", method="lookup"),
    ]

    def lookup(self) -> Data:
        try:
            response = requests.get(
                "https://myvariant.info/v1/query",
                params={
                    "q": self.query,
                    "size": self.size,
                    "fields": self.fields,
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            hits = payload.get("hits", [])

            simplified = []
            for hit in hits:
                simplified.append(
                    {
                        "id": hit.get("_id"),
                        "score": hit.get("_score"),
                        "dbsnp": hit.get("dbsnp", {}),
                        "clinvar": hit.get("clinvar", {}),
                        "gnomad_exome": hit.get("gnomad_exome", {}),
                        "gnomad_genome": hit.get("gnomad_genome", {}),
                        "cadd": hit.get("cadd", {}),
                    }
                )

            self.status = f"Found {len(simplified)} MyVariant hit(s)."
            return Data(
                data={
                    "query": self.query,
                    "count": len(simplified),
                    "hits": simplified,
                }
            )
        except Exception as exc:
            return Data(data={"error": str(exc), "query": self.query})

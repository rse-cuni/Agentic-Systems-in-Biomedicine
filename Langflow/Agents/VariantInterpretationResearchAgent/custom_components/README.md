# Variant Agent Custom Components

This folder contains the Langflow custom components used by the `VariantInterpretationResearchAgent`.

## Components

| Path | Purpose |
| ---- | ------- |
| `biomed/clinvar_lookup.py` | Alias-aware ClinVar lookup for primary variant interpretation evidence |
| `biomed/pubmed_variant_search.py` | PubMed retrieval for exact-variant and disease-context papers |
| `biomed/myvariant_lookup.py` | MyVariant.info enrichment for identifiers and annotation support |

## How to load these components

Point Langflow at this folder with `LANGFLOW_COMPONENTS_PATH`.

```bash
export LANGFLOW_COMPONENTS_PATH="/absolute/path/to/Agentic-Systems-in-Biomedicine/Agents/VariantInterpretationResearchAgent/custom_components"
langflow run
```

Restart Langflow after adding or editing any of these files.

## Notes

- `ClinVar` and `PubMed` use public NCBI E-utilities.
- An NCBI API key is optional for light use and mostly helps with rate limits.
- `MyVariant.info` does not require an API key for the basic public queries used here.

## NCBI credentials

Both NCBI-backed components expose `email` and `api_key` fields directly in Langflow.

How to obtain an API key:

1. Sign in to or create a [My NCBI account](https://www.ncbi.nlm.nih.gov/account/).
2. Open [NCBI Account Settings](https://www.ncbi.nlm.nih.gov/account/settings/).
3. Scroll to `API Key Management`.
4. Click `Create API Key`.
5. Paste the generated key into both the `ClinVar Lookup` and `PubMed Variant Search` nodes.

Official references:

- [NCBI API overview](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- [NCBI API key documentation](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys/)

# IPv6 Hitlist Analysis

An exploratory data-analysis pipeline for responsive IPv6 addresses. The project samples a responsive-address dataset, measures prefix concentration and interface-identifier (IID) patterns, enriches addresses with ASN/country data, and generates simple address candidates from frequently observed `/64` prefixes.

## Questions explored

- How concentrated are responsive IPv6 addresses at `/32`, `/48`, and `/64` prefix lengths?
- Which IID construction patterns occur most often?
- Which ASNs and countries appear in the sample?
- Can common `/64` prefixes be used to produce a reproducible candidate set for further analysis?

## Pipeline

| Step | Script | Output |
| --- | --- | --- |
| Sample responsive addresses | `01_make_sample.py` | `responsive_sample_10000.txt` |
| Analyze prefixes | `02_prefix_analysis.py` | `top_prefix32.csv`, `top_prefix48.csv`, `top_prefix64.csv` |
| Enrich ASN/country metadata | `03_as_country_analysis.py` | `asn_country_result.csv` |
| Summarize IID types | `04_parse_addr6_iid.py` | `iid_type_count.csv` |
| Generate candidates | `05_generate_candidates.py` | `generated_candidates.txt` |

## Snapshot of results

The included analysis uses a 10,000-address responsive IPv6 sample. `addr6` reports that all sampled addresses are globally routable unicast addresses. The most common IID categories are IEEE-derived (61.55%), randomized (20.38%), and low-byte (16.75%).

The supplied CSV outputs and figures in `picture/` make the results reproducible and easy to inspect.

## Run locally

### Requirements

- Python 3.9+
- `pandas`

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The raw input (`responsive-addresses.txt.xz`) is intentionally excluded from version control because it exceeds GitHub's file-size limit. The repository includes the derived 10,000-address sample, so steps 2–5 can run immediately. Place an authorized raw responsive-address dataset in the project root to re-run step 1.

Run the analysis scripts from this repository's root directory in numeric order:

```bash
python 01_make_sample.py
python 02_prefix_analysis.py
python 03_as_country_analysis.py
python 04_parse_addr6_iid.py
python 05_generate_candidates.py
```

`03_as_country_analysis.py` queries Team Cymru's public whois service and therefore requires network access. The remaining steps run against the local files.

## Data and responsible use

This is a course data-analysis project. The candidate-generation step is included solely to study address-structure patterns; it does not perform network probing or scanning. Use only datasets and network activity for which you have permission.

## Repository contents

- `responsive_sample_10000.txt` — reproducible 10,000-address sample
- `responsive_sample_10000.txt` — reproducible 10,000-address sample
- `addr6_decode.txt` and `addr6_stats.txt` — IID decoding inputs and summary
- `*.csv` — generated analysis tables
- `picture/` — figures used in the report

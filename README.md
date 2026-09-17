# Christian Wellbeing: Faith and Health Data Story

An evidence-first portfolio project about self-reported health and religious
affiliation among U.S. adults in the 2022 General Social Survey.

> **Core principle:** these results describe associations. They do not show
> that religious faith causes better or worse health.

## The question

How do general, physical, and mental self-reported health differ among adults
who identify as Christian, with another faith, or with no religious affiliation?

## Results

| Metric | Christian | Other faith | No religious affiliation |
|---|---:|---:|---:|
| Excellent or good general health | 72.45% | 75.85% | 70.96% |
| 8+ physically unhealthy days | 8.48% | 8.83% | 11.10% |
| 8+ mentally unhealthy days | 14.65% | 22.52% | 25.42% |

The Other faith group is comparatively small, so its confidence intervals are
wider. The mental-health differences are descriptive and may reflect age,
income, education, community support, access to care, or other confounders.

## Power BI report

The public report link will be added after the aggregate-only semantic model is
verified and published. Report design and field configuration are documented in
[`powerbi/visual_spec.md`](powerbi/visual_spec.md).

## Reproduce the analysis

```powershell
python scripts/download_data.py
python scripts/analyze.py
python -m unittest discover -s tests -v
```

The download is pinned by SHA-256. Raw respondent data is stored under
`data/raw/` and excluded from Git. The Power BI model uses only the nine-row
aggregate file in `data/processed/chart_data.csv`.

## Repository guide

- `scripts/`: verified download and survey-weighted analysis pipeline
- `tests/`: mapping, schema, range, release-count, and result regression tests
- `data/processed/`: aggregate Power BI input and data-quality receipt
- `docs/`: methodology and public data dictionary
- `powerbi/`: theme, DAX, Power Query, and visual specification
- `linkedin/`: final English LinkedIn draft

## Method summary

Estimates use `WTSSNRPS`. Confidence intervals use Taylor linearization with
`VSTRAT` and `VPSU`. Metric-specific reserved and missing responses are
excluded. See [`docs/methodology.md`](docs/methodology.md) for definitions,
group mappings, design details, and limitations.

## Data source and license

Source: [General Social Survey 2022](https://gss.norc.org/get-the-data.html),
NORC at the University of Chicago. Source data is not redistributed by this
repository. Users should consult the GSS documentation and terms before use.

Project code is released under the [MIT License](LICENSE).


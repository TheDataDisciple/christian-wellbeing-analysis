# Christian Wellbeing: Faith and Health Data Story

An evidence-first portfolio project about self-reported health and religious
affiliation among U.S. adults in the 2022 General Social Survey.

![Mental health by religious affiliation, Power BI Desktop editorial report](powerbi/exports/christian_wellbeing_editorial_2022-1.png)

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

The [current two-page report in Power BI Service](https://app.powerbi.com/groups/me/reports/f0efb5fe-96db-4b41-9f95-d3682b32e860/MentalHealthEditorial?experience=power-bi)
is the interactive counterpart of the editable project below. The link points
to a workspace report and may require appropriate Power BI sign-in and access;
this repository does not grant access. Report design and field configuration
are documented in [`powerbi/visual_spec.md`](powerbi/visual_spec.md).

The editable portfolio source is a text-based Power BI Project at
[`powerbi/project/ChristianWellbeing2022/ChristianWellbeing2022.pbip`](powerbi/project/ChristianWellbeing2022/ChristianWellbeing2022.pbip).
It contains two 1600 × 1080 pages:

1. **01 | Mental Health** — the landing page, focused on adults reporting eight
   or more mentally unhealthy days in the past month.
2. **02 | Health Context** — aligned comparisons of excellent or good general
   health and eight or more physically unhealthy days.

The three native bar charts use direct values and restrained styling. The
survey-design-adjusted 95% confidence intervals and valid respondent counts
are available in interactive tooltips; static images do not show those
intervals. The PBIP embeds only the nine reviewed aggregate rows and is
checked against `data/processed/chart_data.csv`. The reviewed Desktop
[two-page PDF](powerbi/exports/christian_wellbeing_editorial_2022.pdf) and
[Mental Health](powerbi/exports/christian_wellbeing_editorial_2022-1.png) /
[Health Context](powerbi/exports/christian_wellbeing_editorial_2022-2.png)
page images show the current editorial version. The image above is rendered
from the PDF exported by Power BI Desktop, not generated from Python chart code.

### Previous reference version

The [earlier public report](https://app.powerbi.com/view?r=eyJrIjoiYzczNGI3ZTctYjY1NS00MmRiLWFhMDYtOTA3MjBjMDhhMTQ2IiwidCI6ImEwNzg4YjhlLWYwNDktNGY1YS04OGEyLTY3NTliZWY2OWM3NiIsImMiOjl9)
has not been replaced. Its Python-rendered [PNG](powerbi/exports/christian_wellbeing_report.png)
and [PDF](powerbi/exports/christian_wellbeing_report.pdf) show the earlier
four-chart composition with visible confidence intervals. They are retained
for comparison, not as the primary design.

## Technologies and workflow

| Tool | How it was used |
|---|---|
| NORC General Social Survey 2022 | Source of the respondent-level survey data; raw records are not committed. |
| Python, pandas, and NumPy | Reproducible data preparation, survey-weighted estimates, and design-adjusted confidence intervals. |
| Pillow | Rendering the earlier static PNG and PDF reference figure from reviewed aggregates. |
| Power BI Desktop | Building and reviewing the interactive report and its aggregate-only semantic model. |
| Power Query (M), DAX, and PBIP/PBIR/TMDL | Embedding the nine aggregate rows, defining measures, and keeping the report and model as reviewable text-based project files. |
| Power BI Service | Hosting the interactive report; it is not used to calculate the survey estimates. |
| Python `unittest` | Regression checks for source mappings, calculations, model values, and report configuration. |
| Git and GitHub | Version control and pull-request review of the code, data outputs, and Power BI project. |
| OpenAI Codex | AI-assisted implementation, testing, and documentation under human review; it is not a runtime dependency or the source of the statistical results. |
| Notion | A project log for decisions, progress, and release checks; it is not a data source or a runtime dependency. |

## Reproduce the analysis

```powershell
python scripts/download_data.py
python scripts/analyze.py
python scripts/render_chart.py
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
- `powerbi/`: editable PBIP source, theme, visual specification, and verified exports
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

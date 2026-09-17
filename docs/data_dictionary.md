# Public Dataset Dictionary

The public file `data/processed/chart_data.csv` contains aggregate estimates
only. It contains no respondent-level records.

| Column | Type | Definition |
|---|---|---|
| `belief_group` | text | Christian, Other faith, or No religious affiliation |
| `metric_id` | text | Stable machine-readable metric identifier |
| `metric_label` | text | Reader-facing metric description |
| `estimate` | decimal | Survey-weighted percentage on a 0–100 scale |
| `ci_low` | decimal | Lower bound of the design-adjusted 95% confidence interval |
| `ci_high` | decimal | Upper bound of the design-adjusted 95% confidence interval |
| `unit` | text | `% of adults` |
| `unweighted_n` | integer | Valid respondent count for the group and metric |
| `source_year` | integer | GSS survey year, 2022 |
| `sort_order` | integer | Stable display order for affiliation groups |


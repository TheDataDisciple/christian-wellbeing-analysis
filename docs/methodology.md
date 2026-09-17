# Methodology

## Research question

How does self-reported health differ across Christian adults, adults affiliated
with another faith, and adults reporting no religious affiliation in the 2022
General Social Survey (GSS)?

This is a descriptive comparison. It does not estimate the causal effect of
religious belief on health.

## Source and analytical population

The source is the official 2022 GSS cross-section published by NORC at the
University of Chicago. The downloaded Stata archive is verified against the
SHA-256 checksum recorded in `data/source_manifest.json`.

The release contains 4,149 rows. The selected nonresponse-adjusted
post-stratification weight (`WTSSNRPS`) is present for 3,544 core respondents.
The remaining 605 oversample records are excluded rather than analyzed without
the selected weight. After excluding missing or unmapped religious affiliation,
the common grouped population contains 3,483 respondents.

## Religious-affiliation grouping

- **Christian:** Protestant, Catholic, Orthodox Christian, generic Christian,
  and inter/non-denominational Christian.
- **Other faith:** Jewish, Muslim/Islam, Buddhist, Hindu, other Eastern
  religion, Native American religion, and other religion.
- **No religious affiliation:** the GSS “None” response.

“No religious affiliation” is not equivalent to atheist; some unaffiliated
respondents may hold spiritual or theistic beliefs.

## Measures

- **Excellent or good general health:** `HEALTH` equals Excellent or Good.
- **8+ physically unhealthy days:** `PHYSHLTH` is between 8 and 30.
- **8+ mentally unhealthy days:** `MNTLHLTH` is between 8 and 30.

Reserved codes and missing values are excluded independently for each measure,
so sample sizes differ across visuals.

## Estimation and uncertainty

Point estimates use `WTSSNRPS`. Ninety-five percent confidence intervals use a
Taylor-linearized ratio estimator with `VSTRAT` as the variance stratum and
`VPSU` as the variance primary sampling unit. Linearized values are summed at
the PSU level, and between-PSU variance is accumulated within strata. The
interval uses a 1.96 normal critical value and is clipped to the 0–100% range.

## Limitations

- Cross-sectional associations cannot establish causality.
- Age, income, education, region, race/ethnicity, marital status, disability,
  and other factors may confound observed differences.
- Health is self-reported and may vary with interpretation and survey mode.
- Religious affiliation does not measure belief intensity, practice, community
  participation, or personal theology.
- The Other faith group is small and heterogeneous, producing wider intervals.
- Physical and mental health questions were answered by subsets of respondents.


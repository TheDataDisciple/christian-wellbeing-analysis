# 2022 editorial report

The report has two pages. Page 01, **Mental Health**, is the user-designed reference. Page 02, **Health Context**, follows its editorial style while retaining two distinct measures: excellent or good general health and 8+ physically unhealthy days in the past month.

The second page uses Georgia headings, navy bars, direct percentage labels, quiet respondent notes, and no visible numeric axes, gridlines, or error bars. Survey-weighted 95% confidence interval bounds remain in each chart's tooltips. These are descriptive associations, not evidence that religious affiliation causes a health outcome.

The 2022 estimates and source data were not changed by this design pass. The
PBIP structure, three chart bindings, and visual bounds were checked locally;
all 10 Python regression tests pass. On 2026-09-22, both pages rendered in the
open Power BI Desktop project. A fresh two-page PDF was exported from Desktop,
rendered to page PNGs, and inspected for clipping and readability. The mental
health page image is now the README's lead image. The earlier Desktop exports
are obsolete and should not be used for this release.

The current two-page Power BI Service report is at
https://app.powerbi.com/groups/me/reports/f0efb5fe-96db-4b41-9f95-d3682b32e860/MentalHealthEditorial?experience=power-bi.
The Service report was reviewed read-only on 2026-09-22. Both page names,
headings, three displayed series, values, and respondent notes match the
Desktop export. One pending publication difference remains: the Service
version's Mental Health alt text says the chart is shown "with 95% confidence
intervals," while the local PBIP now clarifies that the intervals are in
tooltips. The earlier public report remains unchanged.

The offline release-candidate tool reports No-Go because its metric catalog
found zero measures. That is a parser limitation, not evidence of an empty
model: the same tool's model inventory lists the DAX measures, and the Python
suite verifies the three visual bindings and aggregate data. Its live-model
connector also did not detect a listening local endpoint, although Desktop
rendered and exported both pages. Treat those automated findings as heuristic
and retain this evidence when reviewing the PR. No republishing or merge is
authorized by this review.

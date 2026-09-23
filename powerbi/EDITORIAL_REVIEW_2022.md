# GSS 2022 editorial report release review

## Current report

The report has two pages. **01 | Mental Health** is the opening page and focuses
on frequent mentally unhealthy days. **02 | Health Context** contains aligned
general-health and physical-health comparisons. The report uses Georgia
headings, navy bars, direct percentage labels, quiet respondent notes, and no
visible numeric axes, gridlines, or error bars. Survey-weighted 95% confidence
interval bounds remain available in the chart tooltips.

The report is descriptive. It does not establish that religious affiliation
causes a health outcome. The estimates, survey-weighting method, group mapping,
and nine-row aggregate Power BI model are unchanged.

## Desktop and phone layouts

The desktop report retains its two 1600 × 1080 pages and three native charts.
Portrait phone layouts are stored as PBIR `mobile.json` files beside the visual
definitions. Mental Health places its chart before the respondent note. Health
Context places its title and subtitle before the general-health chart and note,
then the physical-health chart and note. Every phone visual is full-width and
the two charts on Health Context are stacked vertically.

## Public report

The canonical anonymous Power BI report is:

https://app.powerbi.com/view?r=eyJrIjoiMWNmYzlkY2UtOGZjOS00ZTFiLWJmY2UtOTIxYTkwMDM5MGFiIiwidCI6ImEwNzg4YjhlLWYwNDktNGY1YS04OGEyLTY3NTliZWY2OWM3NiIsImMiOjl9&pageName=MentalHealthEditorial

Before the mobile update, the link was verified without authentication: it
opened on **01 | Mental Health**, reported page 1 of 2, and displayed the
reviewed values and respondent note. After publication, the same checks must be
repeated at desktop and phone viewport sizes.

## Technology and assisted workflow

The statistical pipeline uses NORC GSS 2022, Python, pandas, NumPy, and
`unittest`. Pillow supports static analytical exports. Power BI Desktop,
Power Query M, DAX, PBIP, PBIR, and TMDL provide the editable report and
aggregate-only semantic model; Power BI Service provides public interaction.
Git, GitHub, and GitHub CLI provide review and release history. Notion stores
the decision and QA log.

OpenAI Codex assisted under human review. The Power BI Desktop and Computer Use
plugins support local authoring, the Power BI browser plugin supports public
verification, Data Analytics skills support visual and analytical QA, the PDF
skill supports rendered export inspection, and Notion Knowledge Capture stores
the release record. None of these plugins is a runtime dependency or source of
the estimates.

## Automated release evidence

The Power BI release-candidate review reports a **Strong 100/100** PBIP
structure score, **Low** insight-scan risk with zero findings, and **24/24**
passing golden baselines. Its model inventory finds the mobile definitions and
the DAX measures. The heuristic metric catalog still reports zero measures; this
is a parser limitation because the same review inventory and repository tests
confirm the measures in TMDL. The automated release status remains **No-Go**
until the required Power BI Desktop render, phone-preview inspection, and
post-publication checks are completed.

Power BI Desktop subsequently round-tripped the PBIP without changing a report
value, visual binding, or mobile position. Its local file differences are
newline normalization only. This is local evidence that Desktop accepts the
project structure, but it is not evidence that the phone canvases are visually
readable. The full suite now contains **13 passing tests**, including explicit
checks for 6–8 unit mobile spacing, 323-unit full-width placement, text sizes of
at least 9 pt, the exact public iframe, technology and plugin disclosure,
licensing language, and canonical-only public links.

## Release gate

The release is ready only when:

- all Python tests pass, including mobile layout and canonical-link checks;
- Power BI Desktop loads both layouts without repair or schema warnings;
- fresh desktop and phone previews have been inspected;
- the exported PDF has been rendered and both pages inspected;
- the public report shows both pages without authentication after publication;
- the final diff contains no respondent-level data, credentials, absolute user
  paths, PBIX/PBIT files, or private GSS 2024 material.

let
    Source = Csv.Document(
        File.Contents("data/processed/chart_data.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"belief_group", type text},
            {"metric_id", type text},
            {"metric_label", type text},
            {"estimate", type number},
            {"ci_low", type number},
            {"ci_high", type number},
            {"unit", type text},
            {"unweighted_n", Int64.Type},
            {"source_year", Int64.Type},
            {"sort_order", Int64.Type}
        }
    )
in
    Typed


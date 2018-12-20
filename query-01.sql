-- results table
SELECT
    "slug",
    "title",
    "views",
    "name"
FROM (
    -- second table as join of articles and article_count
    SELECT
        "article_count"."slug",
        "articles"."title",
        "articles"."author",
        "article_count"."views"
    FROM "articles"
    JOIN (
        -- first table
        SELECT
            SPLIT_PART("path",'/',3) AS "slug",
            COUNT(*) AS "views"
        FROM "log"
        JOIN "articles"
        ON "articles"."slug" = SPLIT_PART("log"."path",'/',3)
        GROUP BY "log"."path"
    ) AS "article_count"
    ON "articles"."slug" = "article_count"."slug"
) AS "author_article_count"
JOIN "authors"
ON "authors"."id" = "author_article_count"."author"
ORDER BY "views" DESC;
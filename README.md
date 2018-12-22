# News Log Analysis - Python DB API

Python script and SQL queries to connect and query a `news` database to provide the following output:

* Most popular three articles of all time
* Most popular article authors of all time
* Day(s) on which more than 1% of HTTP requests lead to errors

The following are demonstrated in this project:
* Python DB API
* Connecting to PostgreSQL
* SQL queries, sub-querries, table joins, views
* SQL string functions and arithmetic operation

## Dependencies
The Python script is developed using version 3.6.5. The database server used is [PostgreSQL](https://www.postgresql.org/) version 10.6; the server must already be present.

The Python script uses `psycopg2` adapter to connect and execute SQL queries to the database server. This can be installed as follows:

```bash
$> pip install psycopg2
```

Prior to the running the Python script, the `news` database must be prepared. This database can be downloaded from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). This will provide a `newsdata.zip` file that will need to be extracted. A `newsdata.sql` file will be obtained. Prepare the database by running the followin in the command prompt.

```bash
$> psql -d news -f newsdata.sql
```

## Running the Python script
Run the scipt as follows:

```bash
$> python logs-analysis.py
```

## SQL View
In order to perform analysis the following view is created

```sql
CREATE OR REPLACE VIEW "article_author_views" AS
SELECT
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
```
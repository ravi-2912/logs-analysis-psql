#!python3
import psycopg2 as psql
import datetime

# connect to news database
# modify string to include user and password
conn = psql.connect("dbname=news user=postgres password=postgres")

# create a cursor
curr = conn.cursor()

# execute a query to create a combined table with articles, 
# total views and their authors
curr.execute('''CREATE OR REPLACE VIEW "article_author_views" AS
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
                ORDER BY "views" DESC;''')

# execute query to get top viewed articles
curr.execute('''SELECT * FROM "article_author_views"
                ORDER BY "views" DESC;''')

# print top three articles
top_articles = curr.fetchmany(3)
for article in top_articles:
    print("{}\t - {} views".format(article[0], article[1]))
print()

# execute query to get most viewed authors
curr.execute('''SELECT
                    "name",
                    SUM("views")
                FROM "article_author_views"
                GROUP BY "name"
                ORDER BY SUM("views") DESC;''')

#print authors and their views
top_authors = curr.fetchall()
for author in top_authors:
    print("{}\t - {} views".format(author[0], author[1]))
print()

# execute query to get HTTP errors more than 1% on a day
curr.execute('''SELECT
                    "table200"."date",
                    (100.00*"numERR"/("numERR"+"numOK"))
                    AS "percent_fail"
                FROM (
                    SELECT
                        DATE("time"),
                        COUNT(*) AS "numOK"
                    FROM "log"
                    WHERE "log"."status"='200 OK'
                    GROUP BY DATE("time")
                ) AS "table200"
                JOIN (
                    SELECT
                        DATE("time"),
                        COUNT(*) AS "numERR"
                    FROM "log"
                    WHERE "log"."status"<>'200 OK'
                    GROUP BY DATE("time")
                ) AS "table404"
                ON "table200"."date"="table404"."date"
                WHERE (100.00*"numERR"/("numERR"+"numOK"))>1.0;''')

# print HTTP erros and dates
top_errors = curr.fetchall()
for error in top_errors:
    date = error[0].strftime("%b %d, %Y")
    print("{}\t - {:.2f}% error".format(date, error[1]))
print()

# close cursor and connection
curr.close()
conn.close()

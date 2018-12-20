SELECT
    "table200"."date",
    "numERR",
    "numOK",
    (100.00*"numERR"/("numERR"+"numOK")) AS "percent_fail"
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
WHERE (100.00*"numERR"/("numERR"+"numOK"))>1.0;
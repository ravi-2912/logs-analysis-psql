# News Log Analysis - Python DB API

Python script and SQL queries to connect and query a `news` database to provide the following output:

* Most popular three articles of all time
* Most popular article authors of all time
* Day(s) on which more than 1% of HTTP requests lead to errors

## Dependencies
The Python script is developed using version 3.6.5. The database server used is [PostgreSQL](https://www.postgresql.org/) version 10.6; the server must already be present.

The Python script uses `psycopg2` adapter to connect and execute SL queries to the database server.

Prior to the Python script the `news` database must be prepared. This database can be downloaded from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). This will provide a `newsdata.zip` file that will need to be extracted. A `newsdata.sql` file will be obtained. Prepare the database by running the followin in the command prompt.

```bash
$> psql -d news -f newsdata.sql
```

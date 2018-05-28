# !/usr/bin/env python3

# psycopg2 is psql adapter for python

import psycopg2

# connection to our database

dbconnect = psycopg2.connect(database="news")
# famous_articles gives top 3 articles from db news


def famous_articles():
    print('  What are the most popular three articles of all time?\n')
    dbcur = dbconnect.cursor()
    top_articles_query = """SELECT articles.title, count(log.path) as\
                    views FROM articles, log WHERE\
                    log.path=('/article/' || articles.slug)\
                    GROUP BY articles.title ORDER BY views desc limit 3"""
    dbcur.execute(top_articles_query)
    articles = dbcur.fetchall()
    for top in articles:
        print ('''       "%s" __ %s views''' % (top[0], top[1]))

# famous_authors gives top 3 famous articles from db news


def famous_authors():
    print('\n  Who are the most popular article authors of all time?\n')
    dbcur = dbconnect.cursor()
    popular_authors_query = """SELECT authors.name, count(log.path) as views FROM\
                 articles, log, authors\
                 WHERE log.path=('/article/'||articles.slug)\
                 AND articles.author = authors.id \
                 GROUP BY authors.name ORDER BY views desc"""
    dbcur.execute(popular_authors_query)
    authors = dbcur.fetchall()
    for top in authors:
        print("	%s __ %s views" % (top[0], top[1]))

# percentage_of_error gives on which days error is moe than 1%


def percentage_of_error():
    print('\n  On which days did more than 1% of requests lead to errors?\n')
    dbcur = dbconnect.cursor()
    error_calculation_query = """ SELECT total.day,
          ROUND(((errors.error_requests*1.0) / total.requests), 3) AS percent
        FROM (
          SELECT date_trunc('day', time) "day", count(*) AS error_requests
          FROM log
          WHERE status LIKE '404%'
          GROUP BY day
        ) AS errors
        JOIN (
          SELECT date_trunc('day', time) "day", count(*) AS requests
          FROM log
          GROUP BY day
          ) AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.error_requests*1.0) / total.requests), 3) > 0.01)
        ORDER BY percent DESC; """
    dbcur.execute(error_calculation_query)
    datawitherror = dbcur.fetchall()
    for z in datawitherror:
        date = z[0].strftime('	%B %d, %Y')
        errors = str(round(z[1]*100, 1)) + "%" + "  errors"
        print(date + '__ '+errors)
# connection is closed
    dbconnect.close()

if __name__ == '__main__':
    famous_articles()
    famous_authors()
    percentage_of_error()

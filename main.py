import sentry_sdk, psycopg2
from flask import Flask, render_template, flash
from sentry_sdk import capture_exception


sentry_sdk.init(
    dsn="https://1f76b334106769b9d015a5d173862544@us.sentry.io/4506699319214080",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
# division_by_zero = 1 / 0

app=Flask(__name__)
app.secret_key='secretkey'

try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
except Exception as e:
    capture_exception(e)
    # print("I am unable to connect to the database")


@app.route("/products")
def prods():
    try:
        cur = conn.cursor
        cur.execute("Select * from products")
        prods = cur.fetchall()
        flash("products fetched successfuly.")
        return render_template("products.html",prods=prods)
    except Exception as e:
        capture_exception(e)
        flash("Server error.Try again later.")
        return render_template("products.html", prods=prods)
    
app.run()
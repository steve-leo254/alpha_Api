import sentry_sdk
import psycopg2
from flask import Flask, render_template, flash, g
from sentry_sdk import capture_exception

sentry_sdk.init(
    dsn="https://1f76b334106769b9d015a5d173862544@us.sentry.io/4506699319214080",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
app.secret_key = 'secretkey'

def get_db():
    if 'db' not in g:
        try:
            g.db = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
        except Exception as e:
            capture_exception(e)
            flash("Error connecting to the database.")
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route("/products")
def prods():
    prods = []

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        prods = cur.fetchall()
        flash("Products fetched successfully.")
    except Exception as e:
        capture_exception(e)
        flash("Server error. Try again later.")

    return render_template("products.html", prods=prods)

if __name__ == '__main__':
    app.run(debug=True)

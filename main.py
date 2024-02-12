import sentry_sdk
from flask import Flask, Request
from sentry_sdk import capture_exception
from flask_sqlalchemy import SQLAlchemy
from dds import Product


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leo.steve@localhost/alpha-product'
db = SQLAlchemy

@app.route("/products", methods["POST","GET"])
def prods():
    if request.method == "GET":
    try:
        prods = product.queryall()
        print(prods)
        return "success"
    
    
    except Exception as e:
        capture_exception(e)
        return "error"
    else:
        if Request.s_json:
            data = Request.json
            print
    
app.run()
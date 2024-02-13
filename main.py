import sentry_sdk
from flask import request
from sentry_sdk import capture_exception
from dds import Product,app,db


sentry_sdk.init(
    dsn="https://1f76b334106769b9d015a5d173862544@us.sentry.io/4506699319214080",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# @app.before_first_request
# def create_table():


@app.route("/products", methods=["POST","GET"])
def prods():
    if request.method == "GET":
        try:
            prods = Product.queryall()
            print(prods)
            return "success"
    
        except Exception as e:
        #  capture_exception(e)
         return "error"
    else:
        if request.is_json:
            data = request.json
            print(data)
            return "stored"
        else:
            return "data is not json"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
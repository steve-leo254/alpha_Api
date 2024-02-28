from flask import jsonify
import sentry_sdk
from flask import flash, jsonify, request
from sentry_sdk import capture_exception
from flask_sqlalchemy import SQLAlchemy
from dds import Product, app, db, Sale
from flask_cors import CORS
import requests
from sqlalchemy import func
from datetime import datetime, date


sentry_sdk.init(
    dsn="https://1f76b334106769b9d015a5d173862544@us.sentry.io/4506699319214080",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
)

# @app.before_first_request
# def create_tables():
#     db.create_all()


# store & store products
CORS(app)


@app.route("/products", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def prods():
    if request.method == "GET":
        try:
            prods = Product.query.all()
            p_dict = []
            for prod in prods:
                p_dict.append(
                    {"id": prod.id, "name": prod.name, "price": prod.price})
            return jsonify(p_dict)
        except Exception as e:
            print(e)
            # capture_exception(e)
            return jsonify({})

    elif request.method == "POST":
        if request.is_json:
            try:
                data = request.json
                new_product = Product(name=data.get(
                    'name'), price=data.get('price'))
                db.session.add(new_product)
                db.session.commit()
                r = "Product added successfully." + str(new_product.id)
                res = {"result": r}
                return jsonify(res), 201
            except Exception as e:
                print(e)
                # capture_exception(e)
                return jsonify({"error": "Internal Server Error"}), 500
        else:
            return jsonify({"error": "Data is not JSON."}), 400
    else:
        return jsonify({"error": "Method not allowed."}), 400

# Task by Thursday
# Get a single product in the route


@app.route('/get-product<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        prd = Product.query.get(product_id)
        if prd:
            return jsonify({
                "id": prd.id,
                "name": prd.name,
                "price": prd.price
            })
        else:
            return jsonify({"error": "Product not found."}), 404
    except Exception as e:
        print(e)
        # capture_exception(e)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/sale', methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        try:
            sale = Sale.query.all()
            s_dict = []
            for sale in sale:
                s_dict.append({"id": sale.id, "pid": sale.pid,
                              "quantity": sale.quantity, "created_at": sale.created_at})
            return jsonify(s_dict)
        except Exception as e:
            print(e)
            # capture_exception(e)
            return jsonify({})

    elif request.method == 'POST':
        if request.is_json:
            try:
                data = request.json
                new_sale = Sale(pid=data.get(
                    'pid'), quantity=data.get('quantity'))
                db.session.add(new_sale)
                db.session.commit()
                s = "sale added successfully." + str(new_sale.id)
                sel = {"result": s}
                return jsonify(sel), 201
            except Exception as e:
                print(e)
                # capture_exception(e)
                return jsonify({"error": "Internal Server Error"}), 500
        else:
            return jsonify({"error": "Data is not JSON."}), 400
    else:
        return jsonify({"error": "Method not allowed."}), 400


# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if request.method == 'GET':
#         try:
#             # Fetch and return currency exchange rate data
#             apikey = "G10JJR1J6E7WZRZQ."
#             url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=KES&apikey="+apikey
#             r = requests.get(url)
#             exchange_rate_data = r.json()
#             return jsonify(exchange_rate_data)
#         except Exception as e:
#             print(e)
#             return jsonify({"error": "Error fetching currency exchange rate"}), 500

#     elif request.method == 'POST':
#         if request.is_json:
#             try:
#                 data = request.json
#                 from_currency = data.get('from_currency')
#                 to_currency = data.get('to_currency') 
#                 response_data = {
#                     "message": "Data received successfully",
#                     "from_currency": from_currency,
#                     "to_currency": to_currency
#                 }
#                 return jsonify(response_data), 201
#             except Exception as e:
#                 print(e)
#                 return jsonify({"error": "Internal Server Error"}), 500
#         else:
#             return jsonify({"error": "Data is not JSON."}), 400
#     else:
#         return jsonify({"error": "Method not allowed."}), 400

@app.route('/dashboard', methods=["GET"])
def dashboard():
   # Query to get sales per day
    sale_per_day = db.session.query(
        # extracts date from created at
        func.date(Sale.created_at).label('date'),
        # calculate the total number of sales per day
        func.sum(Sale.quantity * Product.price).label('total_sale')
    ).join(Product).group_by(
        func.date(Sale.created_at)
    ).all()

    #  to JSON format
    sale_data = [{'date': str(day), 'total_sale': sale}
                  for day, sale in sale_per_day]
    #  sales per product
    sale_per_product = db.session.query(
        Product.name,
        func.sum(Sale.quantity*Product.price).label('sale_product')
    ).join(Sale).group_by(
        Product.name
    ).all()

    # to JSON format
    saleproduct_data = [{'name': name, 'sale_product': sale_product}
                         for name, sale_product in sale_per_product]

    return jsonify({'sale_data': sale_data, 'saleproduct_data': saleproduct_data})





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# Get a single product in the route =done
# Create a new project call it alpha-app,make it boostrapand datatables enabled with dummy data(products) in a table = done
# Have a form in a bootstrap modal with products input = done
# Push your latest code. Create a new repo on github for alpha-app = done

#  Thursday tas
# display your currency in your web app
# comsume  other public API

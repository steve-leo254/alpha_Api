from flask import jsonify
import sentry_sdk
from flask import flash, jsonify, request
from sentry_sdk import capture_exception
from flask_sqlalchemy import SQLAlchemy
from  dds import Product, app, db,Sales
from flask_cors import CORS


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


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        try:
            sales = Sales.query.all()
            s_dict = []
            for sale in sales:
                s_dict.append({
                    "id": sale.id,
                    "pid": sale.pid,  # Corrected the attribute name
                    "quantity": sale.quantity,  # Corrected the attribute name
                    "created_at": sale.created_at
                })
            return jsonify(s_dict)
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500

    elif request.method == "POST":
        if request.is_json:
            try:
                data = request.json
                new_sale = Sales(pid=data.get('pid'), quantity=data.get('quantity'))  # Corrected attribute names
                db.session.add(new_sale)
                db.session.commit()
                result_message = "Sale added successfully. Sale ID: " + str(new_sale.id)
                result = {"result": result_message}
                return jsonify(result), 201
            except Exception as e:
                print(e)
                return jsonify({"error": "Internal Server Error"}), 500
        else:
            return jsonify({"error": "Data is not JSON."}), 400
    else:
        return jsonify({"error": "Method not allowed."}), 400



# Task by Thursday
# Get a single product in the route
# Create a new project call it alpha-app,make it boostrapand datatables enabled with dummy data(products) in a table
# Have a form in a bootstrap modal with products input
# Push your latest code. Create a new repo on github for alpha-app




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



from flask import jsonify
import sentry_sdk
from flask import flash, jsonify, request
from sentry_sdk import capture_exception
from flask_sqlalchemy import SQLAlchemy
from dds import Product, User,app, db, Sale
from flask_cors import CORS
import requests
from sqlalchemy import func
from datetime import datetime, date
import jwt 
from functools import wraps
import datetime
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import decode_token

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
CORS(app,origins=["http://127.0.0.1:5500"], supports_credentials=True)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
            
             # Query the database to get the user based on the user ID
            current_user = User.query.filter_by(username=current_user).first()

            if not current_user:
                return jsonify({'message': 'User not found!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)


    return decorated




@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']

        # Check if the username does not exist
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            r = f"Successfully stored user with id: {str(new_user.id)}"
            res = {"result": r}
            return jsonify(res), 201
        else:
            return jsonify({'error': f'Username {username} already exists'}), 400
    except IntegrityError as e:
        db.session.rollback() 
        return jsonify({'error': 'IntegrityError - Unique constraint violated'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    # Assuming the password is stored as a string
    user = User.query.filter_by(username=username).first()

    if user:

        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() 
                            + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "User does not exist"}), 403

@app.route("/products", methods=["POST", "GET"])
@token_required
def prods(current_user):

    print("--------------", current_user)

    if request.method == "GET":
        try:
            prods = Product.query.all()
            p_dict = []
            for prod in prods:
                p_dict.append({"id": prod.id, "name": prod.name, "cost": prod.cost, "price": prod.price, 'username': prod.username})
            return jsonify(p_dict)
        except Exception as e:
            print(e)
            # capture_exception(e)
            return jsonify({})

    elif request.method == "POST":
        if request.is_json:
            try:
                data = request.json

                # Extract user_id from the current_user object
                user_id = current_user.id

                new_product = Product(
                    name=data['name'], cost=data['cost'], price=data['price'], user_id=user_id)
                db.session.add(new_product)
                db.session.commit()
                r = "Product added successfully. ID: " + str(new_product.id)
                res = {"result": r}
                return jsonify(res), 201
            except Exception as e:
                print(e)
                # capture_exception(e)
                return jsonify({"error": "Internal Server Error"}), 500
        else:
            return jsonify({"error": "Data is not JSON."}), 400




@app.route('/get-product<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        prd = Product.query.get(product_id)
        if prd:
            return jsonify({
                "id": prd.id,
                "name": prd.name,
                "cost": prd.cost,
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



@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        # Query to get sales per day
        sale_per_day = db.session.query(
            func.date(Sale.created_at).label('date'),  # extracts date from created at
            func.sum(Sale.quantity * Product.price).label('total_sale')  # calculate the total number of sales per day
        ).join(Product).group_by(
            func.date(Sale.created_at)
        ).all()

        # Convert the result to JSON format
        sale_data = [{'date': str(day), 'total_sale': total_sale}
                     for day, total_sale in sale_per_day]

        # Query to get sales per product
        sale_per_product = db.session.query(
            Product.name,
            func.sum(Sale.quantity * Product.price).label('sale_product')
        ).join(Sale).group_by(
            Product.name
        ).all()

        # Convert the result to JSON format
        saleproduct_data = [{'name': name, 'sale_product': sale_product}
                             for name, sale_product in sale_per_product]

        return jsonify({'sale_data': sale_data, 'saleproduct_data': saleproduct_data})

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500




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
# Task by Thursday
# Get a single product in the route

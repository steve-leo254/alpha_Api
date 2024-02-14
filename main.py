import sentry_sdk
from flask import request,jsonify
from sentry_sdk import capture_exception
from dds import Product,app,db


sentry_sdk.init(
    dsn="https://1f76b334106769b9d015a5d173862544@us.sentry.io/4506699319214080",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# @app.before_first_request
# def create_table():

#Get all product and store
@app.route("/products", methods=["POST","GET","PUT","PATCH","DELETE"])
def prods():
    if request.method == "GET":
        try:
            prods = Product.queryall()
            res = []
            for i in prods:
                res = ({"id": i.id,"name": i.name,"price": i.price})
            return jsonify(res),200
    
        except Exception as e:
        #  capture_exception(e)
            return jsonify({"Error":"Server error storing product."}),500
    elif request.method ==  "POST":
        if request.is_json:
            try:
                data = request.json
                print(type(data))
                new_data = Product(name=data['name'], price= data['price'])
                db.session.add(new_data)
                db.session.commit()
                r = f'Successfully stored product id" : {str(new_data.id)}'
                res = {"Result" : r}
                return jsonify(res),201
            except Exception as e:
                print(e)
                return jsonify({"Error":"Server error storing product."}),500
        else:
            return jsonify({"Error":"Method is not json"}),400
        


#Task by Thursday
#Get a single product in the route
#Create a new project call it alpha-app,make it boostrapand datatables enabled with dummy data(products) in a table
#Have a form in a bootstrap modal with products input
#Push your latest code. Create a new repo on github for alpha-app
        


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
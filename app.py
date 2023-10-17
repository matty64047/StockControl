from flask import Flask, request, jsonify
from StockControlOOP import *
import json
from flask_login import LoginManager, login_user, login_required, logout_user
import mongoengine as db

app = Flask(__name__)
app.secret_key = 'some key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connection = db.connect(host="mongodb://localhost:27017/users")
stock_controller = StockController()

app.secret_key = 'some key'

#==============================Authentication===========================#

class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@app.route('/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '') 
    user = User.objects(name=username,
                        password=password).first()
    print(User.objects())
    if user:
        login_user(user)
        return jsonify(user.to_json())
    else:
        return "Username or Password Error", 401
        
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return "Logout Success", 200

        
@app.route('/register', methods=['POST'])
def register():
    info = json.loads(request.data)
    username = info.get('username', '')
    password = info.get('password', '')
    email = info.get('email', '')

    # Check if the username already exists
    existing_user = User.objects(name=username).first()
    if existing_user:
        return "Username already exists", 400

    # Create a new user
    new_user = User(name=username, password=password, email=email)
    new_user.save()

    # Log in the newly created user (optional)
    login_user(new_user)

    return jsonify(new_user.to_json())

@app.route('/delete_user', methods=['DELETE'])
@login_required
def delete_user():
    user_id = request.args.get('user_id')
    # You can also use the username as a query parameter if you prefer.

    # Retrieve the user to be deleted
    user_to_delete = User.objects(id=user_id).first()

    if user_to_delete:
        # Delete the user from the database
        user_to_delete.delete()
        logout_user()  # Optional: Log the user out after deletion
        return "User deleted successfully", 200
    else:
        return "User not found", 404
    
#==============================Stock Control Methods===========================#

@app.route('/items', methods=['GET'])
def get_items():
    item = request.args.get('item')
    if item:
        return jsonify(stock_controller.search_stock("item"))
    else:
        items = stock_controller.get_stock()
        json_data = json.dumps([{"name": item.name, "quantity": item.quantity} for item in items])
        return json_data
     
@app.route('/items', methods=['PUT'])
@login_required
def add_item():
    name = request.args.get('name')
    quantity = int(request.args.get('quantity'))
    item_type = int(request.args.get('item_type'))
    item_types = [Perishables, Liquid, NonPerishables, Frozen]
    item = item_types[item_type](quantity, name)
    stock_controller.add_stock(item)
    return jsonify("Successfully Added")
    

@app.route('/items', methods=['DELETE'])
@login_required
def delete_item():
    name = request.args.get('name')
    quantity = int(request.args.get('quantity'))
    item_type = int(request.args.get('item_type'))
    item_types = [Perishables, Liquid, NonPerishables, Frozen]
    item = item_types[item_type](quantity, name)
    stock_controller.remove_stock(item)
    return jsonify("Successfully removed")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
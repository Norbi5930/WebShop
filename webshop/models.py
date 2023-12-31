from webshop import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    obj = db.relationship("Object", backref="username", lazy=True)


    def __repr__(self):
        return f"User({self.username}, {self.email})"



class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    uname = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def __repr__(self):
        return f"Object({self.title}, {self.name.username})"
    


    

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    uname = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    buying_id = db.Column(db.Integer, nullable=False)
    buying_name = db.Column(db.String, nullable=False)
    buying_email = db.Column(db.String, nullable=False)
    buying_locate = db.Column(db.String, nullable=False)
    buying_mobil = db.Column(db.Integer, nullable=False)
    seller_name = db.Column(db.String, nullable=False)



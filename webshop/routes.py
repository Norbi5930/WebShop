from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, login_required, logout_user

from webshop import app, db, bcrypt
from webshop.forms import NewObject, NewUser, LoginForm, NewOrder
from webshop.models import Object, User, Cart
from random import randint



with app.app_context():
    db.create_all()
    db.session.commit()



@app.route("/")
@app.route("/home")
def home():
    return render_template("welcome.html", title="Kezdőlap")


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Elérhetőségek")


@app.route("/shop")
def shop():
    shop_db = db.session.execute(db.select(Object)).scalars()
    return render_template("shop.html", title="Shop" ,objects=shop_db)

@app.route("/shop/new", methods=["GET", "POST"])
def newobject():
    form = NewObject()
    if form.validate_on_submit():
        current_object = Object(title=form.title.data, description=form.description.data, uname=current_user.username, price=form.price.data, user_id=current_user.id)
        db.session.add(current_object)
        db.session.commit()
        flash("A kívánt cikk sikeresen közétéve!", "succes")
        return redirect(url_for("shop"))
    return render_template("create.html", title="Létrehozás",form=form, cimke="Új tárgy Közzététel")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = NewUser()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Sikeres regisztráció!", "succes")
        return redirect(url_for("home"))
    return render_template("register.html", title="Regisztráció", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Sikeres bejelentkezés!", "succes")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Bejelentkezés sikertelen. Ellenőrizd a megadott felhasználónevet és jelszót", "danger")
    
    return render_template("login.html", title="Bejelentkezés", form=form)



@app.route("/shop/<int:shop_id>")
@login_required
def obj(shop_id):
    current_obj = Object.query.get_or_404(shop_id)
    return render_template("treatment.html", title="Kezelő felület",object=current_obj)



@app.route("/shop/<int:shop_id>/delete", methods=["GET", "POST"])
@login_required
def delete(shop_id):
    current_obj = Object.query.get_or_404(shop_id)
    if current_obj.uname != current_user.username:
        abort(403)
    db.session.delete(current_obj)
    db.session.commit()
    flash("A cikk sikeresen törölve lett!", "succes")
    return redirect(url_for("home"))



@app.route("/shop/<int:shop_id>/update", methods=["GET", "POST"])
@login_required
def update(shop_id):
    current_obj = Object.query.get_or_404(shop_id)
    if current_obj.uname != current_user.username:
        abort(403)
    form = NewObject()
    if form.validate_on_submit():
        current_obj.title = form.title.data
        current_obj.description = form.description.data
        current_obj.price = form.price.data
        db.session.commit()
        flash("Az adatokat frissítettük!", "succes")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.title.data = current_obj.title
        form.description.data = current_obj.description
        form.price.data = current_obj.price
    return render_template("create.html", title="Szerkesztés", form=form, cimke="A kurzus frissítése")



@app.route("/shop/<int:shop_id>/add_cart", methods=["GET", "POST"])
@login_required
def add_cart(shop_id):
    current_obj = Object.query.get_or_404(shop_id)
    form = NewOrder()

    if current_obj.uname == current_user.username:
        flash("Nem teheted a saját árucikkedet a kosaradba!", "danger")
        return redirect(url_for("shop"))
    
    if form.validate_on_submit():
        cart_obj = Cart(title=current_obj.title, description=current_obj.description, uname=current_obj.uname, price=current_obj.price,
                         buying_id=current_user.id, buying_name=current_user.username, buying_email=current_user.email, buying_locate=form.locate.data, buying_mobil=form.mobil_number.data, seller_name=current_obj.uname)
        db.session.add(cart_obj)
        db.session.commit()
        print(current_obj.id)
        flash("Az árucikket sikeresen a kosarába helyeztük!", "succes")
        return redirect(url_for("shop"))

    return render_template("neworder.html", title="Rendelés leadása", form=form)

    

@app.route("/shop/<int:cart_id>/remove_cart", methods=["GET", "POST"])
@login_required
def remove_cart(cart_id):
    current_cart = Cart.query.get_or_404(cart_id)
    
    if current_cart.buying_name != current_user.username:
        abort(403)
    db.session.delete(current_cart)
    db.session.commit()
    flash("Az árucikk sikeresen eltávolítva a kosarából!", "succes")
    return redirect(url_for("my_cart"))


@app.route("/my_cart", methods=["GET", "POST"])
@login_required
def my_cart():
    cart_db = db.session.query(Cart).filter(Cart.buying_name == current_user.username).all()
    return render_template("cart.html", title="Kosaram", objects=cart_db)


@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    orders_db = db.session.query(Cart).filter(Cart.seller_name == current_user.username).all()

    return render_template("orders.html", title="Megrendelések", objects=orders_db)



@app.route("/account", methods=["GET"])
@login_required
def account():
    return render_template("account.html", title="Profil")



@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

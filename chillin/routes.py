from chillin import app
from flask import render_template, redirect, url_for, flash, request
from chillin.models import User, Event
from chillin.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, CreateEventForm
from chillin import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
@login_required
def home_page():
    return render_template("home.html")

@app.route("/host_event", methods=["GET", "POST"])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        event_to_create = Event(title=form.title.data,
                                description=form.description.data,
                                location=form.location.data,
                                time=form.time.data,
                                group_size=form.group_size.data,
                                mode=form.mode.data,
                                joined=0,
                                host=current_user.user_id)
        db.session.add(event_to_create)
        db.session.commit()
        return redirect(url_for("home_page"))
    return render_template("create_event.html", form=form)


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                db.session.commit()
                flash(f"Congratulations! You've purchased {p_item_object.name} for {p_item_object.prettier_price}.",
                      category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}.",
                      category="danger")

        # Sold Item
        sold_item = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                db.session.commit()
                flash(f"Congratulations! You've sold {s_item_object.name} for {s_item_object.prettier_price}",
                      category="success")
            else:
                flash(f"Something went wrong with selling {p_item_object.name}.",
                      category="danger")
        return redirect(url_for("market_page"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, owned_items=owned_items, purchase_form=purchase_form,
                               selling_form=selling_form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.name}", category="success")

        return redirect(url_for("home_page"))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f"{err_msg[0]}", category="danger")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as {attempted_user.name}", category="success")
            return redirect(url_for("home_page"))
        else:
            flash("Username and password are not matched, please try again", category="danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))

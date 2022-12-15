from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.order import Order


@app.route("/cookies")
def all_orders():

    orders = Order.all_orders()

    return render_template("all_orders.html", orders=orders)

@app.route("/cookies/new")
def log_order_page():
    
    return render_template("new_order.html")

@app.route("/create-order", methods=['POST'])
def create_order():

    if not Order.validate_order(request.form):
        return redirect("/cookies/new")

    data = {
        "name": request.form['name'],
        "cookie_type": request.form['cookie_type'],
        "boxes": request.form['boxes']
    }

    Order.save(data)
    return redirect("/cookies")


@app.route("/cookies/edit-order/<int:order_id>")
def edit_order(order_id):
    data = {
        "id": order_id
    }

    order = Order.one_order(data)

    return render_template("edit_order.html",order=order)


@app.route("/update", methods=['POST'])
def update():
    if not Order.validate_order(request.form):
        return redirect(f"/cookies/edit-order/{request.form['id']}")

    data = {
        "name": request.form['name'],
        "cookie_type": request.form['cookie_type'],
        "boxes": request.form['boxes'],
        "id": request.form['id']
    }

    Order.update(data)

    return redirect("/cookies")

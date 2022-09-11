from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.order import Order

@app.route('/')
def index():
    return redirect('/cookies')

@app.route('/cookies')
def users():
    return render_template("all_orders.html",orders=Order.get_all())

@app.route('/order/new')
def new():
    return render_template("new_order.html")

@app.route('/order/create',methods=['POST'])
def create():
    if Order.validate_order(request.form):
        Order.save(request.form)
        return redirect('/cookies')
    else: return redirect('/order/new')

@app.route('/order/edit/<int:id>')
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit_order.html", order=Order.get_one(data))

@app.route('/order/update',methods=['POST'])
def update():
    if Order.validate_order(request.form):
        Order.update(request.form)
        return redirect('/cookies')
    else: return redirect('/cookies/edit/<id>')
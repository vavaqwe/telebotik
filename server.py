import flask
from flask import Flask, render_template, request, redirect, url_for, session
import config
from database import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = config.SECRET

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        result = get_password(username)
        if result is None:
            error = True
        else:
            password_db, login_db = result

        if username == login_db and password_db == password:
            session['username'] = username
            session.permanent = False
            return redirect(url_for('index'))
        else:
            error = True  

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
@login_required
def index():
    user_id = session['username']
    orders = get_user_orders(user_id)
    return render_template('index.html', orders=orders)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        type_ = request.form.get('type')
        place = request.form.get('place')
        number_phone = request.form.get('number_phone')
        user_id = session['username']

        add_new_order(
            date=date,
            time=time,
            type_photo=type_,
            phone=number_phone,
            city=place,
            user_id=user_id
        )

        return redirect(url_for('index'))

    return render_template('order.html')

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return "Order not found", 404

    date_obj = datetime.strptime(order[1], "%d.%m.%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        type_ = request.form.get('type')
        place = request.form.get('place')
        phone = request.form.get('number_phone')
        user_id = session['username']
        
        update_order(order_id, date, time, type_, phone, place, user_id)
        return redirect(url_for('index'))

    return render_template('edit_order.html', order=order, formatted_date=formatted_date)

@app.route('/delete_order/<int:order_id>')
@login_required
def delete_order(order_id):
    delete_order_by_id(order_id)
    return redirect(url_for('index'))

def run_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False, debug=True)

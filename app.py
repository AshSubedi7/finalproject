from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productsdb.db'
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
@app.route('/delete/<int:id>')
def delete(id):
    product_to_delete = Products.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/addproducts/')
    except:
        return "There was a problem deleting the product!!"

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    product_to_update = Products.query.get_or_404(id)
    if request.method == 'POST':
        product_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/addproducts/')
        except:
            return "There was a problem updating product."

    else:
        return render_template('update.htm', product_to_update=product_to_update)

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/about')
def about():
    return render_template('about.htm')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == "POST":
        if request.form['password'] != 'Panther$':
            error = 'Invalid Credentials. Please try again!'
        else:
            return redirect(url_for('invenhome'))
    return render_template('login.htm', error=error)

@app.route('/invenhome')
def invenhome():
    return render_template('invenhome.htm')

@app.route('/productslist/')
def productslist():
    return render_template('productslist.htm')

@app.route('/addproducts/', methods=['POST', 'GET'])
def addproducts():
    if request.method == "POST":
        product_name = request.form['name']
        new_product = Products(name=product_name)
        
        
        try:
            db.session.add(new_product) 
            db.session.commit()
            return redirect('/addproducts/')
        except:
            return "There was an error adding the product to the database!!"

    else:
        products = Products.query.order_by(Products.date_created)
        return render_template('addproducts.htm', products = products)

       
    
if __name__ == "__main__":
    app.run(debug=True)
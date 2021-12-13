from flask import Flask, request, jsonify, render_template, g, session, url_for,redirect
import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename

#Import from other module
import user
import database
import rpaSystem
import peekingDuckAPI

app = Flask(__name__)
app.secret_key = 'PEEKINGDUCKISTHEBEST12345'

##Login
conn = database.create_connection()
with conn:
    users = []
    cur = conn.cursor()
    sql = "SELECT * from user"
    cur.execute(sql)
    fetch=cur.fetchall()
    for row in fetch:
         users.append(user.User(id=row[0], username=row[1], password=row[2]))


###########Log In system for rating from users#######
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


#To check if admin and password is correct 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        return redirect(url_for('login'))

    return render_template('login.html')


#Logout 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


#DashBoard Page
@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))
    data = []
    conn = database.create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()
    cur.execute("SELECT * FROM equipments")
    rows2 = cur.fetchall()
    profit=0
    for row in rows:
        profit += row[4]*row[2]
    loss=0
    for row in rows2:       
        loss += row[2]*row[3]
    data =[
        ("Total Sales ",profit),
        ("Equipment Spent",loss)
    ]

    product = [row[1] for row in rows]
    product_solds = [row[4] for row in rows]
    product_sales = [row[4]*row[2] for row in rows]
    product_inventory = [row[3] for row in rows]
    labels = [row[0] for row in data]
    value = [row[1] for row in data]

    return render_template('dashboard.html', 
    product = product , product_solds = product_solds 
    ,product_inventory=product_inventory,product_sales=product_sales,labels=labels,value=value,
    )

#Peeking Duck System
@app.route('/imagePurchase')
def imagePurchase():
        if not g.user:
             return redirect(url_for('login'))

        return render_template('imagePurchase.html')

#Image for purchase
@app.route('/purchase' , methods=['GET','POST'])
def purchase():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
           f = request.files['img']
           full_name = "save.jpg"
           f.save("C:/Hackathon_2021_AI/" + full_name)
           product = peekingDuckAPI.api(full_name)
           conn = database.create_connection()
           cur = conn.cursor()
           cur.execute("SELECT * FROM product")
           rows = cur.fetchall()
           total = 0 
           for i in product:           
               for a in rows:
                   if(a[1].lower() == i):
                       total+=a[2]
           msg=""
           product_list = product.tolist()
           for a in rows:
               count = product_list.count(a[1].lower())
               if(count > 0):
                   product = a[1]
                   msg += product + " : " + str(count) + "\n"
               
           return render_template('purchase.html',total = "$"+ str(total),msg = msg)

    return redirect(url_for('imagePurchase'))

#Purchase
@app.route('/confirm_purchase',methods=['GET','POST'])
def confirm_purchase():
    if not g.user:
        return redirect(url_for('login'))

    if request.method =='POST':
             conn = database.create_connection()
             cur = conn.cursor()
             cur.execute("SELECT * FROM product")
             rows = cur.fetchall()
             full_name = "save.jpg"
             product = peekingDuckAPI.api(full_name)
             product_list = product.tolist()
             for a in rows:
                 count = product_list.count(a[1].lower())
                 if(count > 0):
                     product = a[1]
                     product_sold = a[4] + count
                     product_inventory = a[3] - count
                     sql = '''UPDATE product SET product_sold = ? , inventory_available = ? WHERE product_name = ? '''
                     cur.execute(sql,(product_sold,product_inventory,product))
                     conn.commit()
            #Print Receipt
             product = request.form.get("product")
             price = request.form.get("price")
             rpaSystem.printReciept(product,price)

             return redirect(url_for('dashboard'))
 
    return redirect(url_for('imagePurchase'))

#Equipment page
@app.route('/equipment')
def equipment():
    if not g.user:
        return redirect(url_for('login'))
    
    conn = database.create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM equipments")
    equipment = cur.fetchall()
    total = 0
    for r in equipment:
        spent = r[2] * r[3]
        total += spent



    return render_template('equipment.html',equipment=equipment,total=total)

#Add Equipment page
@app.route('/addequipment')
def addequipment():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('addequipment.html')

#Add Equipment by excel
@app.route('/addequipmentbyexcel')
def addequipmentbyexcel():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('addequipmentbyexcel.html')

#Add Equipment Function
@app.route('/addequipmentfunction',methods=['GET','POST'])
def addequipmentfunction():
    if not g.user:
        return redirect(url_for('login'))
    
    if request.method =='POST':
         name = request.form.get("name")
         price = request.form.get("price")
         qty = request.form.get("qty")

         sql = ''' INSERT INTO equipments(equipment_name,price,quantity)
              VALUES(?,?,?) '''

         conn = database.create_connection()
         cur = conn.cursor()
         cur.execute(sql, (name,price,qty))
         conn.commit()

         return redirect(url_for('equipment'))
        
    return redirect(url_for('addequipment'))


#Add Equipment Function By Excel
@app.route('/addequipmentbyexcelfunction',methods=['GET','POST'])
def addequipmentbyexcelfunction():
     if not g.user:
        return redirect(url_for('login'))
    
     if request.method =='POST':
         f = request.files['excel']
         full_name = "save.xlsx"
         f.save("C:/Hackathon_2021_AI/" + full_name)
         rpaSystem.addEquipmentExcel(full_name)

         return redirect(url_for('equipment'))

     return redirect(url_for('addequipmentbyexcel'))
     
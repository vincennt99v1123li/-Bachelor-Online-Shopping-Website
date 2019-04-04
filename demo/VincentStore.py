from flask import Flask, render_template, request, url_for, redirect, session
from flask_mail import Mail, Message
app = Flask(__name__)
app.secret_key = 'any random string'
import pymysql
import datetime



mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'VincentStoreOnline@gmail.com'
app.config['MAIL_PASSWORD'] = 'mumgor-kaxjah-xygZi9'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

user_id=''
user_details='xxx'


@app.route('/',methods = ['POST', 'GET'])
def main():
   return render_template("assisment_main.html")

@app.route('/aboutus',methods = ['POST', 'GET'])
def aboutus():
   return render_template("assisment_aboutus.html")

@app.route('/login_page',methods = ['POST', 'GET'])
def login_page():
   if "Userid" in session:
      return redirect(url_for("profile_page"))
   else:
      return render_template("assisment_log_in.html")

@app.route('/shopping_cart',methods = ['POST', 'GET'])
def shopping_cart():
   pd_price=0
   pd_total_price=0
   
   if "Userid" in session:
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_cart.quantity, Shopping_cart.total_price, Shopping_cart.shopping_cart_id from Product INNER JOIN Shopping_cart ON Product.product_id=Shopping_cart.product_id WHERE Shopping_cart.customer_id = """+str(session["Userid"])+""" ORDER BY product_id """)
         pd_list=(cursor.fetchall())
         cursor.execute( """SELECT total_price FROM Shopping_cart WHERE customer_id = """+str(session["Userid"]))
         pd_list_price_qt=(cursor.fetchall())
      db.close()
      for row in pd_list_price_qt:
         pd_price+=float(row[0])

      return render_template("assisment_shopping_cart.html",pd_list =pd_list,sum=("%.2f" %pd_price))
   else:
      return render_template("assisment_log_in.html")

@app.route('/receipt',methods = ['POST', 'GET'])
def receipt():
   
   if "Userid" in session:
      pd_price=0
      pd_total_price=0
      pd_id_1=[]
      pd_qt_1=[]
      pd_total_price_1=[]
      pd_cart_id_1=[]
      pd_list=[]
      pd_list_price_qt=[]
      cus_email_db=[]
      cus_email=[]
      cus_pt=0
      cus_pt_db=[]
      cus_pt_earn=0

      delivery_dt=[]


      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()

      db_delivery = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db_delivery.cursor() as cursor:
         cursor.execute( """SELECT delivery_schdule  FROM Delivery """)
         delivery_list=(cursor.fetchall())
      db_delivery.close()

      for row in delivery_list:
         delivery_dt.append(row[0])
         


      date_delivery =  datetime.datetime.now().date() + datetime.timedelta(days = (delivery_dt[0]- 1))
      
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT product_id,quantity,total_price, shopping_cart_id FROM Shopping_cart WHERE customer_id = """+str(session["Userid"]))
         pd_list_1=(cursor.fetchall())
      db.close()

      for row in pd_list_1:
         pd_id_1.append(row[0])
         pd_qt_1.append(row[1])
         pd_total_price_1.append(row[2])
         pd_cart_id_1.append(row[3])

      
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")

      cursor = db2.cursor() 

      i=0
      while i < len(pd_id_1):

         sql2 = """INSERT INTO Shopping_record (customer_id, product_id, shopping_record_id, quantity, total_price, date_purchase, time_purchase, delivery_date) VALUES(%d,%d,NULL,%d,%f,'%s','%s','%s') """\
         %(int(session["Userid"]),int(pd_id_1[i]),int(pd_qt_1[i]),float(pd_total_price_1[i]),date_p,time_p,date_delivery)
         try:
            cursor.execute(sql2)
            db2.commit()
         except:

            db2.rollback() 
         i+=1

      db2.close()
      
      
      db3 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db3.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_cart.quantity, Shopping_cart.total_price from Product INNER JOIN Shopping_cart ON Product.product_id=Shopping_cart.product_id WHERE Shopping_cart.customer_id = """+str(session["Userid"])+""" ORDER BY product_id """)
         pd_list=(cursor.fetchall())
         cursor.execute( """SELECT total_price FROM Shopping_cart WHERE customer_id = """+str(session["Userid"]))
         pd_list_price_qt=(cursor.fetchall())
      db3.close()
      for row in pd_list_price_qt:
         pd_price+=float(row[0])

      db4 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")


      cursor = db4.cursor() 
      i=0
      while i < len(pd_cart_id_1):
         sql3="""DELETE FROM Shopping_cart WHERE shopping_cart_id = %d"""%(int(pd_cart_id_1[i]))
         try:
            cursor.execute(sql3)
            db4.commit()
           
         except:

            db4.rollback() 
         i+=1

      db4.close()

      db_points = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db_points.cursor() as cursor:
         cursor.execute( """SELECT collecting_points FROM customer WHERE customer_id = """+str(session["Userid"]))
         cus_pt_db=(cursor.fetchall())
      db_points.close()
      for row in cus_pt_db:
         cus_pt+=(int(row[0]))


      cus_pt_earn= round(pd_price/10)
      cus_pt += cus_pt_earn

      db5 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db5.cursor() as cursor:
         cursor.execute( """SELECT email FROM customer WHERE customer_id = """+str(session["Userid"]))
         cus_email_db=(cursor.fetchall())
      db5.close()
      for row in cus_email_db:
         cus_email.append(str(row[0]))

      db6 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db6.cursor() 
      sql="""UPDATE customer SET collecting_points = %d WHERE customer_id = '%s'"""%(int(cus_pt), str(session["Userid"]))
      try:
         cursor.execute(sql)
         db6.commit()
           
      except:

         db6.rollback() 
        
      db6.close()


      msg = Message('Receipt', sender = 'VincentStoreOnline@gmail.com', recipients = [cus_email[0]])
      msg.html = render_template("assisment_mail.html",pd_list =pd_list,sum=("%.2f" %pd_price),date=date_p, time=time_p ,delivery2=date_delivery, cusid=session["Userid"], earn=cus_pt_earn,cuspt=cus_pt)
   
      mail.send(msg)
     

      

      return render_template("assisment_receipt.html",pd_list =pd_list,sum=("%.2f" %pd_price),date=date_p, time=time_p,delivery2=date_delivery, cusid=session["Userid"], earn=cus_pt_earn,cuspt=cus_pt)
   else:
      return render_template("assisment_log_in.html")

@app.route('/register_page',methods = ['POST', 'GET'])
def register_page():
   if "Userid" in session:
      return redirect(url_for("profile_page"))
   else:
      return render_template("assisment_registor.html")

@app.route('/profile_page',methods = ['POST', 'GET'])
def profile_page():
   if "Userid" in session:
      userid = session["Userid"]
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT * from customer Where customer_id = '"""+userid+"""'""")
         personal_detail=(cursor.fetchall())
      db.close()
      try:
         db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         with db2.cursor() as cursor:
            cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE Shopping_record.customer_id = """+str(session["Userid"])+""" ORDER BY date_purchase DESC, time_purchase DESC """)
            pd_list=(cursor.fetchall())
           
         db2.close()
         

         return render_template("assisment_profile.html",personal_detail = personal_detail,pd_list =pd_list)
      except:
         return render_template("assisment_profile.html",personal_detail = personal_detail,pd_list =pd_list)
   else:
      return redirect(url_for("login_page"))


@app.route('/search_drink_price',methods = ['POST', 'GET'])
def search_drink_price():
   Max_price=(request.form["Max_price"])
   Min_price=(request.form["Min_price"])
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      
      cursor.execute( """SELECT * from Product Where( product_price BETWEEN %f and %f ) AND (product_type = 'Drink') order by product_price"""%(float(Min_price),float(Max_price)))
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list,  Drink_filter = ("$"+Min_price+" - $" +Max_price))
   db.close()

@app.route('/search_food_price',methods = ['POST', 'GET'])
def search_food_price():
   Max_price=(request.form["Max_price"])
   Min_price=(request.form["Min_price"])
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      
      cursor.execute( """SELECT * from Product Where( product_price BETWEEN %f and %f ) AND (product_type = 'Food') order by product_price"""%(float(Min_price),float(Max_price)))
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list,  food_filter = ("$"+Min_price+" - $" +Max_price))
   db.close()

@app.route('/search_drink',methods = ['POST', 'GET'])
def search_drink():
   search=request.form["search_drink"]
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where(( product_name = '"""+search+ """') OR (product_brand = '"""+search+"""')) AND (product_type = 'Drink')""")
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list,  Drink_filter = search)
   db.close()

@app.route('/search_food',methods = ['POST', 'GET'])
def search_food():
   search=request.form["search_food"]
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where(( product_name = '"""+search+ """') OR (product_brand = '"""+search+"""')) AND (product_type = 'Food')""")
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list,  food_filter = search)
   db.close()


@app.route('/food',methods = ['POST', 'GET'])
def food():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list,  food_filter = "All")
   db.close()

@app.route('/drink',methods = ['POST', 'GET'])
def drink():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list,  Drink_filter = "All")
   db.close()

@app.route('/drink_error',methods = ['POST', 'GET'])
def drink_error():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list,  Drink_filter = "All",error="not enough stock")
   db.close()

@app.route('/tea',methods = ['POST', 'GET'])
def tea():
  
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Tea' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list = drink_list, Drink_filter = "Tea")
   db.close()

@app.route('/carbonated',methods = ['POST', 'GET'])
def carbonated():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'carbonated_drink' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Carbonated drink")
   db.close()

@app.route('/juice',methods = ['POST', 'GET'])
def juice():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'juice' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Juice")
   db.close()

@app.route('/milk',methods = ['POST', 'GET'])
def milk():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'milk' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
      
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Milk")
   db.close()

@app.route('/beer',methods = ['POST', 'GET'])
def beer():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'beer' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Beer")
   db.close()

@app.route('/coffee',methods = ['POST', 'GET'])
def coffee():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'coffee' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Coffee")
   db.close()


@app.route('/water',methods = ['POST', 'GET'])
def water():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'water' and product_type = 'Drink' """)
      drink_list=(cursor.fetchall())
     
      return render_template("assisment_drink.html",drink_list =drink_list, Drink_filter = "Water")
   db.close()


@app.route('/bread',methods = ['POST', 'GET'])
def bread():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Bread' and product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list, food_filter = "Bread")
   db.close()

@app.route('/cup_noodle',methods = ['POST', 'GET'])
def cup_noodle():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Cup_noodle' and product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list, food_filter = "Cup noodle")
   db.close()

@app.route('/frozen',methods = ['POST', 'GET'])
def frozen():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Frozen_food' and product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list, food_filter = "Frozen food")
   db.close()

@app.route('/snacks',methods = ['POST', 'GET'])
def snacks():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Snacks' and product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list, food_filter = "Snacks")
   db.close()

@app.route('/ice_cream',methods = ['POST', 'GET'])
def ice_cream():
   
   db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
   with db.cursor() as cursor:
      cursor.execute( """SELECT * from Product Where product_subtype = 'Ice_cream' and product_type = 'Food' """)
      food_list=(cursor.fetchall())
     
      return render_template("assisment_food.html",food_list =food_list, food_filter = "Ice cream")
   db.close()


@app.route('/purchase_drink',methods = ['POST', 'GET'])
def purchase_drink():
   if "Userid" in session:
      userid = session["Userid"]
      pid=request.form["product_id"]
      pqt=request.form["product_quantity"]
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      success= False
      with db.cursor() as cursor:
         cursor.execute( """SELECT product_price from Product WHERE product_id= """+str(pid))
         pd_price_db=(cursor.fetchall())
      pd_price_str=str(pd_price_db)

      pd_price=float(pd_price_str[2:len(pd_price_str)-4])
      total_pd_price=int(pqt)*pd_price

      with db.cursor() as cursor:
         cursor.execute( """SELECT Stock from Product WHERE product_id= """+str(pid))
         pd_stock_db=(cursor.fetchall())
      pd_stock_str=str(pd_stock_db)
      pd_stock=int(pd_stock_str[2:len(pd_stock_str)-4])
      db.close()

      if int(pqt) <= pd_stock:

         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         cursor = db.cursor() 
         sql="""INSERT INTO Shopping_cart (customer_id, product_id,shopping_cart_id, quantity,total_price ) VALUES (%d,%d,NULL,%d,%f)"""\
         %(int(userid), int(pid),int(pqt),total_pd_price)
         try:
            cursor.execute(sql)
            db.commit()
            success=True
         except:

            db.rollback() 
        
         db.close()
         if success ==True:
            db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
            cursor = db.cursor() 
            sql="""UPDATE Product SET Stock = Stock - %d WHERE product_id = %d"""%(int(pqt), int(pid))
            try:
               cursor.execute(sql)
               db.commit()
           
            except:

               db.rollback() 
        
            db.close()

      
         return redirect(url_for("drink"))
      else:
         return redirect(url_for("drink_error"))

@app.route('/purchase_food',methods = ['POST', 'GET'])
def purchase_food():
   if "Userid" in session:
      userid = session["Userid"]
      pid=request.form["product_id"]
      pqt=request.form["product_quantity"]
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      success= False
      with db.cursor() as cursor:
         cursor.execute( """SELECT product_price from Product WHERE product_id= """+str(pid))
         pd_price_db=(cursor.fetchall())
      pd_price_str=str(pd_price_db)

      pd_price=float(pd_price_str[2:len(pd_price_str)-4])
      total_pd_price=int(pqt)*pd_price

      with db.cursor() as cursor:
         cursor.execute( """SELECT Stock from Product WHERE product_id= """+str(pid))
         pd_stock_db=(cursor.fetchall())
      pd_stock_str=str(pd_stock_db)
      pd_stock=int(pd_stock_str[2:len(pd_stock_str)-4])
      db.close()

      if int(pqt) <= pd_stock:

         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         cursor = db.cursor() 
         sql="""INSERT INTO Shopping_cart (customer_id, product_id,shopping_cart_id, quantity,total_price ) VALUES (%d,%d,NULL,%d,%f)"""\
         %(int(userid), int(pid),int(pqt),total_pd_price)
         try:
            cursor.execute(sql)
            db.commit()
            success=True
         except:

            db.rollback() 
        
         db.close()
         if success ==True:
            db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
            cursor = db.cursor() 
            sql="""UPDATE Product SET Stock = Stock - %d WHERE product_id = %d"""%(int(pqt), int(pid))
            try:
               cursor.execute(sql)
               db.commit()
           
            except:

               db.rollback() 
        
            db.close()

      
         return redirect(url_for("food"))
      else:
         return redirect(url_for("drink_error"))




@app.route('/remove',methods = ['POST', 'GET'])
def remove():
   if request.method == 'POST':
      pqt = request.form["product_qty"]
      pid = request.form["product_id"]
      cartid = request.form["cart_id"]
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE Product SET Stock = Stock + %d WHERE product_id = %d"""%(int(pqt), int(pid))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()

      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql2="""DELETE FROM Shopping_cart WHERE shopping_cart_id = %d"""%(int(cartid))
      try:
         cursor.execute(sql2)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      return redirect(url_for("shopping_cart"))

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      
      
      login = request.form
      usrn = request.form["Username"]
      uspw = request.form["pwd"]
      
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         found=False
         a = """SELECT password from customer WHERE username='""" + usrn+"""'"""
         cursor.execute(a)
         x=(cursor.fetchall())
         len_x =len(str(x))
         y= str(x)

         if uspw ==  y[3:len_x-5] and ((y[3:len_x-5])!= ""):
            cursor.execute("""SELECT customer_id from customer WHERE username='""" + usrn+"""'""")
            cusid_db=(cursor.fetchall()[0])
            str_cusid_db = str(cusid_db)
            len_cusid_db = len(str(cusid_db))
            session["Userid"] = str_cusid_db[1:len_cusid_db-2]
            return redirect(url_for("profile_page"))
         else:
            return render_template("assisment_log_in.html",incorrect = "Incorrect username or password")
      db.close()


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('Userid', None)
   return redirect(url_for('login_page'))

@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      
      fir_nam= request.form['first_name']
      las_nam= request.form['last_name']
      sex_choice= request.form['sex']
      birth_date= request.form['birth']
      email_address=request.form['email']
      phone_no=request.form['phone']
      home_address=request.form['address']
      checkbox=request.form['agree_confirm']
      usrn = request.form['Username']
      uspw = request.form['pwd']

      email_list=[]
      email_count=0
      phone_list=[]
      phone_count=0
      usrn_list=[]
      usrn_count=0

      email_mail=[]
      email_mail.append(email_address)



      db_check= pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db_check.cursor() as cursor:
         cursor.execute( """SELECT COUNT(email) from customer Where email = '"""+str(email_address)+"""'""")
         email_list=(cursor.fetchall())
         cursor.execute( """SELECT COUNT(telephone_no) from customer Where telephone_no = '"""+str(phone_no)+"""'""")
         phone_list=(cursor.fetchall())
         cursor.execute( """SELECT COUNT(username) from customer Where username = '"""+str(usrn)+"""'""")
         usrn_list=(cursor.fetchall())

      db_check.close()
      for row in email_list:
         email_count+=(int(row[0]))

      for row in phone_list:
         phone_count+=(int(row[0]))

      for row in usrn_list:
         usrn_count+=(int(row[0]))
      
      if (email_count==0) and (phone_count==0) and (usrn_count==0):


         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")

         cursor = db.cursor() 

         x= str(fir_nam)


         sql = """INSERT INTO customer (first_name, last_name, telephone_no, email, Address, Sex, birth, username, password, collecting_points) VALUES ('%s','%s',%d,'%s','%s','%s','%s','%s','%s',0)"""\
         %(str(fir_nam), str(las_nam), int(phone_no), str(email_address), str(home_address),str(sex_choice), str(birth_date), str(usrn), str(uspw))
         try:
            cursor.execute(sql)
            db.commit()
            
         except:

            db.rollback() 

            return redirect(url_for("login_page"))
         db.close()
         msg = Message('Welcome to VincentStore', sender = 'VincentStoreOnline@gmail.com', recipients = email_mail[0].split())
         msg.html = render_template("assisment_mail_register.html",fir_nam=str(fir_nam), las_nam=str(las_nam), sex_choice=str(sex_choice), birth_date=str(birth_date), email_address=str(email_address), phone_no=str(phone_no), home_address=str(home_address), usrn=str(usrn))
   
         mail.send(msg)
         return redirect(url_for("login_page"))

      elif email_count!=0:
         return render_template("assisment_registor_error.html", fir_nam=fir_nam, las_nam=las_nam, sex_choice=sex_choice, birth_date=birth_date, email_address=email_address, phone_no=phone_no, home_address=home_address, usrn=usrn,uspw=uspw, error_email="This email has been registered" )
      elif phone_count!=0:
         return render_template("assisment_registor_error.html", fir_nam=fir_nam, las_nam=las_nam, sex_choice=sex_choice, birth_date=birth_date, email_address=email_address, phone_no=phone_no, home_address=home_address, usrn=usrn,uspw=uspw, error_phone="This phone number has been registered" )
      elif usrn_count!=0:
         return render_template("assisment_registor_error.html", fir_nam=fir_nam, las_nam=las_nam, sex_choice=sex_choice, birth_date=birth_date, email_address=email_address, phone_no=phone_no, home_address=home_address, usrn=usrn,uspw=uspw, error_usrn="This username has been registered" )

@app.route('/fir_name_update',methods = ['POST', 'GET'])
def fir_name_update():
   if request.method == 'POST':
      fir_nam= request.form['first_name_update']
      email=request.form['email_address']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()

      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET first_name = '%s' WHERE customer_id = %d"""%(str(fir_nam), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account first name has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/las_name_update',methods = ['POST', 'GET'])
def las_name_update():
   if request.method == 'POST':
      las_nam= request.form['last_name_update']
      email=request.form['email_address']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()

      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET last_name = '%s' WHERE customer_id = %d"""%(str(las_nam), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account last name has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/phone_update',methods = ['POST', 'GET'])
def phone_update():
   if request.method == 'POST':
      phone= request.form['phone_update']
      email=request.form['email_address']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()

      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET telephone_no = %d WHERE customer_id = %d"""%(int(phone), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account phone number has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/email_update',methods = ['POST', 'GET'])
def email_update():
   if request.method == 'POST':
      email= request.form['email_update']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()

      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET email = '%s' WHERE customer_id = %d"""%(str(email), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account email has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/address_update',methods = ['POST', 'GET'])
def address_update():
   if request.method == 'POST':
      address= request.form['address_update']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()
      email=request.form['email_address']
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET Address = '%s' WHERE customer_id = %d"""%(str(address), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account address has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/usrn_update',methods = ['POST', 'GET'])
def usrn_update():
   if request.method == 'POST':
      usrn= request.form['usrn_update']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()
      email=request.form['email_address']
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET username = '%s' WHERE customer_id = %d"""%(str(usrn), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account username has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))

@app.route('/uspw_update',methods = ['POST', 'GET'])
def uspw_update():
   if request.method == 'POST':
      uspw= request.form['password_update']
      time_p = datetime.datetime.now().time()
      date_p = datetime.datetime.now().date()
      email=request.form['email_address']
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      cursor = db.cursor() 
      sql="""UPDATE customer SET password = '%s' WHERE customer_id = %d"""%(str(uspw), int(session["Userid"]))
      try:
         cursor.execute(sql)
         db.commit()
           
      except:

         db.rollback() 
      db.close()
      msg = Message('Account warning', sender = 'VincentStoreOnline@gmail.com', recipients = email.split())
      msg.html = render_template("assisment_mail_update.html",content= "Your account password has been updated",time_p=time_p,date_p=date_p)
   
      mail.send(msg)
      return redirect(url_for("profile_page"))




@app.route('/staff',methods = ['POST', 'GET'])
def staff():
   return render_template("staff_log_in.html")


@app.route('/staff_profile_page',methods = ['POST', 'GET'])
def staff_profile_page():
   if "Staffid" in session:
      Staffid = session["Staffid"]
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT * from staff Where staff_id = '"""+Staffid+"""'""")
         personal_detail=(cursor.fetchall())
      db.close()
      
         

      return render_template("staff_profile.html",personal_detail = personal_detail)
     
   else:
      return redirect(url_for("staff"))


@app.route('/staff_order_page',methods = ['POST', 'GET'])
def staff_order_page():
   if "Staffid" in session:
     
   
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id  ORDER BY date_purchase DESC, time_purchase DESC  """)
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter="All")
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_drink',methods = ['POST', 'GET'])
def staff_order_page_drink():
   if "Staffid" in session:
      
   
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE product_type="Drink" ORDER BY date_purchase DESC, time_purchase DESC  """)
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter="Drink")
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_drink_sub',methods = ['POST', 'GET'])
def staff_order_page_drink_sub():
   if "Staffid" in session:
     
      sub=request.form["sub"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE product_type="Drink" and product_subtype='%s' ORDER BY date_purchase DESC, time_purchase DESC  """%(str(sub)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter=sub)
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_food',methods = ['POST', 'GET'])
def staff_order_page_food():
   if "Staffid" in session:
      
   
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE product_type="Food" ORDER BY date_purchase DESC, time_purchase DESC  """)
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter="Food")
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_food_sub',methods = ['POST', 'GET'])
def staff_order_page_food_sub():
   if "Staffid" in session:
     
      sub=request.form["sub"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE product_type="Food" and product_subtype='%s' ORDER BY date_purchase DESC, time_purchase DESC  """%(str(sub)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter=sub)
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_cusid_date',methods = ['POST', 'GET'])
def staff_order_page_cusid_date():
   if "Staffid" in session:
      
      search_cusid=request.form["search_cusid"]
      search_date=request.form["search_date"]
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE Shopping_record.customer_id =%d and date_purchase='%s'  ORDER BY date_purchase DESC, time_purchase DESC  """%(int(search_cusid),str(search_date)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter=("CustomerID: "+search_cusid+" & Date: "+search_date))
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_date',methods = ['POST', 'GET'])
def staff_order_page_date():
   if "Staffid" in session:
      
      
      search_date=request.form["search_date"]
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE date_purchase='%s'  ORDER BY date_purchase DESC, time_purchase DESC  """%(str(search_date)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter=("Date: "+search_date))
   else:
      return redirect(url_for("staff"))

@app.route('/staff_order_page_record',methods = ['POST', 'GET'])
def staff_order_page_record():
   if "Staffid" in session:
      
      
      search_id=request.form["search_id"]
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT Product.*, Shopping_record.quantity, Shopping_record.total_price, Shopping_record.Shopping_record_id,Shopping_record.date_purchase,Shopping_record.time_purchase,Shopping_record.delivery_date, Shopping_record.customer_id from Product INNER JOIN Shopping_record ON Product.product_id=Shopping_record.product_id WHERE Shopping_record.Shopping_record_id=%d  ORDER BY date_purchase DESC, time_purchase DESC  """%(int(search_id)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_order.html",pd_list =pd_list,Drink_filter=("Shopping record ID: "+search_id))
   else:
      return redirect(url_for("staff"))


@app.route('/staff_food',methods = ['POST', 'GET'])
def staff_food():
   if "Staffid" in session:
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT * from Product Where product_type = 'Food' """)
         food_list=(cursor.fetchall())
     
      
      db.close()
      return render_template("staff_food.html",food_list =food_list,  food_filter = "All")
   else:
      return redirect(url_for("staff"))


@app.route('/staff_drink',methods = ['POST', 'GET'])
def staff_drink():
   if "Staffid" in session:
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         cursor.execute( """SELECT * from Product Where product_type = 'Drink' """)
         drink_list=(cursor.fetchall())
     
      
      db.close()
      return render_template("staff_drink.html",drink_list =drink_list,  Drink_filter = "All")
   else:
      return redirect(url_for("staff"))



@app.route('/staff_update_page_stock_price',methods = ['POST', 'GET'])
def staff_update_page_stock_price():
   if "Staffid" in session:
      pid=request.form["product_id"]
     
      p_m_category=request.form["product_main_category"]
      pstock=request.form["product_stock"]
      pprice=request.form["product_price"]
      return render_template("staff_update_product_drink_stock_price.html",pid=pid, p_m_category=p_m_category,pstock=pstock,pprice=pprice)
   else:
      return redirect(url_for("staff"))



@app.route('/staff_update_page_drink',methods = ['POST', 'GET'])
def staff_update_page_drink():
   if "Staffid" in session:
      pid=request.form["product_id"]
      pname=request.form["product_name"]
      pbrands=request.form["product_brands"]
      pcategory=request.form["product_category"]
      pstock=request.form["product_stock"]
      pprice=request.form["product_price"]
      return render_template("staff_update_product_drink.html",pid=pid, product_name=str(pname),product_brand=pbrands,pcategory=pcategory,pstock=pstock,pprice=pprice)
   else:
      return redirect(url_for("staff"))

@app.route('/staff_update_page_food',methods = ['POST', 'GET'])
def staff_update_page_food():
   if "Staffid" in session:
      pid=request.form["product_id"]
      pname=request.form["product_name"]
      pbrands=request.form["product_brands"]
      pcategory=request.form["product_category"]
      pstock=request.form["product_stock"]
      pprice=request.form["product_price"]
      return render_template("staff_update_product_food.html",pid=pid, product_name=str(pname),product_brand=pbrands,pcategory=pcategory,pstock=pstock,pprice=pprice)
   else:
      return redirect(url_for("staff"))



@app.route('/staff_update_stock_price',methods = ['POST', 'GET'])
def staff_update_stock_price():
   if "Staffid" in session:
      if request.method == 'POST':
         pid=request.form["pid"]
        
         p_m_category=request.form["p_m_category"]
         pstock=request.form["pstock"]
         pprice=request.form["pprice"]


         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         cursor = db.cursor() 
         sql="""UPDATE Product SET  product_price =%f,Stock =%d WHERE product_id = %d"""\
         %( float(pprice),int(pstock), int(pid))
         try:
            cursor.execute(sql)
            db.commit()
           
         except:

            db.rollback() 
         db.close()
         

         db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         with db2.cursor() as cursor:
            cursor.execute( """SELECT * from Product  WHERE product_id='"""+(str(pid))+"""'""")
            pd_list=(cursor.fetchall())
           
         db2.close()
         
      if p_m_category == "Drink":
         return render_template("staff_drink.html",drink_list =pd_list,Drink_filter=("ID: "+pid))
      else:
         return render_template("staff_food.html",food_list =pd_list,food_filter=("ID: "+pid))


   else:
      return redirect(url_for("staff"))


@app.route('/staff_update_drink',methods = ['POST', 'GET'])
def staff_update_drink():
   if "Staffid" in session:
      if request.method == 'POST':
         pid=request.form["pid"]
         pname=request.form["product_name"]
         pbrands=request.form["product_brand"]
         pcategory=request.form["pcategory"]
         pstock=request.form["pstock"]
         pprice=request.form["pprice"]


         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         cursor = db.cursor() 
         sql="""UPDATE Product SET product_name = '%s', product_brand = '%s', product_price =%f,Stock =%d, product_subtype='%s' WHERE product_id = %d"""\
         %(str(pname),str(pbrands), float(pprice),int(pstock),str(pcategory),int(pid))
         try:
            cursor.execute(sql)
            db.commit()
           
         except:

            db.rollback() 
         db.close()
         

         db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         with db2.cursor() as cursor:
            cursor.execute( """SELECT * from Product  WHERE product_id='"""+(str(pid))+"""'""")
            pd_list=(cursor.fetchall())
           
         db2.close()
         

      return render_template("staff_drink.html",drink_list =pd_list,Drink_filter=("ID: "+pid))
         


   else:
      return redirect(url_for("staff"))



@app.route('/staff_update_food',methods = ['POST', 'GET'])
def staff_update_food():
   if "Staffid" in session:
      if request.method == 'POST':
         pid=request.form["pid"]
         pname=request.form["product_name"]
         pbrands=request.form["product_brand"]
         pcategory=request.form["pcategory"]
         pstock=request.form["pstock"]
         pprice=request.form["pprice"]


         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         cursor = db.cursor() 
         sql="""UPDATE Product SET product_name = '%s', product_brand = '%s', product_price =%f,Stock =%d, product_subtype='%s' WHERE product_id = %d"""\
         %(str(pname),str(pbrands), float(pprice),int(pstock),str(pcategory),int(pid))
         try:
            cursor.execute(sql)
            db.commit()
           
         except:

            db.rollback() 
         db.close()
         

         db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         with db2.cursor() as cursor:
            cursor.execute( """SELECT * from Product  WHERE product_id='"""+(str(pid))+"""'""")
            pd_list=(cursor.fetchall())
           
         db2.close()
         

      return render_template("staff_food.html",food_list =pd_list,food_filter=("ID: "+pid))
         


   else:
      return redirect(url_for("staff"))



@app.route('/staff_drink_page_drink_sub',methods = ['POST', 'GET'])
def staff_drink_page_drink_sub():
   if "Staffid" in session:
      
      sub=request.form["sub"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT * from Product WHERE product_type="Drink"  and product_subtype='%s'  """%(sub))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_drink.html",drink_list =pd_list,Drink_filter=sub)
   else:
      return redirect(url_for("staff"))

@app.route('/staff_drink_page_food_sub',methods = ['POST', 'GET'])
def staff_drink_page_food_sub():
   if "Staffid" in session:
      
      sub=request.form["sub"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT * from Product WHERE product_type="Food"  and product_subtype='%s'  """%(sub))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_food.html",food_list =pd_list,food_filter=sub)
   else:
      return redirect(url_for("staff"))



@app.route('/staff_search_drink_ID',methods = ['POST', 'GET'])
def staff_search_drink_ID():
   if "Staffid" in session:
      search_drink=request.form["search_drink"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT * from Product WHERE product_type="Drink"  and product_id=%d  """%(int(search_drink)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_drink.html",drink_list =pd_list,Drink_filter=("ID: "+search_drink))
   else:
      return redirect(url_for("staff"))


@app.route('/staff_search_food_ID',methods = ['POST', 'GET'])
def staff_search_food_ID():
   if "Staffid" in session:
      search_food=request.form["search_food"]
      
      db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db2.cursor() as cursor:
         cursor.execute( """SELECT * from Product WHERE product_type="Food"  and product_id=%d  """%(int(search_food)))
         pd_list=(cursor.fetchall())
           
      db2.close()
         

      return render_template("staff_food.html",food_list =pd_list,food_filter=("ID: "+search_food))
   else:
      return redirect(url_for("staff"))



@app.route('/staff_update_new',methods = ['POST', 'GET'])
def staff_update_new():
   if "Staffid" in session:
      return render_template("staff_product_new.html")
   else:
      return redirect(url_for("staff"))


@app.route('/staff_update_new_insert',methods = ['POST', 'GET'])
def staff_update_new_insert():
   if "Staffid" in session:
      if request.method == 'POST':
         
         pname=request.form["product_name"]
         pbrands=request.form["product_brand"]
         
         p_main_category=request.form["p_main_category"]
         pstock=request.form["pstock"]
         pprice=request.form["pprice"]



         if p_main_category == "Drink":
            p_category=request.form["pcategory_drink"]
         else:
            p_category=request.form["pcategory_food"]


         db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")

         cursor = db.cursor() 


         sql = """INSERT INTO Product (product_id, product_name, product_brand, product_price, Stock, product_type, product_subtype) VALUES (NULL,'%s','%s',%f,%d,'%s','%s')"""\
         %(str(pname),str(pbrands),float(pprice),int(pstock),str(p_main_category),str(p_category))
         try:
            cursor.execute(sql)
            db.commit()
            
         except:

            db.rollback() 

      
         db.close()
         db2 = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
         with db2.cursor() as cursor:
            if p_main_category == "Drink":
               cursor.execute( """SELECT * from Product where product_type = "Drink" order by product_id desc """)
            else:
               cursor.execute( """SELECT * from Product where product_type = "Food" order by product_id desc """)
            pd_list=(cursor.fetchall())
           
         db2.close()
         
      if p_main_category == "Drink":
         return render_template("staff_drink.html",drink_list =pd_list,drink_filter=("ID: descending"))
      else:
         return render_template("staff_food.html",food_list =pd_list,food_filter=("ID: descending"))
   else:
      return redirect(url_for("staff"))


@app.route('/staff_login',methods = ['POST', 'GET'])
def staff_login():
   if request.method == 'POST':
      
      
      login = request.form
      usrn = request.form["Username"]
      uspw = request.form["pwd"]
      
      db = pymysql.connect("localhost", "admin", "123456aaa", "ALL POS")
      with db.cursor() as cursor:
         found=False
         a = """SELECT password from staff WHERE username='""" + usrn+"""'"""
         cursor.execute(a)
         x=(cursor.fetchall())
         len_x =len(str(x))
         y= str(x)

         if uspw ==  y[3:len_x-5] and ((y[3:len_x-5])!= ""):
            cursor.execute("""SELECT staff_id from staff WHERE username='""" + usrn+"""'""")
            cusid_db=(cursor.fetchall()[0])
            str_cusid_db = str(cusid_db)
            len_cusid_db = len(str(cusid_db))
            session["Staffid"] = str_cusid_db[1:len_cusid_db-2]
            return redirect(url_for('staff_profile_page'))
         else:
            return render_template("staff_log_in.html",incorrect = "Incorrect username or password")
      db.close()


@app.route('/staff_logout')
def staff_logout():
   # remove the username from the session if it is there
   session.pop('Staffid', None)
   return redirect(url_for('staff'))



if __name__ == '__main__':
   app.run(debug = True)
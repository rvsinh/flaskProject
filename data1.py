from flask import Flask
from flask import render_template,request
import sqlite3

#Make sqlite connection here

conn = sqlite3.connect('database.db')

#final application Detail from here
app = Flask(__name__)

#for homePage
@app.route("/")
def home():
    return render_template("home.html")

#for about page
@app.route("/about")
def about():
    return render_template("about.html",myPageName="about",myList=[0,1,2,3,4,5])

#for signup detail
@app.route('/signup')
def signup():
    return render_template("signup.html")

#use to seee that connection with is work or not
@app.route('/userList')
def userList():
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    return render_template("userList.html",rows = rows)

#use this function to add the userdata in database
@app.route('/addData',methods = ['POST','GET'])
def addData():
    if request.method == "POST":
        try:
            #division = request.form["selectData"]
            detail = request.form["sDetail"]
            field1 = request.form["field1"]
            field2 = request.form["field2"]
            field3 = request.form["field3"]
            field4 = request.form["field4"]
            print(detail,field1,field2,field3,field4)
        except:
            pass
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from department")
    rows = cur.fetchall()
    print(rows)
    return render_template("addNew.html",rows = rows)

#import app
if __name__ == "__main__":
    app.run()

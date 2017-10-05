from flask import Flask
import os
from flask import render_template,request,redirect,url_for,session,flash
from werkzeug.utils import secure_filename
from flask_mail import Mail,Message
#from flask.ext.session import Session
#from wrekzeug.utils import secure_filename
import sqlite3

#final application Detail from here
app = Flask(__name__)
app.secret_key = 'A0Zr98j'
mail = Mail(app)
#Session(app)

#configure mail
app.config['MAIL_SERVER']='smtp.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'noreply.notification@thermaxglobal.com'
app.config['MAIL_PASSWORD'] = '!Thermax@321'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

#config session
mail = Mail(app)

#Upload folder where temprorarily store the file for backup
UPLOAD_FOLDER = 'C:\\Users\\ravi.singh2\\Desktop\\dev\\finalProject\\backup'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Make sqlite connection here

conn = sqlite3.connect('database.db')



#we need to upload data into the database not in the folder
ALLOWED_EXTENSIONS = set(['txt','pdf','png'])



#for homePage
@app.route("/")
def home():
    if 'userName' in session:
        return redirect(url_for('about'))
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userName' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        print("come to login")
        userName = request.form['username']
        passWord = request.form['password']
        if userName == 'admin' and passWord == 'Thermax':
            session['userName'] = userName
            flash('Logged in successfully.')
            #next = flask.request.args.get('next')
            return redirect(url_for('about'))
        return redirect(url_for('home'))
    return render_template('index.html')

#for logout purpose
@app.route("/logout")
def logout():
    session.pop('userName',None)
    return redirect(url_for('home'))


#for about page
@app.route("/about")
def about():
    if 'userName' not in session:
        return redirect(url_for('login'))
    return render_template("about.html",myPageName="about",myList=[0,1,2,3,4,5])

#for signup detail
@app.route('/signup')
def signup():
    if 'userName' in session:
        return redirect(url_for('about'))
    return render_template("signup.html")

#use to seee that connection with is work or not
@app.route('/userList')
def userList():
    if 'userName' not in session:
        return redirect(url_for('login'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    cur.execute("select * from department")
    division = cur.fetchall()
    #print(division)
    return render_template("userList.html",rows = rows,division = division)

#use this function to add the userdata in database
@app.route('/addData',methods = ['GET','POST'])
def addData():
    if 'userName' not in session:
        return redirect(url_for('login'))
    cur = conn.cursor()
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                return "File not submitted... try again"
            #store file into a variable
            f = request.files['file']
            fileName = secure_filename(f.filename)
            division = request.form["selectData"]
            print("Select option is :",division)
            print("select file Detail is :",os.path.abspath(fileName))
            detail = request.form["sDetail"]
            field1 = request.form["field1"]
            field2 = request.form["field2"]
            field3 = request.form["field3"]
            field4 = request.form["field4"]
            final = "Data is Submitted"
            date = "13.01.2017"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            query = "insert into software(category,detail,field1,field2,field3,field4,final,insertdate) values ('"+division+"','"+detail+"','"+field1+"','"+field2+"','"+field3+"','"+field4+"','"+final+"','"+os.path.abspath(fileName)+"')"
            print(query)
            cur.execute(query)
            conn.commit()
            print(field1,field2,field3,field4)
        except:
            #print(E)
            #print(request.form["field1"])
            print("Not working well")
            pass
    conn.row_factory = sqlite3.Row
    cur.execute("select * from department")
    rows = cur.fetchall()
    print(rows)
    return render_template("addNew.html",rows = rows)

#use this function to upload the document to related the data about user
@app.route('/upload',methods=['POST','GET'])
def uploadData():
    if request.method == "POST":
        if 'file' not in request.files:
            return render_template("uploadExample.html")
        else:
            cur = conn.cursor()
            print("Come in uploadFunction")
            f = request.files['file']
            fileName = secure_filename(f.filename)
            #f.save(secure_filename(f.filename))
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            print(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            fp = open(os.path.join(app.config['UPLOAD_FOLDER'],fileName),"rb")
            sql = "insert into fileData(file,type,file_name) values (?,?,?)"
            cur.execute(sql,[sqlite3.Binary(fp.read()),'png',f.filename])
            conn.commit()
            fp.close()
            return "File Upload successfully"
    return render_template("uploadExample.html")
#show detail regarding user request
@app.route('/softList/<guest>',methods=['Get','POST'])
def softList(guest):
    if 'userName' not in session:
        return redirect(url_for('login'))
    if len(guest) == 0:
        return redirect(url_for('usrList'))
    else:
        cur = conn.cursor()
        query = "select * from  softList where deptName = '"+guest+"'"
        cur.execute(query)
        rows = cur.fetchall()
        return render_template("showDetail.html",rows = rows, guest = guest)
#show mail detail
@app.route('/send')
def send():
    msg = Message('Hello', sender = 'noreply.notification@thermaxglobal.com', recipients = ['ravi.s.singh@thermaxglobal.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    try:
        mail.send(msg)
        return "massage sending Successfully"
    except:
        return "Mesaage sending not work"
#import app
if __name__ == "__main__":
    app.run()

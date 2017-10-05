from flask import Flask
import os
from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
#from wrekzeug.utils import secure_filename
import sqlite3

#final application Detail from here
app = Flask(__name__)

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
@app.route('/addData',methods = ['GET','POST'])
def addData():
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
#import app
if __name__ == "__main__":
    app.run()

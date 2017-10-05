from flask import Flask
import os,json
import pygal
from flask import render_template,request,redirect,url_for,session,flash,send_from_directory
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
    return "Contact admin"

#use to seee that connection with is work or not
@app.route('/userList')
def userList():
    if 'userName' not in session:
        return redirect(url_for('login'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('PRAGMA table_info(finalTable);')
    columnData = cur.fetchall()
    cur.execute("select * from finalTable")
    rows = cur.fetchall()
    cur.execute("select * from department")
    division = cur.fetchall()
    #print(division)
    return render_template("userList.html",rows = rows,division = division,columnData=columnData)

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
            print("show all form data in simeple format : ")
            print(request.form)
            print("Select option is :",division)
            print("select file Detail is :",os.path.abspath(fileName))
            data = []
            try:
                data.append(request.form["field1"])
                data.append(request.form["field2"])
                data.append(request.form["field3"])
                data.append(request.form["field18"])
                data.append(request.form["field4"])
                data.append(request.form["field15"])
                data.append(request.form["field16"])
                data.append(request.form["field17"])
                data.append(request.form["selectData"])
                #data.append(request.form["sDetail"])
                data.append(request.form["field5"])
                data.append(request.form["field6"])
                data.append(request.form["field7"])
                data.append(request.form["lDate"])
                data.append(request.form["nDate"])
                data.append(request.form["field8"])
                data.append(request.form["field9"])
                data.append(request.form["field10"])
                data.append(request.form["field11"])
                data.append(request.form["field12"])
                data.append(request.form["field13"])
                data.append(request.form["field14"])
                data.append(request.form["pDate"])
                final = "Data is Submitted"
                #date = "13.01.2017"
                print(data)
            except Exception ,e:
                return "Following error : "+str(e)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            #query = "insert into software(category,detail,field1,field2,field3,field4,final,insertdate) values ('"+division+"','"+detail+"','"+field1+"','"+field2+"','"+field3+"','"+field4+"','"+final+"','"+os.path.abspath(fileName)+"')"
            query2 = "insert into finalTable(publisher,softName,version,serial,licenseType,licenseMetric,numberOfLicense,licenseServer,division,divisionKeyUser,divisionKeyEmail,amcStatus,lastAmcDate,nextAmcDate,partnerName,partnerContact,partnerEmailId,principleContact,princpleEmail,poRaisedDiv,poNumber,poDate) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            print(query2)
            #print(query)
            cur.execute(query2,data)
            conn.commit()
            #print(field1,field2,field3,field4)
        except Exception,e:
            return "the reason is : "+str(e)
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
    if 'userName' not in session:
        return redirect(url_for('login'))
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
            #try to load data in the database through json form
            fp = open(os.path.join(app.config['UPLOAD_FOLDER'],fileName),"r")
            try:
                datastore = json.load(fp)
                for i in datastore:
                    lst = datastore[i].keys()
                    query = "insert into users(userName,password,emailId) values(?,?,?)"
                    data = []
                    for j in lst:
                        data.append(datastore[i][j])
                    try:
                        cur.execute(query,data)
                        conn.commit()
                    except Exception,e:
                        return("Database user insert problem: "+str(e))
            except Exception,e:
                return "Json file format error : "+str(e)
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
    if 'userName' not in session:
        return redirect(url_for('login'))
    msg = Message('Hello', sender = 'noreply.notification@thermaxglobal.com', recipients = ['ravi.s.singh@thermaxglobal.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    try:
        mail.send(msg)
        return "massage sending Successfully"
    except:
        return "Mesaage sending not work"

#show everydivisionData in graph wise so its easy to see that which division used more software and pc related cost
@app.route('/graph')
def showGraph():
    if 'userName' not in session:
        return redirect(url_for('login'))
    cur = conn.cursor()
    #first get total count of software
    query = ("select count(*) as cnt from softList")
    try:
        cur.execute(query)
        rows = cur.fetchall()
        totalSoft = int(rows[0][0])
        print(totalSoft)
    except Exception,e:
        return "Db error while count(softList) : "+str(e)
    query = ("select count(*) as num,deptName from softList group by(deptName)")
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except Exception,e:
        return "check db configureation :"+str(e)
    sendData = rows
    #now do operation on this perticular data
    try:
        pie_chart = pygal.Pie()
        pie_chart.title = "Software userd by all Division"
        for row in rows:
            print(row['deptName'],int(row['num']))
            pie_chart.add(row['deptName'],(int(row['num'])*100)/totalSoft)
        print("final chart",pie_chart)
        pie_Data =pie_chart.render_data_uri()
        return render_template('showGraph.html',pie_Data = pie_Data)
    except Exception,e:
        return "rendering graph problem :"+str(e)
        pass
    #return render_template('showGraph.html',rows=rows)

#showDetailGraph
#this function is going to show that in which division which type of software used most
@app.route('/detGraph/<divName>',methods=['POST','GET'])
def detGraph(divName):
    if 'userName' not in session:
        return redirect(url_for('login'))
    return "This function is work :"+divName

#download report from flask application
@app.route('/download', methods=['GET', 'POST'])
def download():
    if 'userName' not in session:
        return redirect(url_for('login'))
    filename = "dbData.json"
    #uploads = (os.path.join(app.config['UPLOAD_FOLDER'],fileName))
    #return str(app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename,mimetype='text/json',as_attachment=True)

#update peticular software and update the table also
@app.route('/update/<id>',methods=['POST','GET'])
def updateRow(id):
    if 'userName' not in session:
        return redirect(url_for('login'))
    curr = conn.cursor()
    if request.method == "POST":
        print("Come in request method")
        try:
            if 'file' not in request.files:
                print("File not submitted... try again")
            #store file into a variable
            else:
                print("Handle it later")
                #f = request.files['file']
                #fileName = secure_filename(f.filename)
            #division = request.form["selectData"]
            data = []
            try:
                data.append(request.form["field1"])
                data.append(request.form["field2"])
                data.append(request.form["field3"])
                data.append(request.form["field18"])
                data.append(request.form["field4"])
                data.append(request.form["field15"])
                data.append(request.form["field16"])
                data.append(request.form["field17"])
                data.append(request.form["field31"])
                #data.append(request.form["sDetail"])
                data.append(request.form["field5"])
                data.append(request.form["field6"])
                data.append(request.form["field7"])
                data.append(request.form["lDate"])
                data.append(request.form["nDate"])
                data.append(request.form["field8"])
                data.append(request.form["field9"])
                data.append(request.form["field10"])
                data.append(request.form["field11"])
                data.append(request.form["field12"])
                data.append(request.form["field13"])
                data.append(request.form["field14"])
                data.append(request.form["pDate"])
                final = "Data is Submitted"
                #date = "13.01.2017"
                print(data)
            except Exception ,e:
                return "Following error : "+str(e)
            #f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            #query = "insert into software(category,detail,field1,field2,field3,field4,final,insertdate) values ('"+division+"','"+detail+"','"+field1+"','"+field2+"','"+field3+"','"+field4+"','"+final+"','"+os.path.abspath(fileName)+"')"
            #query2 = "insert into finalTable(publisher,softName,version,serial,licenseType,licenseMetric,numberOfLicense,licenseServer,division,divisionKeyUser,divisionKeyEmail,amcStatus,lastAmcDate,nextAmcDate,partnerName,partnerContact,partnerEmailId,principleContact,princpleEmail,poRaisedDiv,poNumber,poDate) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            query3 = '''update finalTable set publisher = ?,softName = ? , version = ?, serial = ?, licenseType = ?, licenseMetric = ?, numberOfLicense = ?, licenseServer = ? , division = ?, divisionKeyUser = ?, divisionKeyEmail = ?, amcStatus = ? , lastAmcDate = ?, nextAmcDate = ?, partnerName = ?,partnerContact = ?,partnerEmailId = ? , principleContact = ? , princpleEmail = ?, poRaisedDiv = ?,poNumber = ?,poDate = ?  '''
            #print(query2)
            #print(query)
            curr.execute(query3,data)
            conn.commit()
            #print(field1,field2,field3,field4)
        except Exception,e:
            return "the reason is : "+str(e)
            #print(request.form["field1"])
            print("Not working well")
            pass
    try:
        curr.execute('select * from finalTable where id='+id)
        row = curr.fetchall()
    except Exception,e:
        return "database row id problem "+str(e)
    return render_template('updateRow.html',rows=row)
    
#function to delete the row of table:
#add some method than its gone complex for user to delete the data
@app.route('/delete/<id>',methods=['POST','GET'])
def delete(id):
    if request.method  == 'POST':
        if request.form['password'] == 'Thermax':
            return render_template('about.html')
        else:
            error = 'Invalid Password'
            return redirect(url_for('logout'))
    flash("Are you Sure want to delete",'error')
    return render_template('deleteRow.html')
#import app
if __name__ == "__main__":
    app.run(host="10.101.34.78",port=int("80"))

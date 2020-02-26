import datetime
import pickle
import socket
import time
from platform import uname
from urllib.request import Request, urlopen

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MYSQL_HOST= 'localhost',
    MYSQL_USER='vatsal',
    MYSQL_PASSWORD='12345678',
    MYSQL_DB='sys'
)

import json 
import pyrebase

config = {
  "apiKey": "AIzaSyDvNt03NBUB8Sue1siFXMGu0QnE_sMDVdk",
  "authDomain": "pix-health.firebaseapp.com",
  "databaseURL": "https://pix-health.firebaseio.com",
  "projectId": "pix-health",
  "storageBucket": "pix-health.appspot.com",
  "messagingSenderId": "588673929157",
  "appId": "1:588673929157:web:a8e1295a14bf49a6e245ac",
  "measurementId": "G-P6P9ZZS8PF"
}

firebase = pyrebase.initialize_app(config=config)

db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


app.secret_key = 'vatsalparsaniya'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/signup_page/")
def signup():
    return render_template("Signup.html")

@app.route("/signup_check/", methods=['POST'])
def signup_check():
    email = request.form['email']
    password_1 = request.form['psw']
    password_2 = request.form['psw-repeat']
    user_id = request.form['uid']

    if password_1 == password_2:
        email = str(email).lower()
        email_database = email.split('@')[0]
        result = db.child("UIds").child("UserID").get().val()
        result[email_database] = user_id
        result = db.child("UIds").child("UserID").set(result)
        try:
            user = auth.create_user_with_email_and_password(email,password_1)
        except Exception as e:
            if json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'EMAIL_EXISTS':
                flash("Email ID is already Exists")
                return render_template('index.html')
            elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_EMAIL':
                flash("Email ID is Invalid")
                return render_template("Signup.html")
            else:
                flash("Something Went Wrong")
                return render_template("Signup.html")
        flash("Successfully SingUP")
        return render_template('index.html')
    else:
        flash("password not match")
        return render_template("Signup.html")





@app.route("/doctor_login/")
def doctor_login():
    return render_template("doctor_login.html")

@app.route('/dlogin_check/', methods=['POST'])
def dlogin_check():
    if request.method == "POST":
        email = str(request.form['email']).lower()
        password = request.form['psw']
        try: 
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print("Error : ")
            print(e.args[-1])
            if json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'EMAIL_NOT_FOUND':
                flash("Email ID not Found , Enter Valid Email")
                return render_template("doctor_login.html")
            elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_PASSWORD':
                flash("Invalid  password , enter valid password")
                return render_template("doctor_login.html")
            else:
                flash("data Not Found")
                return render_template("index.html")
        Uids = db.child("UIds").child("UserID").get().val()
        User_id = Uids[email.split('@')[0]]
        doctor_id = db.child("Doctors").get().val()
        if User_id in doctor_id:
            flash("Successfully User : {} Data found ".format(doctor_id[str(User_id)]["Name"]))
            return render_template("doctor_dashboard.html",uname=doctor_id[str(User_id)]["Name"])
        else:
            flash("you are not authorised as a Doctor")
            return render_template("doctor_login.html")

@app.route("/doctor_deshboard/<uname>/")
def lelele(uname):
    return render_template("doctor_dashboard.html",uname=uname)  

@app.route("/Search_card_no/<user>")
def Search_card_no(user):
    host = '192.168.43.48' # as both code is running on same pc
    port = 5005 # socket server port number
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server
    data = client_socket.recv(1024)  # receive response
    rdata=pickle.loads(data)
    client_socket.close()  
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sys.basic_details WHERE CARDNUMBER='"+str(rdata)+"';")
    first = cur.fetchall()
    print(first)
    cur.execute("SELECT * FROM sys.p_medical_visits WHERE CARDNO='"+str(rdata)+"';")
    second = cur.fetchall()
    # print(second)
    mysql.connection.commit()
    cur.close()
    return render_template("show_card_details.html",uname=user,card_number=str(rdata),first=first,second=second)

@app.route("/updatedetails/<Doctor>/<cardno>/", methods=['POST'])
def update_Visit_details(Doctor,cardno):
    if request.method == "POST":
        caseflow = request.form['caseflow']
        Diagnosis = request.form["Diagnosis"]
        Prescrioption = request.form["Prescrioption"]
        Report = request.form["Report"]
        hospital = request.form["hospital"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sys.p_medical_visits VALUES ('"+cardno+"','"+caseflow+"','"+Doctor+"','"+hospital+"','"+str(datetime.datetime.now())+"','"+Diagnosis+"','"+Prescrioption+"','"+Report+"');")
        # first = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        flash("Data submitted successfully")
        return render_template("doctor_dashboard.html",uname=Doctor)

@app.route("/doctor_past_patient/<uname>/")
def doctor_past_patient(uname):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sys.p_medical_visits WHERE DOCTOR='"+str(uname)+"';")
        first = cur.fetchall()
        print(first)
        mysql.connection.commit()
        cur.close()
        return render_template("doctor_past_patient.html",uname=uname,Data=first)


@app.route("/patient_login/")
def patient_login():
    return render_template("patient_login.html")

@app.route('/plogin_check/', methods=['POST'])
def plogin_check():
    if request.method == "POST":
        email = str(request.form['email']).lower()
        password = request.form['psw']
        try: 
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print("Error : ")
            print(e.args[-1])
            if json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'EMAIL_NOT_FOUND':
                flash("Email ID not Found , Enter Valid Email")
                return render_template("patient_login.html")
            elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_PASSWORD':
                flash("Invalid  password , enter valid password")
                return render_template("patient_login.html")
            else:
                flash("data Not Found")
                return render_template("index.html")
        Uids = db.child("UIds").child("UserID").get().val()
        User_id = Uids[email.split('@')[0]]
        flash(" Patient Login Successfully ")
        return render_template("patient_dashboard.html",uname=User_id)

@app.route("/patient_dashboardd/<uname>/")
def patient_dashboardd(uname):
    return render_template("patient_dashboard.html",uname=uname)

# Patient Details
@app.route("/Pdetail/<uname>/")
def Pdetail(uname):
    result = db.child("Users").child(str(uname)).get().val()
    return render_template("PP_data.html",uname=uname,Data=result["Details"])

# patient Medical History
@app.route("/Mphistory/<uname>/")
def Mphistory(uname):
    result = db.child("Users").child(str(uname)).get().val()["Reports"]
    keys = []
    values = []
    for key, val in result.items():
        keys.append(key)
        values.append(val)
    length=len(values)
    return render_template("Hpdata.html",values=values,uname=uname)





@app.route("/chemist_login/")
def chemist_login():
    return render_template("chemist_login.html")

@app.route('/clogin_check/', methods=['POST'])
def clogin_check():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EMAIL,PASSWORD FROM sys.chemist;")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if (email,password) in data:
            flash("Loged in Successfully")
            cur = mysql.connection.cursor()
            cur.execute("SELECT EMAIL FROM sys.chemist WHERE EMAIL=\'"+email+"\';")
            uname = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template("chemist_dashboard.html",uname=uname[0][0])
        else:
            flash("Wrong!! Email or Password")
            return redirect(url_for("chemist_login"))

@app.route("/chemist_dashboardd/<uname>/")
def chemist_desbd(uname):
    return render_template("chemist_dashboard.html",uname=uname)

@app.route("/chemist_scratch_data/<uname>/")
def chemist_scratch_data(uname):
    host = '192.168.43.48' # as both code is running on same pc
    port = 5005 # socket server port number

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = client_socket.recv(1024)  # receive response
    rdata=pickle.loads(data)
    # print(rdata)  # show in terminal
    # mdata = str(rdata)
    client_socket.close()  
    cur = mysql.connection.cursor()
    # cur.execute("SELECT USER FROM sys.chemist WHERE EMAIL=\'"+email+"\';")
    cur.execute("SELECT * FROM sys.p_medical_visits WHERE CARDNO='"+str(rdata)+"';")
    first = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("camist_card.html",Data=first,uname=uname)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234,debug=True)

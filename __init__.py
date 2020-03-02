import datetime
import pickle
import socket
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from platform import uname
from urllib.request import Request, urlopen
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

def client_program():
    host = '192.168.43.48' # as both code is running on same pc
    port = 5005  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = client_socket.recv(1024)  # receive response
    data = pickle.loads(data)
    # print('Received from server: ' + str(data))  # show in terminal
    return data


def get_img(doc_name,pat_name,Meds,Quantity,Dosage):
    pattern = Image.open("static\img\lena.jpg", "r").convert('RGB')

    d = datetime.now()
    d= str(d)
    davaa = Meds 
    quan = Quantity
    desc = Dosage

    size = width, height = pattern.size
    draw = ImageDraw.Draw(pattern,'RGBA')
    font = ImageFont.truetype("arial.ttf", 25)

    draw.text((120,10), "Doctor Name:" + doc_name, (0, 0, 0, 0),font=font)
    draw.text((1000,10), "Patient Name:" + pat_name, (0, 0, 0, 0),font=font)
    draw.text((540,10), d, (0, 0, 0, 0),font=font)

    draw.text((120,30), "--------------------------------------------------------------------------------------------------------------------------------------------", (0, 0, 0, 0),font=font)
    draw.text((120,50), "Sr", (0, 0, 0, 0),font=font)
    draw.text((240,50), "Name", (0, 0, 0, 0),font=font)
    draw.text((580,50), "Quantity", (0, 0, 0, 0),font=font)
    draw.text((900,50), "Dosage", (0, 0, 0, 0),font=font)
    draw.text((120,70), "--------------------------------------------------------------------------------------------------------------------------------------------", (0, 0, 0, 0),font=font)
    draw.rectangle([(120,90),(1200,500)],None)
    w=0
    for j in range(len(quan)):
        draw.text((120, (90+w)), str(j), (0, 0, 0, 0), font=font)
        draw.text((240, (90+w)), davaa[j], (0, 0, 0, 0), font=font)
        draw.text((580, (90+w)), quan[j], (0, 0, 0, 0), font=font)
        draw.text((900, (90+w)), desc[j], (0, 0, 0, 0), font=font)
        draw.text((120, (110+w)),"--------------------------------------------------------------------------------------------------------------------------------------------",(0, 0, 0, 0), font=font)
        w=w+50
    pattern.save("static/img/prescription.jpg")
    

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
            return render_template("doctor_dashboard.html",uname=User_id)
        else:
            flash("you are not authorised as a Doctor")
            return render_template("doctor_login.html")

@app.route("/doctor_deshboard/<uname>/")
def lelele(uname):
    return render_template("doctor_dashboard.html",uname=uname)  

@app.route("/Search_card_no/<user>/")
def Search_card_no(user):
    uname = str(client_program())
    # uname = "760207156235"
    print(uname)
    result1 = db.child("Users").child(str(uname)).get().val()
    result2 = db.child("Users").child(str(uname)).get().val()["Reports"]
    values = []
    for key, val in result2.items():
        values.append(val)
    return render_template("show_card_details.html",values=values,uname=user,Data=result1["Details"],patientid=uname)

@app.route("/p_details_by_id/<uname>/", methods=['POST'])
def p_details_by_id(uname):
    pid = request.form['PID']
    pid = str(pid)
    result1 = db.child("Users").child(str(pid)).get().val()
    result2 = db.child("Users").child(str(pid)).get().val()["Reports"]
    values = []
    for key, val in result2.items():
        values.append(val)
    return render_template("show_card_details.html",values=values,uname=uname,Data=result1["Details"],patientid=pid)


@app.route("/updatedetails/<Doctor>/<cardno>/", methods=['POST'])
def update_Visit_details(Doctor,cardno):
    if request.method == "POST":
        date = str(datetime.today().strftime('%d-%m-%Y'))
        Diagnosis = str(request.form['Diagnosis'])
        Doctor_Name = db.child("Doctors").child(str(Doctor)).get().val()["Name"]
        Hospital_name = db.child("Doctors").child(str(Doctor)).get().val()["Hospitals"][0]
        patient_name = db.child("Users").child(str(cardno)).child("Details").get().val()["Name"]
        quantity = str(request.form['quantity']).split(',')
        Meds = str(request.form['Meds']).split(',')
        Dosage = str(request.form['Dosage']).split(',')
        get_img(Doctor_Name,patient_name,Meds,quantity,Dosage)

        result =  db.child("Users").child(str(cardno)).get().val()["Reports"]
        keys = []
        value = []
        for key , val  in result.items():
            keys.append(key)
            value.append(val)
        length = len(value)
        next_id = length+1
        next_id = "Id"+str(next_id)
        img_path = "Prescription/{}/{}/User{}.jpg".format(cardno,next_id,1)
        storage.child(img_path).put("static/img/prescription.jpg")
        pre_url = str(storage.child(img_path).get_url(1))
        img_path = "Prescription/{}/{}/User{}.jpg".format(cardno,next_id,2)
        storage.child(img_path).put("static/img/lena.jpg")
        rep_url = str(storage.child(img_path).get_url(1))
        db.child("Users").child(str(cardno)).child("Reports").child(next_id).set({"Date":date,"Diagnosis":Diagnosis,"Doctor":Doctor_Name,"DoctorID":Doctor,"Hospital":Hospital_name,"PrescriptionUrl":pre_url,"ReportUrl":rep_url})
        result = db.child("Doctors").child(str(Doctor)).child("PastRecords").get().val()
        next_id = "RecordId" + str(len(result)+1)
        db.child("Doctors").child(str(Doctor)).child("PastRecords").child(next_id).set({"Date":date,"Diagnosis":Diagnosis,"PatientId":cardno})
        flash("Data submitted successfully")
        return render_template("doctor_dashboard.html",uname=Doctor)

@app.route("/doctor_past_patient/<uname>/")
def doctor_past_patient(uname):
        result = db.child("Doctors").child(str(uname)).get().val()["PastRecords"]
        values = []
        key1 = []
        for key,val in result.items():
            key1.append(key)
            values.append(val)
        return render_template("doctor_past_patient.html",uname=uname,Data=values,Data2=key1)

@app.route("/d_past_patient_details/<uname>/<pid>/")
def d_past_patient_details(uname,pid):
    result1 = db.child("Users").child(str(pid)).get().val()
    result2 = db.child("Users").child(str(pid)).get().val()["Reports"]
    values = []
    for key, val in result2.items():
        values.append(val)
    return render_template("d_past_patient_details.html",values=values,uname=uname,Data=result1["Details"],patientid=uname)






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
    values = []
    for key, val in result.items():
        values.append(val)
    return render_template("Hpdata.html",values=values,uname=uname)

# patient appoinments
@app.route("/appointment/<uname>/")
def appointment(uname):
    result = db.child("Users").child(str(uname)).get().val()["Appointments"]
    values = []
    for _,val in result.items():
        values.append(val)
    return render_template("appointment.html",uname=uname,values=values)

# patient Medicines
@app.route("/Medicines/<uname>/")
def Medicines(uname):
    result = db.child("Users").child(str(uname)).get().val()["Medicines"]
    return render_template("Medicines.html",uname=uname,values=result["12345678"])

# patient near hospital
@app.route("/near_hospitals/<uname>/")
def near_hospitals(uname):
    result = db.child("Hospitals").get().val()
    return render_template("NHospitals.html",uname=uname,values=result)




@app.route("/chemist_login/")
def chemist_login():
    return render_template("chemist_login.html")

@app.route('/clogin_check/', methods=['POST'])
def clogin_check():
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
                return render_template("chemist_login.html")
            elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_PASSWORD':
                flash("Invalid  password , enter valid password")
                return render_template("chemist_login.html")
            else:
                flash("data Not Found")
                return render_template("index.html")
        Uids = db.child("UIds").child("UserID").get().val()
        User_id = Uids[email.split('@')[0]]
        flash(" Chemist Login Successfully ")
        return render_template("chemist_dashboard.html",uname=User_id)

@app.route("/chemist_dashboardd/<uname>/")
def chemist_desbd(uname):
    return render_template("chemist_dashboard.html",uname=uname)

@app.route("/chemist_scratch_data/<uname>/")
def chemist_scratch_data(uname):
    uid = str(client_program())
    # uid = "188320981535"
    result = db.child('Users').child(str(uid)).child("Reports").get().val()
    last_id = len(result)
    result = db.child('Users').child(str(uid)).child("Reports").child("Id"+str(last_id)).get().val()
    print(result)
    return render_template("camist_card.html",Data=result,uname=uname)




@app.route("/pathologist_login/")
def pathologist_login():
    return render_template("pathologist_login.html")

@app.route("/pathologist_login_check/", methods=['POST'])
def pathologist_login_check():
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
                return render_template("pathologist_login.html")
            elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_PASSWORD':
                flash("Invalid  password , enter valid password")
                return render_template("pathologist_login.html")
            else:
                flash("data Not Found")
                return render_template("index.html")
        Uids = db.child("UIds").child("UserID").get().val()
        User_id = Uids[email.split('@')[0]]
        flash(" pathologist Login Successfully ")
        return render_template("pathologist_dashboard.html",uname=User_id)

@app.route("/Upload_lab_report/", methods=['POST'])
def Upload_lab_report():
    f = request.files['file']
    pid = request.form['PID']
    print(pid)
    result = db.child("Users").child(pid).child("Reports").get().val()
    last_id = len(result)
    result = db.child("Users").child(pid).child("Reports").child("Id"+str(last_id)).get().val()

    storage.child("Prescription/{}/Id{}/User2.jpg".format(pid,last_id)).put(f)
    # storage.child("Prescription/usersid/reportid/User1.jpg").put(f)
    flash("Data Updated")
    return render_template("pathologist_dashboard.html")


@app.route("/data_visualization/")
def data_visualization():
    return render_template("data_visulization.html")


@app.route("/temp/", methods=['POST'])
def temp():
    data1 = request.form['name1']
    data2 = request.form['mail1']
    data3 = request.form['name2']
    data4 = request.form['mail2']
    print(data1,data2)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234,debug=True)

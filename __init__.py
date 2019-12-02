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
    MYSQL_DB='smartcard'
)
app.secret_key = 'vatsalparsaniya'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    # cur = mysql.connection.cursor()
    # cur.execute("CREATE TABLE sys.doctor(USER varchar(30),EMAIL varchar(35),PASSWORD varchar(30));")
    # cur.execute("INSERT INTO sys.doctor VALUES (\"meet\",\"Darshit@gmail.com\",\"12345678\");")
    # cur.execute("SELECT EMAIL FROM sql12308164.authorization;")
    # rv = cur.fetchall()
    # print(rv)
    # mysql.connection.commit()
    # cur.close()
    return render_template("index.html")

@app.route("/doctor_login/")
def doctor_login():
    return render_template("doctor_login.html")

@app.route('/dlogin_check/', methods=['POST'])
def dlogin_check():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EMAIL,PASSWORD FROM sys.doctor;")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if (email,password) in data:
            flash("Loged in Successfully")
            cur = mysql.connection.cursor()
            cur.execute("SELECT USER FROM sys.doctor WHERE EMAIL=\'"+email+"\';")
            uname = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template("doctor_dashboard.html",uname=uname[0][0])
        else:
            flash("Wrong!! Email or Password")
            return redirect(url_for("doctor_login"))

@app.route("/patient_login/")
def patient_login():
    return render_template("patient_login.html")

@app.route('/plogin_check/', methods=['POST'])
def plogin_check():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EMAIL,PASSWORD FROM sys.patient;")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if (email,password) in data:
            flash("Loged in Successfully")
            cur = mysql.connection.cursor()
            cur.execute("SELECT USER FROM sys.patient WHERE EMAIL=\'"+email+"\';")
            uname = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template("patient_dashboard.html",uname=uname[0][0])
        else:
            flash("Wrong!! Email or Password")
            return redirect(url_for("patient_login"))


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
            cur.execute("SELECT USER FROM sys.chemist WHERE EMAIL=\'"+email+"\';")
            uname = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template("chemist_dashboard.html",uname=uname[0][0])
        else:
            flash("Wrong!! Email or Password")
            return redirect(url_for("chemist_login"))


@app.route("/signup_page/")
def signup():
    return render_template("Signup.html")

@app.route("/Search_card_no/<user>")
def Search_card_no(user):
    # render_template("get_card_details.html",uname=user)
    # get user card Data
    host = '192.168.60.47' # as both code is running on same pc
    port = 5005 # socket server port number

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = client_socket.recv(1024)  # receive response
    rdata=pickle.loads(data)
    # print(rdata)  # show in terminal
    # mdata = str(rdata)
    client_socket.close()  
    # mdata = client_program(mdata)
    # print(mdata)
    # card_number = 188320981535
    # card_number = 12
    # time.sleep(2)
    print(rdata)
    cur = mysql.connection.cursor()
    # cur.execute("SELECT USER FROM sys.chemist WHERE EMAIL=\'"+email+"\';")
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
        # uname1 = str("Tanmeet")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sys.p_medical_visits WHERE DOCTOR='"+str(uname)+"';")
        first = cur.fetchall()
        print(first)
        # cur.execute("SELECT * FROM sys.p_medical_visits WHERE DOCTOR='Tanmeet';")
        mysql.connection.commit()
        cur.close()
        return render_template("doctor_past_patient.html",uname=uname,Data=first)

@app.route("/doctor_deshboard/<uname>/")
def lelele(uname):
    return render_template("doctor_dashboard.html",uname=uname)

@app.route("/Pdetail/<uname>/")
def Pdetail(uname):
    cur = mysql.connection.cursor()
    cur.execute("SELECT CARDNO FROM sys.patient WHERE USER = '"+uname+"';")
    first = cur.fetchall()[0][0]
    cur.execute("SELECT * FROM sys.basic_details WHERE CARDNUMBER='"+str(first)+"';")
    second = cur.fetchall()
    print(second)
    mysql.connection.commit()
    cur.close()
    return render_template("PP_data.html",uname=uname,Data=second)

@app.route("/patient_dashboardd/<uname>/")
def patient_dashboardd(uname):
    return render_template("patient_dashboard.html",uname=uname)

@app.route("/chemist_scratch_data/<uname>/")
def chemist_scratch_data(uname):
    host = '192.168.60.47' # as both code is running on same pc
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
    return render_template("camist_card.html",Data=first)

@app.route("/chemist_deshboardd/<uname>/")
def chemist_dashboardd(uname):
    return render_template("chemist_deshboard.html",uname=uname)

@app.route("/Mhistory/<uname>/")
def Mhistory(uname):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sys.p_medical_visits;")
    first = cur.fetchall()
    print(first)
    # cur.execute("SELECT * FROM sys.p_medical_visits WHERE DOCTOR='Tanmeet';")
    mysql.connection.commit()
    cur.close()
    return render_template("Hdata.html",Data=first)

@app.route("/chemist_dashboardd/<uname>/")
def chemist_desbd(uname):
    return render_template("chemist_dashboard.html",uname=uname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234,debug=True)

import json
from optparse import Values

import pyrebase
from decorator import append

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

set_Appointments_data = {"Checkup":"Therapy","Data":"25/02/2020","Doctor":"Dr. V.P.Parsaniya","Hospital":"Iscon Hospital"}

db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


# # Doctor id 
# doctor_id = db.child("Users").get().val()
# # print(doctor_id["123456789012"])
# for Key , value in doctor_id.items():
#   print(Key)


# print(doctor_id["321321321321"])

# try:
#   email = "Vatsalparsaniya@gmail.com"
#   password = "12345678"
#   id_number = 123456789012
#   data = {"Vatsalparsaniya" : 123456789012}
#   results = db.child("UIds").set(data)
#   user = auth.create_user_with_email_and_password(email,password)
#   # auth.send_email_verification(user['idToken'])

# except Exception as e:
#   print(e.args[-1])
#   if json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'EMAIL_EXISTS':
#     print("Email ID is already Exists")
#     print("Move to the login page")
#   elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_EMAIL':
#     print("Email ID is Invalid")
#     print("rander this page again")
#   else:
#     print("Something Went Wrong")
#     print("Go to the signup page")
  
# try:
#   email = "Vatsalparsaniya@gmail.com"
#   password  = "12345678"
#   idnumber = "123456789012"
#   user = auth.sign_in_with_email_and_password(email, password)
#   Uids = db.child("UIds").get().val()
#   print("UIDS : ",Uids[email.split('@')[0]])
# except Exception as e:
#   print("Error : ")
#   print(e.args[-1])
#   if json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'EMAIL_NOT_FOUND':
#     print("Email ID not Found , Enter Valid Email")
#   elif json.loads(e.args[-1])["error"]["errors"][0]["message"] == 'INVALID_PASSWORD':
#     print("Invalid  password , enter valid password")
  
  
# doctor_id = db.child("Doctors").get().val()
# print(doctor_id["123456789012"])

# Add data
# rasult = db.child("Users").child("UserId1").child("Appointments").child("Id4").set(set_Appointments_data)
# result = db.child("UIds").child("UserID").get().val()
# result["vatsal12"] = "123432123421"
# result = db.child("UIds").child("UserID").set(result)
# print(result)

# doctor_id = db.child("Doctors").get().val()
# print(doctor_id["123456789012"]["Name"])

# if "123456789012" in doctor_id:
#   print("Yes")
# else:
#   print("No")
# get data
# data = db.child("Users").get().val()
# print(data.val())
# print(data["UserId1"]["Appointments"]["Id2"]["Checkup"])

# upload Image
# storage.child("Reports/usersid/reportid/User1.jpg").put("Extra_Code/backgroung_index.jpg")
# storage.child("Prescription/usersid/reportid/User1.jpg").put("Extra_Code/background_index.jpg")



# Pdetails
# result = db.child("Users").child("121234567890").get().val()
# print(result["Details"])

# result = db.child("Hospitals").get().val()

# print(result)

# from datetime import datetime
# datetime.today().strftime('%d-%m-%Y')


# result =  db.child("Users").child("188320981535").child("Details").get().val()["Name"]
# print(result)
# keys = []
# value = []
# for key , val  in result.items():
#   keys.append(key)
#   value.append(val)
# length = len(value)
# next_id = length+1
# next_id = "Id"+str(next_id)
# print("nextID",next_id)

# db.child("Users").child("188320981535").child("Reports").child("Id3").set({"Date":"10/12/2020","Doctor":"vatsal pp"})
# result = storage.child("Prescription/{}/reportid/User2.jpg".format("188320981535")).put("static/img/1.jpg")
# print(result)
# url = storage.child("Prescription/188320981535/reportid/User1.jpg").get_url(1)
# print(url)

# result = db.child("Doctors").child(121234567890).child("PastRecords").get().val()
# print(len(result))

result = db.child('Users').child("188320981535").child("Reports").child("Id"+str(3)).get().val()["PrescriptionUrl"]
print(result)
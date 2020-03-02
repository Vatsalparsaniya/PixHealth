from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

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

def get_img(doc_name,pat_name,Meds,Quantity,Dosage,pid):
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

    pattern.save("static/img/1.jpg")
    return pattern

imggg = get_img("Vatsal","Darshit",["Paracetamol","Chlorofine"],["20","30"],["1-1-1","1-0-1"],"123456789098")

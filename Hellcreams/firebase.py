import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred_object = credentials.Certificate('./capstonetest-d81da-firebase-adminsdk-64uiw-ba419847e3.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': "https://capstonetest-d81da-default-rtdb.firebaseio.com"
})
ref = db.reference("users")
ref.update({
    "phew":
        {"email": "qery@phew.com",
         "id": "seki",
         "password": "alali"}
})

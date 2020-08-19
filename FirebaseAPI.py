from firebase import firebase
import CREDENTIALS

firebase = firebase.FirebaseApplication(CREDENTIALS.GOOGLE_FIREBASE, None)

def insert(data):
    #data =  { 'Name': 'John Doe',
    #          'RollNo': 3,
    #          'Percentage': 70.02
    #          }

    for x in data:
        result = firebase.post(CREDENTIALS.GOOGLE_FIREBASE_TABLE,x)
        #print(result)
    print("Inserted data.")


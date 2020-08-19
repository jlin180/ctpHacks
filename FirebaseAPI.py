from firebase import firebase
import CREDENTIALS

firebase = firebase.FirebaseApplication(CREDENTIALS.GOOGLE_FIREBASE, None)

def insert(data):
    #data =  { 'Name': 'John Doe',
    #          'RollNo': 3,
    #          'Percentage': 70.02
    #          }
    result = firebase.post(CREDENTIALS.GOOGLE_FIREBASE_TABLE,data)
    #print(result)
    print("done!")


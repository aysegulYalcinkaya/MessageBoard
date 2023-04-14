import mysql.connector
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer=joblib.load("vectorizer.joblib")
classifier_model = joblib.load("spam_classifier.joblib")

def connect():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="message_board"
    )
    return mydb

while True:
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM trigger_table")
    myresult = mycursor.fetchall()
    mydb.close()
    if len(myresult)>0:
        print("NEW MESSAGE ARRIVED")
        for row in myresult:
            id=row[0]
            mydb=connect()
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM tb_mail where id=%s',(id,))
            mail=mycursor.fetchone()
            mycursor.execute("DELETE FROM trigger_table")
            message_text=mail[2]
            mydb.close()
            integers = vectorizer.transform([message_text])
            x = classifier_model.predict(integers)
            if x==1:
                print(message_text, "==>", " SPAM!!!!")
            else:
                print(message_text, "==>", " NOT SPAM :)")
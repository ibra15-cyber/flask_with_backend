from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy import func


app=Flask(__name__) #creating our app so our app name
#our app connected to a database postgres database locally through sql alchemy
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:'enterpassword'@localhost/height_collector'
#using the postgre url on heroku
app.config['SQLALCHEMY_DATABASE_URI']='DATABASE_URL: postgres://nmianmplbaqnkn:bf436ad0145bb8cea80914d8b758d46a16b7b3e57931501f1e2a67c074e99fc4@ec2-34-206-148-196.compute-1.amazonaws.com:5432/dfac3jc3khglm7?sslmode=require'
#making an obj of our dabase through SQLAlchemy
db=SQLAlchemy(app)
 
#we created a class that we pass our database 
class Data(db.Model):
    #class variables
    __tablename__='data' 
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True)
    height=db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height= height



@app.route("/")
def index():
    return render_template("index.html")

#on pressing the submit call the success method
#so the success method that will render the success notification 
#will also handle sending the data to database
@app.route("/success", methods=['POST'])
def success():
    if request.method =='POST':
        email = request.form['email_name'] #get the input in form field
        height = request.form['height_name'] #get the input in form field
        
        #if the email entered is already in the db table return the index page with a notification else continue
        if db.session.query(Data).filter(Data.email==email).count()== 0: #we use count to confirm if the same email is entered twice 0 is no 1 is yes
            data=Data(email, height) #passing to our class which passes it to column in our db
            db.session.add(data) #creating a session to pass data each time
            db.session.commit() #then commiting 

            #after submiting count average
            average_height=db.session.query(func.avg(Data.height)).scalar()
            average_height=round(average_height, 1)
            
            #count
            count = db.session.query(Data.height).count()
            #calling our script send_email that has a method send_email to handle
            try: 
                send_email(email,height,average_height,count)
            except:
                print(None)
            return render_template("success.html") #we rendering the static part of our site while sending data to the db
    #if the db session isnt new ie 0 render the same page with a text
    return render_template("index.html", text="You have entered the same email before") #return the same page otherwise with a text. then we grab the text in the html


if __name__ == '__main__':
    app.debug=True
    app.run()


from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email


app=Flask(__name__) #creating our app so our app name
#our app connected to a database postgres database locally through sql alchemy
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:nyars150@localhost/height_collector'
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
        #calling our script send_email that has a method send_email to handle emailing
        try: 
            send_email(email,height)
        except:
            print(None)
        #if the email is already in the table return the index page with a notification
        if db.session.query(Data).filter(Data.email==email).count()== 0: #we use count to confirm if the same email is entered twice 0 is no 1 is yes
            data=Data(email, height) #passing to our class which passes it to column in our db
            db.session.add(data) #creating a session to pass data each time
            db.session.commit() #then commiting 
            return render_template("success.html") #we rendering the static part of our site while sending data to the db
    #if the db session isnt new ie 0 render the same page with a text
    return render_template("index.html", text="You have entered the same email before") #return the same page otherwise with a text. then we grab the text in the html


if __name__ == '__main__':
    app.debug=True
    app.run()


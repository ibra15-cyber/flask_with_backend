from email.mime.text import MIMEText
from email import message
import smtplib, ssl

#we are creating a method that will wrap our emailing from my email account
#to any one's that entered their height
#our fn takes the fellows email and height
def send_email(email, height): 
    from_email="nyars15@gmail.com" #my email that will do the sending
    from_passwd="who?WHAT?why?.@gmaa"
    to_email=email                  #the email to send msg to

    subject="Height data"           #subject
    message="Hey there, your height is <strong>%s</strong>." %height #the message

    msg=MIMEText(message, "html") #creating a Message, MIMEText obj
    msg["Subject"] = subject #adding a subject
    msg["To"] = to_email    #adding a to field that will contain the email to send to 
    msg["From"] = from_email #addding the from field that will contain my email

    gmail=smtplib.SMTP('smtp.gmail.com', port=587) #linking up my Mimetext with google servers bc my email is google
    gmail.ehlo
    gmail.starttls(context=ssl.create_default_context()) #this solved the error
    gmail.login(from_email, from_passwd) #login with my email
    gmail.send_message(msg) #gmail server should invoke send_message method with the content of the MIMEText
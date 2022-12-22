from email.mime.text import MIMEText
from email import message
import smtplib, ssl

#we are creating a method that will wrap our emailing from my email account
#to any one's that entered their height
#our fn takes the fellows email and height
def send_email(email, height, average_height, count): 
    from_email="your email" #my email that will do the sending
    from_passwd="your password"
    to_email=email                  #the email to send msg to

    subject="Height data"           #subject
    message="Hey there, your height is <strong>%s</strong>.<br> The average height is <strong>%s</strong>, out of <strong>%s</strong> people.<br> Thanks!" %(height, average_height, count) #the message

    #message body and format
    msg=MIMEText(message, "html") #creating a Message, MIMEText obj
    msg["Subject"] = subject #adding a subject
    msg["To"] = to_email    #adding a to field that will contain the email to send to 
    msg["From"] = from_email #addding the from field that will contain my email

    #gmail server
    server=smtplib.SMTP('smtp.gmail.com', port=587) #linking up my Mimetext with google servers bc my email is google
    server.ehlo
    server.starttls(context=ssl.create_default_context()) #this solved the error
    server.login(from_email, from_passwd) #login with my email
    server.send_message(msg) #gmail server should invoke send_message method with the content of the MIMEText

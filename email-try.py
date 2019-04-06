# Python code to illustrate Sending mail with attachments 
# from your Gmail account 

# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import configparser
import logging

logging.basicConfig(filename='email.log', level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
config = configparser.ConfigParser()
config.read('cred.ini')
FROM = config.get('Login','from')
TO = config.get('Login','to')
PASSWORD = config.get('Login','password')
SUBJECT = config.get('Login','subject')
BODY = config.get('Login','body')
FILE = config.get('Login','file')
filename= FILE
# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = FROM 

# storing the receivers email address 
msg['To'] = TO 

# storing the subject 
msg['Subject'] = SUBJECT

# string to store the body of the mail 
body = BODY

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
#filename = "File_name_with_extension"
filename = filename.split(';')
if filename is not None:
    for f in filename:
        attachment = open(f, "rb") 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % f) 
        msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(FROM, PASSWORD) 

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
s.sendmail(FROM, TO, text) 

# terminating the session 
s.quit() 
logging.info("email sent")

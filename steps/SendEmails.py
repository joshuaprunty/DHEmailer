import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmails():
    # Credentials
    sender_email = "nudiningupdates@gmail.com"
    sender_password = "lrqhulbaafhthacx"

    # Subject Line
    subject = "Today's Dining Hall Selections at NU."

    # Get User Data
    with open('/Users/joshprunty/Desktop/DHEmailer/data/users.json', 'r') as file:
        userData = json.load(file)

    # Get Messages Data
    with open('/Users/joshprunty/Desktop/DHEmailer/data/messages.json','r') as file:
        messages = json.load(file)

    # For all users:
    for user in userData:
        toSend = MIMEMultipart()
        toSend["From"] = sender_email
        toSend["To"] = user["email"]
        toSend["Subject"] = subject
        body = messages[user['email']]

        toSend.attach(MIMEText(body, "plain"))

        # Choose a mail server (e.g., Google's SMTP server)
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls

        # Create a secure SSL context
        context = smtplib.SMTP(smtp_server, port)
        receiver_email = user["email"]
        try:
            # Try to log in to server and send email
            context.ehlo()  # Can be omitted
            context.starttls()  # Secure the connection
            context.ehlo()  # Can be omitted
            context.login(sender_email, sender_password)
            context.sendmail(sender_email, receiver_email, toSend.as_string())
            print("Email sent successfully!")
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            context.quit()

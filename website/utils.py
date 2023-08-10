import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration

def trigger_email():
    sender_email = 'sagarsinghchauhan49@gmail.com'
    receiver_email = 'sagarsinghchauhan49@gmail.com'
    subject = 'Registration Successfull'
    message = 'registration ID : IYT1231TEST'

    # Gmail SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'sagarsinghchauhan49@gmail.com'
    password = 'xfzjaqtmjtzcwlqi'

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Create a secure SSL/TLS connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # Log in to the Gmail account
        server.login(username, password)
        # Send the email
        server.send_message(msg)

    print('Email sent successfully!')
    
def trigger_error_email(msg):
    sender_email = 'sagarsinghchauhan49@gmail.com'
    receiver_email = 'sagarsinghchauhan49@gmail.com'
    subject = 'Registration Successfull'

    # Gmail SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'sagarsinghchauhan49@gmail.com'
    password = 'xfzjaqtmjtzcwlqi'

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(msg, 'plain'))

    # Create a secure SSL/TLS connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # Log in to the Gmail account
        server.login(username, password)
        # Send the email
        server.send_message(msg)

    print('Email sent successfully!')
    
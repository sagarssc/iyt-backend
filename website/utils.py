import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration

def trigger_email(registration_number, name, email, phone_number):
    trigger_customer_email(registration_number, name, email, phone_number)
    trigger_service_email(registration_number, name, email, phone_number)

def trigger_service_email(registration_number, name, email, phone_number):
    sender_email = 'sagarsinghchauhan49@gmail.com'
    receiver_email = 'alfacode.ai@gmail.com'
    subject = 'New Booking'
    message = '''Hi,
    New user registered.
    User Details:
    name:  {}
    email: {}
    phone_number: {}
    registration_number: {}'''.format(name, email, phone_number, registration_number)

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
def trigger_customer_email(registration_number, name, email, phone_number):
    sender_email = 'sagarsinghchauhan49@gmail.com'
    receiver_email = email
    subject = 'Registration Successfull'
    message = '''Hi {},
    your registration is completed for IYT teacher training course your registration no is {}.'''.format(name, registration_number)

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
    
def trigger_error_email(message):
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
    msg.attach(MIMEText(message, 'plain'))

    # Create a secure SSL/TLS connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # Log in to the Gmail account
        server.login(username, password)
        # Send the email
        server.send_message(msg)

    print('Email sent successfully!')
    
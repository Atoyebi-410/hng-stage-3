from flask import Flask, request
from celery import Celery
import logging
from datetime import datetime

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Setup logging
logging.basicConfig(filename='messaging_system.log', level=logging.INFO)

@celery.task
def send_email(recipient):
    import smtplib
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('your-email@example.com', 'your-password')
    message = f'Subject: Hello\n\nThis is a test email to {recipient}.'
    server.sendmail('your-email@example.com', recipient, message)
    server.quit()

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return f'Email has been queued to {sendmail}'

    if talktome:
        logging.info(f'Current time logged: {datetime.now()}')
        return 'Current time has been logged'

    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

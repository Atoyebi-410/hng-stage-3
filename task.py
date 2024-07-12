from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_email(recipient):
    import smtplib
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('your-email@example.com', 'your-password')
    message = f'Subject: Hello\n\nThis is a test email to {recipient}.'
    server.sendmail('your-email@example.com', recipient, message)
    server.quit()

from django.core.mail import EmailMessage
email = EmailMessage('Hello World', 'Some body text', to=['pl@live.unc.edu'])
email.send()
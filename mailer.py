from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send(login_id, password, to, subject = None, body = None):
	msg = MIMEMultipart()
	htmlBody = MIMEText(body, 'html')

	msg.attach(htmlBody)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()

	msg['From'] = login_id
	msg['To'] = to
	msg['Subject'] = subject

	server.login(msg['From'], password)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()

	print(msg.as_string())

class Mailer(object):
	def __init__(self, login_id, password):
		self.login_id = login_id
		self.password = password

	def sendMail(self, to, subject = None, body = None):
		msg = MIMEMultipart()
		htmlBody = MIMEText(body, 'html')

		msg.attach(htmlBody)
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()

		msg['From'] = self.login_id
		msg['To'] = to
		msg['Subject'] = subject

		server.login(self.login_id, self.password)
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()

		print(msg.as_string()) 

	def sendRegistrationMail(self, to, temp_password):
		subject = "Confirm Registration"
		body = 'Welcome, '
		body += '''
		<br>
			Your temporary password is %s<br>
			Change your password after logging in through the profile page
		'''%temp_password

		self.sendMail(to, subject = subject, body = body)

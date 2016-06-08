#!/usr/bin/python
import smtplib
import string
class email(object):
	def __init__(self):
		self.HOST = "smtp.gmail.com"
		self.SUBJECT = "Test email from Python"
		self.TO = "ruikang.dai@me.com"
		self.FROM = "aucue1@gmail.com"
		self.PASSWORD = "Wosangle123456"
		self.CONTENT = "Python rules them all!"
		self.BODY = ""
	def compose(self, FROM, TO, SUBJECT, CONTENT):
		self.BODY = string.join((
			"From: %s" % FROM,
			"To: %s" % TO,
			"Subject: %s" % SUBJECT,
			"",
			CONTENT
			), "\r\n")
	def setHost(self, HOST):
		self.HOST = HOST
	def setSender(self, FROM, PASSWORD):
		self.FROM = FROM
		self.PASSWORD = PASSWORD
	def setContent(self, SUBJECT, CONTENT):
		self.SUBJECT = SUBJECT
		self.CONTENT = CONTENT
	def setReceiver(self, TO):
		self.TO = TO
	def send(self):
		self.compose(self.FROM, self.TO, self.SUBJECT, self.CONTENT)
		try:
			server = smtplib.SMTP_SSL(self.HOST,"465")
			server.ehlo()
			server.login(self.FROM, self.PASSWORD)
			server.sendmail(self.FROM, [self.TO, 'aucue0@gmail.com'], self.BODY)
			server.close()
			print "sent!"
		except:
			print "failed to send mail"

if __name__ == '__main__':
	e = email()
	e.send()

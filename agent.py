#!/usr/bin/python

import smtplib
import sys
import getpass
import imaplib
import email
import os
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



def get_input(prompt):
	result = raw_input(prompt)
	return result

def connect_smtp(login, password):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(login, password)
	return server

def connect_imap(login, password):
	imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
	imap_server.login(login, password)
	imap_server.list()
	imap_server.select("inbox")
	return imap_server

def send_message(server, login, to, text):
	server.sendmail(login, to, text)
	server.quit()
	print("Message sent to <%s>" % to)
	time.sleep(1)

def create_message(login):
    to = get_input("Enter recipient e-mail address: ")
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = to
    msg['Subject'] = get_input("Enter message subject: ")
    body = get_input("Enter message text: ")
    msg.attach(MIMEText(body, 'plain'))
    return msg

def print_message(email_message):
	print("To: %s" % email_message['To'])
	print("From: %s" % email_message['From'])
	print("Subject: %s" % email_message['Subject'])

	maintype = email_message.get_content_maintype()
	if maintype == "multipart":
		for part in email_message.get_payload():
			if part.get_content_maintype() == 'text':
				print("\nBody: \n%s" % part.get_payload())

def get_message(imap_server):
	result, data = imap_server.uid('search', None, "ALL")
	latest_email_uid = data[0].split()[-1]
	result, data = imap_server.uid('fetch', latest_email_uid, '(RFC822)')
	raw_email = data[0][1]
	email_message = email.message_from_string(raw_email)
	return email_message

os.system('clear')
print("Conecting to server...\n")
login = get_input("Enter your e-mail address (gmail only): ")
password = getpass.getpass()

while 42:
	os.system('clear')
	user_input = get_input("Enter <send> for sending email\nEnter <check> for checking your inbox\nEnter <exit> for exit:\n")
	if user_input == "send":
		smtp_server = connect_smtp(login, password)
		connect_smtp(login, password)
		msg = create_message(login)
		send_message(smtp_server, login, msg['To'], msg.as_string())
	elif user_input == "check":
		imap_server = connect_imap(login, password)
		email_message = get_message(imap_server)
		print_message(email_message)
		mes = get_input("\n\nContinue ? y/n: ")
		if mes == 'n':
			break ;
	elif user_input == "exit":
		break ;
	else:
		print("Invalid command")
		time.sleep(1)

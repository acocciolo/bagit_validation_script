# Bag validation script
#
# For a given directory, validates all BagIt bags in the directory.
# It sends an email to you letting you know the results of the validation.
# Note that all sub-folders in the directory should be bags (non-bags
# will generate a validation error).  
# Note that by default, the message is setup to come from Gmail, however,
# you can change this for any outgoing SMTP server.
#
# Written by Anthony Cocciolo for Bard Graduate Center, 2016

import os, sys, bagit
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# parameteres that should be updated
start_path = "e:\\bard"    # Path to Archives share - should be all bags
email_address = "TO_EMAIL_ADDRESS"  # recipient of email result
from_email_address = "FROM_GMAIL_ADDRESS"    # from email address
outgoing_mail_server = "smtp.gmail.com"
outgoing_mail_port = 587
outgoing_smtp_password = "FROM_GMAIL_PASSWORD"


# nothing below here should need to be updated

# initialize variables 
valid = 0
invalid = 0
total = 0
ind_bags = ""
body = ""

# get list of directories
directories=[d for d in os.listdir(start_path) if os.path.isdir(d)]

# loop through directories and check bags
for dir in directories:
	bag = bagit.Bag(start_path + '\\' + dir)
	
	if bag.is_valid():
		ind_bags = ind_bags + dir + " is valid.\n"
		valid = valid + 1
	else:
		ind_bags = ind_bags + dir + " is NOT A VALID BAG.\n"
		invalid = invalid + 1
	total = total + 1
	
# prepare email message
body = str(total) + " directories checked containing \n" + str(valid) + " valid bag(s)\n" + str(invalid) + " invalid bag(s)."
body = body + "\n\nSpecific results include:\n" + ind_bags

if invalid > 0:
	body = body + "\n\nPlease run bagger immediately on the invalid bag(s) to find the specific problems with the bag."
	subject = "ARCHIVES FIXITY ERROR: " + str(invalid) + " invalid bag(s)"
else:
	subject = "Digital Archives Validation: " + str(total) + " bag(s) intact"
	
# send email message
msg = MIMEMultipart()
msg['From'] = from_email_address
msg['To'] = email_address
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP(outgoing_mail_server, outgoing_mail_port)
server.starttls()
server.login(from_email_address, outgoing_smtp_password)
text = msg.as_string()
server.sendmail(from_email_address, email_address, text)
server.quit()

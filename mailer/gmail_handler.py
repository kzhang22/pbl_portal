import sender
import message
import gmail


def get_gmail_sender():
	gmailer = sender.GMail('berkeleypbl.webdev', 'dek19942012')
	gmailer.connect()
	return gmailer

def send_message(msg):
	gmailer = get_gmail_sender()
	gmailer.send(msg)

def get_mail():
	g = gmail.login('berkeleypbl.webdev', 'dek19942012')
	mail = g.inbox().mail(subject = 'Attendance Updates')
	return mail

send_message(message.Message(to = 'berkeleypbl.webdev@gmail.com', subject = 'Attendance Updates'))
check_inbox()
import smtplib
from xero_config import *

def email_admin(message):
    fromaddr = FROM_ADDR
    toaddrs = TO_ADDRS
    msg = "\r\n".join([
        "From: GFSA",
        "To: Admin",
        "Subject: [GFSA] GFSA Notification",
        "",
        message
    ])
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USERNAME,EMAIL_PASSWORD)
        server.sendmail(fromaddr, toaddrs, msg)
        server.close()
        print "Successfully sent email"
        return True
    except:
        print "Failed to send email"
        return False

def email_anyone(to_email, message):
    fromaddr = FROM_ADDR
    toaddrs = [to_email]
    msg = "\r\n".join([
        "From: GFSA",
        "To: Member",
        "Subject: [GFSA] GFSA Notification",
        "",
        message
    ])
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USERNAME,EMAIL_PASSWORD)
        server.sendmail(fromaddr, toaddrs, msg)
        server.close()
        print "Successfully sent email"
        return True
    except:
        print "Failed to send email"
        return False

def send_SMS(mobile, message):
    #email_address = mobile + '@' + SMS_SERVER
    #return email_anyone(email_address, message)
    return False
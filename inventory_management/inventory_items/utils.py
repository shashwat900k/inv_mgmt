from django.core.mail import send_mail
from django.core import signing

def sendactivationemail(user_id, username, user_email):
    signer = signing.dumps({'user_info': user_id})
    url_link = 'http://localhost:8080/inventory/email_activation/'+signer
    subject = "BC Inventory Management: Email Activation"
    from_email = "shashwat@beautifulcode.in"
    to_email = [user_email]
    text_content = "Hey {}, thanks for registering on the Beautiful Code Inventory Management. Plase click on the below link to complete the registration process".format(username)
    html_content = '<html><body><a href='+url_link+'>Click here</a></body></html>'
    send_mail(subject=subject, message=text_content, from_email=from_email, recipient_list=to_email, html_message=html_content)

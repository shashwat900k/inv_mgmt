from django.core.mail import send_mail

def sendactivationemail(user_id, username, user_email):
    subject = "BC Invemtory Management: Email Activation"
    from_email = "shashwat@beautifulcode.in"
    to_email = [user_email]
    text_content = "Hey {}, thanks for registering on the Beautiful Code Inventory Management. Plase click on the below link to complete the registration process".format(username)
    html_content = '<html><body><a href="http://localhost:8080/inventory/email_activation/'+str(user_id)+'">Click here</a></body></html>'
    send_mail(subject=subject, message=text_content, from_email=from_email, recipient_list=to_email, html_message=html_content)

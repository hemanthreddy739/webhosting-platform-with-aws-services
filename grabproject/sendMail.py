from .getIhsUserDetails import getIhsUserDetails
from django.conf import settings
from django.core.mail import send_mail

def sendmail(code, server_ip):
    userdetails = getIhsUserDetails(code)
   
    userFullname = userdetails.get('name')
    userEmail = userdetails.get('email') 

    if userEmail:
        # send mail

        subject = 'Your web server credentials'
        message = f"""

                Hey! {userFullname} hope you are fine. 
                This mail is from 'IHS' Platform, your website is launched successfully
                in the IHS 'webserver'.
                we are providing your webserver credentials, so if you
                want to custamize your webserver you can.

                webserver credentials:-
                -------------------------
                server_ip :- {server_ip}
                username:- your-user-name
                password:- password-you-want-to-set-for-user

                please don't share this email, to protect your server.

                Thanks you from the team "IHS"
                
            """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [userEmail],
            fail_silently=False
        )

        print('mail sent to the registerd-user mail successfully.')
from email.message import EmailMessage
import ssl
import smtplib
import secrets


email_sender = "threadvortexinc@gmail.com"
email_password = "nbip ovsv ielo zvie"

def send_conformation_mail(email_receiver):
    """
    Send a conformation mail to the provided mail.

    Args:
        email_receiver (str): The email to send the conformation mail to.

    Returns:
        str | None: The confirmation_code sent to the email address (randomly generated and URL safe). If the mail isn't in the affirmative format then return None.
    """

    
    # generate 8 chars code    
    confirmation_code = secrets.token_urlsafe(8)
    
    subject = "Confirmation mail"
    body = f"""
Hello, this is the confirmation mail from Thread Vortex.
Your code is: 
    
----------------
{confirmation_code}
----------------
    
Thanks for usings our servers, we hope you enjoy your time!
"""
    try:
        # set up the EmailMessage object and define the message's attributes
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)
        
        context = ssl.create_default_context()
        
        # send the message to the provided mail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        return confirmation_code
    except smtplib.SMTPRecipientsRefused:
        return None
    
if __name__ == "__main__":
    send_conformation_mail("altermeinego@gmail.com")
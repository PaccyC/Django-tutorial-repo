from django.core.mail import send_mail,mail_admins,BadHeaderError
# Create your views here.

    
def say_hello(request):
    try:
        send_mail('subject','message','pacifique@gmail.com',['elite@gmail.com'])
    except BadHeaderError:
        pass
            

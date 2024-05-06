from django.core.mail import send_mail,mail_admins,EmailMessage,BadHeaderError
from rest_framework.response import Response
from django.shortcuts import render
# Create your views here.

    
def say_hello(request):
    try:
        # send_mail('subject','message','pacifique@gmail.com',['elite@gmail.com'])
        # mail_admins("subjct here","message here",html_message='message')
        message=EmailMessage("subject here","Body of the message",'paccy@gmail.com',['elite@gmail.com'])
        message.attach_file('playground/static/images/cat.jpg')
        message.send()
    except BadHeaderError:
        pass
    
    return render(request,'hello.html',{'name':'Paccy'})
            

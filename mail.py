from django.core.mail import send_mail

send_mail(
    "hello",
    "email send testing",
    "nandhakumarp764@gmail.com",
    ["6.11nandhakumar2002@gmail.com"],
    fail_silently=False,
)
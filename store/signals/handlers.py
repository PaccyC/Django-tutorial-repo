from django.conf import settings
from store.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save




# Signal handler
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_for_user(sender,**kwargs):
    
    if kwargs["created"]:
        Customer.objects.create(user=kwargs["instance"])
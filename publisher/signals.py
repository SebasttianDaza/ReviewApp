from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from publisher.messages.queue_message import QueueMessagePublisher


@receiver(post_save, sender=Review)
def review_post_action(sender, instance, created, **kwargs):
    print(sender, created)
    message = QueueMessagePublisher()
    message.add_message("new review created")
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Image, Video
from publisher.queue_message import QueueMessagePublisher


@receiver(post_save, sender=Review)
@receiver(post_save, sender=Image)
@receiver(post_save, sender=Video)
def review_post_action(sender, instance, created, **kwargs):
    message = QueueMessagePublisher()
    review = {
        "id": instance.id,
        "title": instance.title,
        "table_name": sender._meta.db_table
    }
    if created:
        review.update({
            "type": "create",
        })
    else:
        review.update({
            "type": "update",
        })
    import json
    message.add_message(json.dumps(review))
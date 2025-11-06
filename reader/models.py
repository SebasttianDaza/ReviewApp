import datetime
from mongoengine import Document, StringField, DateTimeField


class ReaderReview(Document):
    title = StringField(max_length=100, required=True)
    subtitle = StringField(max_length=100, required=True)
    date_created = DateTimeField(required=True)
    date_updated = DateTimeField(required=True)

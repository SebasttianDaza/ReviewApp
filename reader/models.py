from mongoengine import Document, StringField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument, IntField
from .schemas.jsonapi import JSONAPIResource

class Video(EmbeddedDocument):
    title = StringField(max_length=100, required=True, null=False)
    description = StringField(max_length=300, required=True)
    source_id = StringField(max_length=100, required=True)
    source = StringField(max_length=100, required=True)

    def serialize_jsonapi(self):
        return JSONAPIResource(
            type="video",
            id="",
            attributes={
                "title": self.title,
                "description": self.description,
                "source": self.source,
                "source_id": self.source_id,
            },
            relationships={}
        )

class Image(EmbeddedDocument):
    title = StringField(max_length=100, required=True, null=False)
    path = StringField(max_length=100, required=True)

    def serialize_jsonapi(self):
        return JSONAPIResource(
            type="image",
            id="",
            attributes={
                "title": self.title,
                "path": self.path,
            },
            relationships={}
        )

class Len(EmbeddedDocument):
    model_name = StringField(max_length=100, required=True, null=False)
    version_name = StringField(max_length=100, required=True, null=False)
    description = StringField(max_length=300, required=True)
    max_resolution = IntField(null=False, required=True)
    sensor_size = IntField(null=False, required=True)
    effective_pixels = IntField(null=False, required=True)
    image = EmbeddedDocumentField(
        Image,
        required=True,
        default=False,
        null=False
    )
    video = EmbeddedDocumentField(
        Video,
        required=False,
        default=False,
        null=True
    )

    def serialize_jsonapi(self):
        return JSONAPIResource(
            type="len",
            id="",
            attributes={
                "model_name": self.model_name,
                "version_name": self.version_name,
                "description": self.description,
                "max_resolution": self.max_resolution,
                "sensor_size": self.sensor_size,
                "effective_pixels": self.effective_pixels,
            },
            relationships={}
        )

class Camera(EmbeddedDocument):
    model_name = StringField(max_length=100, required=True, null=False)
    version = StringField(max_length=100, required=True, null=False)
    max_resolution = IntField(null=False, required=True)
    sensor_size = IntField(null=False, required=True)
    effective_pixels = IntField(null=False, required=True)
    storage_types = StringField(max_length=100, null=False, required=True)
    screen_size = StringField(max_length=100, null=False, required=True)
    image = EmbeddedDocumentField(
        Image,
        required=False,
        default=False,
        null=True
    )
    video = EmbeddedDocumentField(
        Video,
        required=False,
        default=False,
        null=True
    )

class ReviewReader(Document):
    meta = {'collection': 'reader_review'}
    title = StringField(max_length=100, required=True)
    subtitle = StringField(max_length=100, required=True)
    body = StringField(max_length=1000, required=True)
    date_created = DateTimeField(required=True)
    date_updated = DateTimeField(required=True)
    video = EmbeddedDocumentField(
        Video,
        required=False,
        default=False,
        null=True
    )
    image = EmbeddedDocumentField(
        Image,
        required=False,
        default=False,
        null=True
    )
    len = EmbeddedDocumentField(
        Len,
        required=False,
        default=False,
        null=True
    )
    camera = EmbeddedDocumentField(
        Camera,
        required=False,
        default=False,
        null=True
    )

    def serialize_jsonapi(self):
        return JSONAPIResource(
            type="review",
            id=self.id,
            attributes={
                'title': self.title,
                'subtitle': self.subtitle,
                'body': self.body,
                'date_created': self.date_created,
                'date_updated': self.date_updated,
            },
            relationships={
                "image": {
                    "links": {},
                    "data": self.image.serialize_jsonapi(),
                } if self.image is not None else {},
                "video": {
                    "links": {},
                    "data": self.video.serialize_jsonapi(),
                } if self.video is not None else {},
                "len": {
                    "links": {},
                    "data": self.len.serialize_jsonapi(),
                } if self.len is not None else {},
            }
        )


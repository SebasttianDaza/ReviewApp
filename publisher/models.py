from django.db import models
from pyexpat import model


class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=50, null=False, unique=True)
    id_auth = models.CharField(max_length=100, null=False, unique=True)


class Images(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ManyToManyField(
        Author,
        on_delete=models.RESTRICT,
        null=False,
        db_table="author_images"
    )


class Videos(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField()
    source = models.CharField(max_length=10, null=False, choices={"YT": "YouTube"})
    credit = models.CharField(max_length=15, null=False)
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        db_comment="Date and time when the video was created"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=False,
        db_comment="Date and time when the video was updated"
    )
    author = models.ManyToManyField(
        Author,
        on_delete=models.RESTRICT,
        null=False,
        db_table="author_video"
    )


class Cameras(models.Model):
    model_name = models.CharField(max_length=100, null=False, unique=True)
    version = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=300, null=False)
    max_resolution = models.IntegerField(null=False)
    sensor_size = models.IntegerField(null=False)
    effective_pixels = models.IntegerField(null=False)
    storage_types = models.CharField(max_length=100, null=False)
    screen_size = models.CharField(max_length=100, null=False)
    # One to many
    image = models.ForeignKey(
        Images,
        on_delete=models.RESTRICT,
        null=True,
    )
    # One to many
    video = models.ForeignKey(
        Images,
        on_delete=models.RESTRICT,
        null=True,
    )
    # Many to many
    author = models.ManyToManyField(
        Author,
        on_delete=models.RESTRICT,
        null=False,
        db_table="cameras_authors"
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        db_comment="Date and time when the camera was created"
    )

    date_updated = models.DateTimeField(
        auto_now=True,
        null=False,
        db_comment="Date and time when the camera was updated"
    )


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100, null=False)
    subtitle = models.CharField(max_length=300, null=False)
    body = models.TextField(null=False)
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        db_comment="Date and time when the review was created"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=False,
        db_comment="Date and time when the review was updated"
    )
    author = models.ManyToManyField(
        Author,
        on_delete=models.RESTRICT,
        null=False,
        db_table="author_reviews"
    )
    # Many to one
    images = models.ForeignKey(
        Images,
        on_delete=models.SET_NULL,
        null=True
    )
    # Many to one
    videos = models.ForeignKey(
        Videos,
        on_delete=models.SET_NULL,
        null=True
    )

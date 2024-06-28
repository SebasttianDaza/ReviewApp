from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=50, null=False, unique=True)
    id_auth = models.CharField(max_length=100, null=False, unique=True)


class Image(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ManyToManyField(
        Author,
        db_table="publishers_images_authors"
    )


class Video(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField()
    source = models.CharField(max_length=10, null=False, choices={"YT": "YouTube"})
    credit = models.CharField(max_length=15, null=False)
    author = models.ManyToManyField(
        Author,
        db_table="publishers_videos_authors"
    )
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


class Len(models.Model):
    modelName = models.CharField(max_length=100, null=False, unique=True)
    versionName = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    maxResolution = models.IntegerField(null=False)
    sensorSize = models.IntegerField(null=False)
    effectivePixels = models.IntegerField(null=False)
    image = models.ForeignKey(
        Image,
        on_delete=models.RESTRICT,
        null=False,
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.RESTRICT,
        null=True
    )
    author = models.ManyToManyField(
        Author,
        db_table="publishers_lens_authors"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        db_comment="Date and time when the len was created"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=False,
        db_comment="Date and time when the len was updated"
    )


class Camera(models.Model):
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
        Image,
        on_delete=models.RESTRICT,
        null=True,
        related_name="%(app_label)s_%(class)s_related"
    )
    # One to many
    video = models.ForeignKey(
        Video,
        on_delete=models.RESTRICT,
        null=True,
    )
    # Many to many
    author = models.ManyToManyField(
        Author,
        db_table="publishers_cameras_authors"
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
    author = models.ManyToManyField(
        Author,
        db_table="publishers_reviews_authors"
    )
    # Many to one
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True
    )
    # Many to one
    video = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        null=True
    )
    # Many to one
    len = models.ForeignKey(
        Len,
        on_delete=models.SET_NULL,
        null=True
    )
    # Many to one
    camera = models.ForeignKey(
        Camera,
        on_delete=models.SET_NULL,
        null=True
    )
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

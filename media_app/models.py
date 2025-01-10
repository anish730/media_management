from django.db import models

class MediaFile(models.Model):
    CATEGORY_CHOICES = [
        ('Audio', 'Audio'),
        ('Video', 'Video'),
        ('Image', 'Image'),
    ]

    file = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=255)
    size = models.PositiveIntegerField()  # in bytes
    file_type = models.CharField(max_length=50)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.file_name

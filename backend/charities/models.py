from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

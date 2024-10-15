from django.db import models

# Create your models here.
class KeywordData(models.Model):
    category = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    variable_level_1 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} - {self.term}"
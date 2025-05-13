from django.db import models
class Evaluation(models.Model):
      url = models.URLField()
      grade = models.CharField(max_length=2)
      report = models.FileField(upload_to='reports/')
      evaluated_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

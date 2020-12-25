from django.db import models
import datetime

# Create your models here.

class Bucket(models.Model):
    name = models.CharField("Bucket Name", max_length=200)
    datetime = models.DateTimeField("Date TIme", default=datetime.datetime.now())

    def __str__(self):
        return self.name

class Todo(models.Model):
    bucket = models.ForeignKey(Bucket, related_name="todo_bucket", on_delete=models.CASCADE)
    name = models.CharField("Todo", max_length=200)
    target = models.DateTimeField("Date TIme", null=True, blank=True)
    created_datetime = models.DateTimeField("Date TIme", default=datetime.datetime.now())
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


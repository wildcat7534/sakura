from django.db import models
import datetime
from django.utils import timezone

import ollama


class ChatMessage(models.Model):
  sender = models.CharField(max_length=100)
  message = models.TextField()
  timestamp = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"{self.sender}: {self.message}"

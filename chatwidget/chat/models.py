from django.db import models
from django.contrib.auth.models import User
import uuid

class Message(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self) -> str:
        return f'{self.content}'


class Chat(models.Model):
    CHOICES_STATUS = (
        (0, 'Создан'),
        (1, 'Активен'),
        (2, 'Закрыт'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author_name = models.CharField(max_length=64)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)
    status = models.CharField(max_length=1, choices=CHOICES_STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self) -> str:
        return f'{self.author_name} - {self.agent}'

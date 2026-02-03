from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='application')
    full_name = models.CharField("ФИО", max_length=200)
    phone = models.CharField("Номер телефона", max_length=20)
    email = models.EmailField("Email")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.full_name}"

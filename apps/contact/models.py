from django.db import models

class ContactPage(models.Model):
    phone_1 = models.CharField("Телефон 1", max_length=20)
    phone_2 = models.CharField("Телефон 2", max_length=20, blank=True)
    phone_3 = models.CharField("Телефон 3", max_length=20, blank=True)

    email = models.EmailField("Email")

    map_embed = models.TextField(
        "Код карты (iframe)",
        help_text="Вставь iframe-код карты (Google / Яндекс)"
    )

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return "Страница контактов"

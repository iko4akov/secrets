from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings
from constants.constants import NULLABLE


class Secret(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user',
        on_delete=models.CASCADE
    )
    name_secret = models.CharField(max_length=20, verbose_name='name_secret')
    secret = models.TextField(verbose_name='secret')

    life_days = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                message="Значение должно быть положительным."
            ),
            MaxValueValidator(
                7,
                message="Количество дней жизни не может быть больше недели."
            )
        ]
    )

    is_reader = models.BooleanField(default=False)

    word_code = models.CharField(max_length=50, verbose_name='кодовое слово')
    secret_key = models.CharField(max_length=100, verbose_name='url тайны', **NULLABLE)

    date_of_burning = models.DateTimeField(verbose_name='дата сожжения секрета', **NULLABLE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'Секрет {self.name_secret} - срок жизни {self.date_of_burning}'
        )

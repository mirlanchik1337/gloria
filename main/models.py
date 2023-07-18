from django.db import models


class Category(models.Model):
    CHOICES = (
        ('ШАРИКИ', 'ШАРИКИ'),
        ('ЦВЕТЫ', 'ЦВЕТЫ'),
        ('Cладкий подарок', 'Сладкий подарок'),
        ('Открытка', 'Открытка'),
        ('Другое', 'Другое')
    )
    name = models.CharField(choices=CHOICES ,max_length=200)

    def __str__(self):
        return self.name

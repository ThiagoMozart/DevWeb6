from decimal import Decimal

from django.db import models
from categoria.models import Categoria
from projeto import settings


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=100)
    qtd = models.IntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table='produto'

    def __str__(self):
        return self.nome









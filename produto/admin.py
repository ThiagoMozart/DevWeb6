from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    fields = ('categoria', 'nome', 'qtd', 'preco')

admin.site.register(Produto, ProdutoAdmin)

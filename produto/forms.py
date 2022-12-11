from django import forms

from categoria.models import Categoria
from produto.models import Produto


class QuantidadeForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    qtd = forms.IntegerField(widget=forms.TextInput())


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('nome', 'categoria', 'preco', 'qtd')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nome')
        self.fields['categoria'].empty_label = '--- Selecione uma categoria ---'
        self.fields['categoria'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['preco'].min_value = 0
        self.fields['preco'].error_messages = {'invalid': 'Valor inválido.',
                                               'max_digits': 'Mais de 5 dígitos no total.',
                                               'max_decimal_places': 'Mais de 2 dígitos decimais.',
                                               'max_whole_digits': 'Mais de 3 dígitos inteiros.'}
        self.fields['preco'].widget.attrs.update({
            'class': 'form-control form-control-sm'
        })

        self.fields['qtd'].min_value=1
        self.fields['qtd'].error_messages={
            'min_value': 'A quantidade deve ser maior ou igual a zero.'
        }
        self.fields['qtd'].widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
        })

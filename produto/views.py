import locale
from decimal import Decimal

from django.db.models import Sum, F
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from produto.forms import ProdutoForm, QuantidadeForm
from produto.models import Produto


def index(request):
    return render(request, 'produto/index.html')


def lista_produtos(request):
    lista_de_produtos = Produto.objects.all()
    preco_total = Decimal("0")
    lista_de_forms = []

    for produto in lista_de_produtos:
        preco_total += (produto.qtd * produto.preco)

        lista_de_forms.append(QuantidadeForm(initial={
            'qtd': produto.qtd,
            'id': produto.id
        }))

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    preco = locale.currency(preco_total, grouping=True)

    context = {
        'listas': zip(lista_de_produtos, lista_de_forms),
        'valor_total': preco
    }

    return render(request, 'produto/lista_produtos.html', context=context)


@csrf_exempt
def atualiza_produtos(request):
    form = QuantidadeForm(request.POST)

    if form.is_valid():
        id = form.cleaned_data['id']
        qtd = form.cleaned_data['qtd']

        produto = get_object_or_404(Produto, pk=id)
        produto.qtd = qtd
        produto.save()

        resultado = Produto.objects.aggregate(preco_total=Sum(F('preco') * F('qtd')))
        preco_total = Decimal(resultado['preco_total'])

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        preco = locale.currency(preco_total, grouping=True)

        return JsonResponse({'preco_total': preco})

    else:
        raise ValueError('Error')


@csrf_exempt
def deleta_produto(request):
    form = QuantidadeForm(request.POST)
    id = form.data['id']

    produto = get_object_or_404(Produto, pk=id)
    produto.delete()

    resultado = Produto.objects.aggregate(preco_total=Sum(F('preco') * F('qtd')))
    preco_total = Decimal(resultado['preco_total'])

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    preco = locale.currency(preco_total, grouping=True)

    return JsonResponse({'preco_total': preco})


@csrf_exempt
def cadastra_produto(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST:
        produto_form = ProdutoForm(request.POST)

        if produto_form.is_valid():
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

            produto = produto_form.save(commit=False)
            produto.preco = Decimal(produto.preco).quantize(Decimal("0.01"))
            produto.save()

            resultado = Produto.objects.aggregate(preco_total=Sum(F('preco') * F('qtd')))
            preco_total = Decimal(resultado['preco_total'])

            preco = locale.currency(preco_total, grouping=True)

            novo_produto = model_to_dict(produto)
            novo_produto["preco"] = locale.currency(produto.preco, grouping=True)

            return JsonResponse({'novoProduto': novo_produto,
                                 'categoria': model_to_dict(produto.categoria),
                                 'preco_total': preco}, safe=False)
    else:
        produto_form = ProdutoForm()

    context = {
        'form': produto_form
    }
    return render(request, 'produto/cadastra_produto.html', context=context)





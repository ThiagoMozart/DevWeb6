from django.contrib import admin
from django.urls import path, include
from projeto import views

urlpatterns = [
    path('', include('produto.urls')),
    path('produto/', include('produto.urls')),
    path('admin/', admin.site.urls),
]

#     Como acessar a página index.html do projeto:
#     http://127.0.0.1:8000/
#
#     Como acessar a página index.html de produto:
#     http://127.0.0.1:8000/produto/
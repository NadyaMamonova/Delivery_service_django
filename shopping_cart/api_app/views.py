#from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CartItem


@method_decorator(csrf_exempt, name='dispatch')
#Функция-обработчик для входящих запросов
class ShoppingCart(View):
    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))  #Извлечение данных запроса
        #Извлечение данных продукта
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')

        #Создание словаря данных
        product_data = {
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,
        }

        #Создание элемента корзины
        cart_item = CartItem.objects.create(**product_data)

        data = {
            "message": f"New iem added to Cart with id: {cart_item.id}"
        }
        return JsonResponse(data, status=201)


    #Функция-обработчик запросов для получения информации
    def get(self, request):
        #Получение количества элементов
        items_count = CartItem.objects.count()
        #Получение всех элементов
        items = CartItem.objects.all()

        #Список данных элементов
        items_data = []
        for item in items:
            items_data.append({
                'product_name': items.product_name,
                'product_price': items.product_price,
                'product_quantity': items.product_quantity,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):

    #Функция для обновления уже сохранённых объектов
    def patch(self, request, item_id):
        data = json.loads(request.body.decobe("utf-8"))
        item = CartItem.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()

        data = {
            'message': f"Item {item_id} has been updated"
        }

        return JsonResponse(data)

    #Функция-обработчик запроса на удаление объекта
    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f"Item {item_id} has been deleted"
        }

        return JsonResponse(data)

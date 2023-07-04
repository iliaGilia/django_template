import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.views import View
# import requests
# from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class DynamicImageView(View):
    def get(self, request):
        # URL of the image you want to display
        image_url = "https://picsum.photos/200/300"
        
        # Fetch the image from the URL
        response = requests.get(image_url)
        
        # Open the image using Pillow
        image = Image.open(BytesIO(response.content))
        
        # Resize the image to your desired dimensions
        image = image.resize((500, 500))
        
        # Save the image to a byte stream
        image_stream = BytesIO()
        image.save(image_stream, format='PNG')
        
        # Set the content type of the response
        response = HttpResponse(content_type='image/png')
        
        # Set the image stream as the response content
        response.write(image_stream.getvalue())
        
        return response

def index(req):
    return JsonResponse('hello', safe=False)

from rest_framework import serializers
from .models import Product, Order
from rest_framework.response import Response
from rest_framework import status

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  
           
        def create(self, validated_data):
            user = self.context['user']
            validated_data['user'] = user
            return Order.objects.create(**validated_data,user=user)

# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields =  ['amount', 'desc', 'price']
#     def create(self, validated_data):
#         # return Order.objects.create(**validated_data)
#         user = self.context['user']
#         return Order.objects.create(**validated_data,user=user)
    
# class CartView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         cart_items = request.data
#         print(cart_items)
#         serializer = CartItemSerializer(data=request.data,  context={'user': request.user},many=True)
#         if serializer.is_valid():
#             cart_items = serializer.save()
#         #     # Process the cart items as needed
#         #     # ...
#             return Response("Cart items received and processed successfully.")
#         else:
#             return Response(serializer.errors, status=400)
#     def get(self,request):
#         user=request.user
#         my_model = user.order_set.all()
#         serializer = CartItemSerializer(my_model,many=True)
#         return Response(serializer.data)



class product_view(APIView):
    
    def get(self, request):
        
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)


    def post(self, request):
        
        serializer = ProductSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        
        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        
        my_model = Product.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def checkout(req):  #actual order(buy)
#     print(req.data)
#     # return Response("test")
#     serializer =OrderSerializer(data=req.data, context={'user': req.user})
#     if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#free access
def index(req):
    return HttpResponse("hello")
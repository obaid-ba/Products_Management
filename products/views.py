from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
import os
from django.conf import settings
from datetime import datetime
# Create your views here.


def products(req):
    return render(req, 'products/products.html', {'products': Product.objects.all()})


def newproduct(request):
    # price = request.POST.get("price")
    # image = request.POST.get('image')
    # data = {
    #     "name": str(request.POST.get("name")),
    #     "content": str(request.POST.get("content")),
    #     "price": price,
    #     "image": image,
    #     "active": True
    # }
    # insert = Product(name=data['name'], content=data['content'], price=data['price'], image=data['image'],active=data['active'])
    # if not price == None:
    #     insert.save()
    # return render(request, 'products/newproduct.html')
    if request.method == 'POST':
        price = request.POST.get("price")
        image_file = request.FILES.get('image')
        if image_file and price:
            # save image in media file
            today = datetime.now()
            folder_path = f'images/{today.strftime("%d/%m/%y")}'
            full_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            os.makedirs(full_path, exist_ok=True)
            file_name = image_file.name
            file_path = os.path.join(folder_path, file_name)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            # wb+: Write mode with binary data. This mode is used for binary files like images.
            with open(full_file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            # save data in database
            product = Product(
                name=request.POST.get("name"),
                content=request.POST.get("content"),
                price=price,
                image=f'images/{today.strftime("%d/%m/%y")}/{file_name}',
                active=True
            )
            product.save()
    return render(request, 'products/newproduct.html')


def deleteproduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')


def editproduct(request, id):
    product = Product.objects.get(id=id)
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        price = request.POST.get('price')
        name = request.POST.get('name')
        content = request.POST.get('content')
        product.price = price
        product.name = name
        product.content = content
        product.save()
    return render(request, 'products/editProduct.html', {'product': product})

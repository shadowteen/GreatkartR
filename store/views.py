import os

from category.models import Category , SubCategory
from orders.models import OrderProduct
from store.models import Product, ProductGallery
from django.shortcuts import get_object_or_404, redirect, render
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Sum, Count
from django.http import JsonResponse
import urllib.request
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def store(request, category_slug=None, brand=None):
    
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True).order_by('-price') 
        brands = Product.objects.values('brand').filter(category=categories, is_available=True).annotate(Count('id'))
        width = Product.objects.values('width').filter(category=categories, is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 
    
        if brand is not None:
            products = Product.objects.all().filter(category=categories,brand=brand, is_available=True).order_by('-price') 
            brands = Product.objects.values('brand').filter(category=categories, brand=brand,is_available=True).annotate(Count('id'))
            width = Product.objects.values('width').filter(category=categories,brand=brand, is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-price')  
        brands = Product.objects.values('brand').filter(is_available=True).annotate(Count('id'))
        width = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 

        if brand is not None:
            products = Product.objects.all().filter(brand=brand, is_available=True).order_by('-price') 
            brands = Product.objects.values('brand').filter(brand=brand,is_available=True).annotate(Count('id'))

    product_count = products.count()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 12)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    ahs = Product.objects.values('ah').filter(category=5,is_available=True).exclude(ah__exact='').annotate(Count('id'))
    ccas = Product.objects.values('cca').filter(category=5,is_available=True).exclude(cca__exact='').annotate(Count('id'))
   

    context = {
        'products': paged_products,
        'product_count': product_count,
        'width':width,
        'brands': brands,
        'ahs':ahs,
        'ccas':ccas,
        'title': 'Best Tyres | Store'
    }
    return render(request, 'store/store.html', context=context)



def store1(request,  category_slug=None, subcategory_slug=None):
    
    if subcategory_slug is not None:
        categories = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = Product.objects.all().filter(subcategory=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    product_count = products.count()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'title': 'Best Tyres | Store'
    }
    return render(request, 'store/store.html', context=context)



def product_detail(request, category_slug,  product_slug, brand):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None  

    try:
        relastedprod = Product.objects.order_by('-price').filter(width__icontains=single_product.width, height__icontains=single_product.height, diameter__icontains=single_product.diameter,is_available=True).exclude(id=single_product.id)
    except OrderProduct.DoesNotExist:
        relastedprod = None
        
    try:
        
        webUrl = urllib.request.urlopen("http://124.43.12.72/SW_APP/stock_balget.php?skuno=" + single_product.skuno)  
        data = webUrl.read()
        y = json.loads(data)
        stockbal = (y["totbal"])
        a = (y["a"])
        b = (y["b"])
        c = (y["c"])
        d = (y["d"])
        



    except:
        stockbal = 0 
        a = 0
        b = 0
        c = 0
        d = 0
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)



    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'product_gallery':product_gallery,
        'orderproduct':orderproduct,
        'relastedprod': relastedprod,
        'stockbal': stockbal, 
        'title': 'Best Tyres | ' + single_product.product_name,
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    }
    return render(request, 'store/product_detail.html', context=context)




def search(request):
    if 'width' in request.GET:
        width = request.GET.get('width')
        profile = request.GET.get('profile')
        diameter = request.GET.get('diameter')

        products = Product.objects.order_by('-price').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter,is_available=True)
        product_count = products.count()



    context = {
        'products': products,
        'q': width,
        'product_count': product_count,
        'title': 'Best Tyres | Product Store'
    }
    return render(request, 'store/store.html', context=context)

def get_sizes(request):
    width =""
    if 'width' in request.GET:
        width = request.GET.get('width') 
        width = Product.objects.values('height').filter(width__icontains=width,is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('height') 
        product_count = width.count()

    if 'profile' in request.GET:
        width = request.GET.get('width') 
        profile = request.GET.get('profile')  
        width = Product.objects.values('diameter').filter(width__icontains=width,height__icontains=profile,is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('diameter') 
        product_count = width.count()    
    if 'rim' in request.GET:
        width = request.GET.get('width') 
        profile = request.GET.get('profile') 
        rim = request.GET.get('rim')  
        width = Product.objects.values('terrain').filter(width__icontains=width,height__icontains=profile,diameter__icontains=rim,is_available=True).exclude(terrain__exact='').annotate(Count('id')).order_by('terrain') 
        product_count = width.count()        


   
    

    return JsonResponse({"width": list(width), "product_count": product_count }, status=200)



def get_agentdt(request):
    agentdt =""
    if 'location' in request.GET:
        if request.GET.get('location')  == "Dehiwala":
            agentdt = "<table class='table'><tr><td>Priyanka</td><td>077111111</td></tr></table>"
        if request.GET.get('location')  == "Staple Street":
            agentdt = "<table class='table'><tr><td>Chathuni</td><td>077111110</td></tr></table>"
        if request.GET.get('location')  == "Polonnaruwa":
            agentdt = "<table class='table'><tr><td>Harshana</td><td>077111112</td></tr></table>"
        if request.GET.get('location')  == "Jaffna":
            agentdt = "<table class='table'><tr><td>Ronald</td><td>077111113</td></tr></table>"
    
    return JsonResponse({"agdt":"Agent Details","agcontdt": agentdt }, status=200)


def search(request):

    width =None
    profile = None
    diameter = None
    terrain = None
    ah = None
    lr =None

    if 'width' in request.GET:
        width = request.GET.get('width')
        profile = request.GET.get('profile')
        diameter = request.GET.get('diameter')
        terrain = request.GET.get('terrain')


        view = request.GET.get('view1')

 
        products = Product.objects.order_by('-price','product_name').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter,is_available=True)
        product_count = products.count()


    widths = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id'))
   
    ah = None
    lr = None
    cca = None

    if 'ah' in request.GET:
        if 'ah' in request.GET:
            ah = request.GET.get('ah')
        
        if 'lr' in request.GET:
            lr = request.GET.get('lr') 

        if 'cca' in request.GET:
            cca = request.GET.get('cca') 


        
        products = Product.objects.order_by('-price').filter(Q(ah__icontains=ah) | Q(cca__icontains=cca),category=5,is_available=True)
        product_count = products.count()
                    
    ahs = Product.objects.values('ah').filter(category=5,is_available=True).exclude(ah__exact='').annotate(Count('id'))
    ccas = Product.objects.values('cca').filter(category=5,is_available=True).exclude(cca__exact='').annotate(Count('id'))
   
    context = {
        'products': products,
        'q': width,
        'product_count': product_count,
        'width': widths,
        'swidth': width,
        'sprofile': profile,
        'sdiameter': diameter,
        'sterrain': terrain,
        'ahs': ahs,
        'ccas': ccas,
        'scca':cca,
        'sah':ah,
        'slr':lr,
        'title': 'Best Tyres | Product Search'
        
    }



   
    return render(request, 'store/store_search_view.html', context=context)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}tinymce/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})
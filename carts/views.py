from django.shortcuts import get_object_or_404, render, redirect
from carts.models import Cart, CartItem
from category.models import Category
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import urllib.request
import json

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart_ind(request):
    product_id = request.GET.get('product_id')
    quantity = request.GET.get('quantity')

    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    if current_user.is_authenticated:
        is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_exists_cart_item:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
                cart_item = CartItem.objects.get(product=product, user=current_user)
                cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:
                saleprice = product.price * ((100-product.discount)/100)
                cart_item = CartItem.objects.create(
                    product=product,
                    price=saleprice,
                    cart=cart,
                    user=current_user,
                    quantity=quantity
                )
                cart_item.save()

                webUrl = urllib.request.urlopen("http://124.43.12.72/SW_APP/order_process.php?stk_no=" + str(product.skuno) + "&refno=" + str(cart.id) + "&quantity=" + str(quantity))  
                return webUrl
                data = webUrl.read()
                y = json.loads(data) 

        else:
            saleprice = product.price * ((100-product.discount)/100)
            cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    price=saleprice,
                    user=current_user,
                    quantity=quantity
                )
            cart_item.save()
            webUrl = urllib.request.urlopen("http://124.43.12.72/SW_APP/order_process.php?stk_no=" + str(product.skuno) + "&refno=" + str(cart.id) + "&quantity=" + str(quantity))  
            data = webUrl.read()
            y = json.loads(data) 
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            saleprice = product.price * ((100-product.discount)/100)
            cart_item = CartItem.objects.create(
                product=product,
                price=saleprice,
                cart=cart,
                quantity=quantity
            )
            cart_item.save()
            webUrl = urllib.request.urlopen("http://124.43.12.72/SW_APP/order_process.php?stk_no=" + str(product.skuno) + "&refno=" + str(cart.id) + "&quantity=" + str(quantity))  
            data = webUrl.read()
            y = json.loads(data) 

    return redirect('cart')

def add_cart(request, product_id):
    
    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    if current_user.is_authenticated:
        is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_exists_cart_item:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
                cart_item = CartItem.objects.get(product=product, user=current_user)
                
                cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:
                saleprice = product.price * ((100-product.discount)/100)
                cart_item = CartItem.objects.create(
                    product=product,
                    price=saleprice,
                    cart=cart,
                    user=current_user,
                    quantity=1
                )
                cart_item.save()
        else:
            saleprice = product.price * ((100-product.discount)/100)
            cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    price=saleprice,
                    user=current_user,
                    quantity=1
                )
            cart_item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            saleprice = product.price * ((100-product.discount)/100)
            cart_item = CartItem.objects.create(
                product=product,
                price=saleprice,
                cart=cart,
                quantity=1
            )
            cart_item.save()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
                 
                total += cart_item.price * cart_item.quantity
                quantity += cart_item.quantity
        tax = 0
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total if "tax" in locals() else 0,
    }
    return render(request, 'store/cart.html', context=context)


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product=product,
                user=request.user
            )
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            product=product,
            cart=cart
        )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            product=product,
            user=request.user
        )
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            product=product,
            cart=cart
        )
    cart_item.delete()
    
    return redirect('cart')

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        # cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = 0
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Ch??? b??? qua
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context=context)
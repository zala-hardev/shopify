# myapp/context_processors.py
from .models import WishList,Product,Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# @login_required(login_url='login')
def wishlist_items(request):
    if request.user.is_authenticated:
        wishlist_items = WishList.objects.filter(user=request.user).select_related('product')
        wishlist_item_list = []
        for i in wishlist_items:
          wishlist_item_list.append(i.product.product_name)
        total_wishlist_products = len(wishlist_item_list)
        return {'wishlist_items': wishlist_items,'wishlist_item_list':wishlist_item_list,'total_wishlist_products':total_wishlist_products}

    else:
        wishlist_items = []
        wishlist_item_list = []
    
    return {'wishlist_items': wishlist_items,'wishlist_item_list':wishlist_item_list}

def cart_items(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(Q(user=request.user) & Q(quantity__gte=1))
        total_cart_items = len(cart_items)
        cart_items_list = [c.product.product_name for c in cart_items]
        # print(cart_items_list)

        return {'total_cart_items':total_cart_items,'cart_items_list':cart_items_list}
        
    return {}

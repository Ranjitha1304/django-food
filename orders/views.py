from django.shortcuts import render, redirect, get_object_or_404
from restaurant.models import MenuItem
from .models import CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, menu_item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            cart_item.quantity = qty
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([ci.total_price for ci in cart_items])
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')
    if request.method == 'POST':
        total_price = sum([ci.total_price for ci in cart_items])
        order = Order.objects.create(user=request.user, total_price=total_price)
        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=ci.menu_item,
                quantity=ci.quantity,
                price=ci.menu_item.price
            )
        cart_items.delete()  # empty cart
        return render(request, 'orders/order_success.html', {'order': order})
    total = sum([ci.total_price for ci in cart_items])
    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

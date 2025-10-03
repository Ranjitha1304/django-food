from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuItem

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/home.html', {'restaurants': restaurants})

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    return render(request, 'restaurant/menu.html', {'restaurant': restaurant, 'menu_items': menu_items})


from django.contrib.auth.decorators import user_passes_test
from orders.models import Order
from restaurant.models import MenuItem

def admin_required(user):
    return user.is_staff

@user_passes_test(admin_required)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = sum([o.total_price for o in Order.objects.all()])
    total_menu_items = MenuItem.objects.count()
    return render(request, 'restaurant/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_menu_items': total_menu_items
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product, Category, Order

def product_list(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'min_price': min_price,
        'max_price': max_price
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    return render(request, 'store/product_cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

@csrf_exempt
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        order = Order.objects.create(name=name, email=email, address=address)

        order_summary = ""
        for item in cart_items:
            order_summary += f"- {item['product'].name} × {item['quantity']} = R{item['subtotal']}\n"

        admin_message = f"""
New Order Received

Order #{order.id}
Name: {name}
Email: {email}
Address: {address}
Total: R{total}

Items Ordered:
{order_summary}
"""

        customer_message = f"""
Hi {name},

Thanks for your order #{order.id}!

Here’s what you ordered:
{order_summary}

Total: R{total}

We’ll process your order shortly.

Cheers,
Juvenile Corner
"""

        try:
            send_mail(
                subject='New Order Received',
                message=admin_message,
                from_email='your-email@gmail.com',
                recipient_list=['your-email@gmail.com'],
                fail_silently=False,
            )

            send_mail(
                subject='Thank you for your order!',
                message=customer_message,
                from_email='your-email@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print("Email error:", e)

        request.session['cart'] = {}
        return redirect('order_confirmation')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@csrf_exempt
def yoco_payment(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        amount = request.POST.get('amount')

        # Retrieve the latest order (or use session data to match it)
        order = Order.objects.latest('id')
        order.transaction_id = token
        order.save()

        print("Saved transaction ID:", token)

        return JsonResponse({'status': 'success'
    })

def order_confirmation(request):
    return render(request, 'store/order_confirmation.html')

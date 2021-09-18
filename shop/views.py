from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders,Comments, OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt

import smtplib
import ssl


def mail(order):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "mycart2403@gmail.com"
    receiver_email = order.email
    password = 'Z3cs48gBO3hW'

    order_id = order.id
    items_json = json.loads(order.items_json)

    name = order.name
    email = order.email
    address = order.address
    city = order.city
    state = order.state
    zip_code = order.zip_code
    phone = order.phone
    item_display_info = ""
    for valid, item_info in items_json.items():
        qty = item_info[0]
        name = item_info[1]
        price = item_info[2]
        item_display_info += f"Name :- {name}    qty :- {qty}    cost :- {price}\n  "
    message = f"""\
    Subject: MY AWESOME CART


    Your order has been placed with order id {order_id} and amount {amount}
    Your Items are :- 
    {item_display_info}

    Delivery Information
    Name :- {name}
    Email :- {email}
    address :- {address}
    city :- {city}
    state :- {state}
    zip_code :- {zip_code}
    phone :- {phone}

    Thankyou for shopping from My Awesome Cart. Wish you a good day ahead!
    """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print(e)

def index(request):
    products = Product.objects.all()
    print(products)
    n = len(products)
    nslides = n//4 + ceil((n/4) - (n//4))

    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod,range(1,nslides),nslides])
    params = {'allProds': allProds}
    return render(request,"shop/index.html",params)

def about(request):
    return render(request, "shop/about.html")


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates" :updates, "item_json": order[0].items_json}, default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noite"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)




def productview(request,myid):
    product = Product.objects.filter(id=myid)[0]
    comments = Comments.objects.filter(post = product)
    products = Product.objects.all()

    n = len(products)
    nslides = n // 4 + ceil((n / 4) - (n // 4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides), nslides])


    context = {'product':product, 'comments': comments, 'allProds': allProds, 'user': request.user}
    return render(request, "shop/productview.html",context)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "mycart2403@gmail.com"
        receiver_email = order.email
        password = 'Z3cs48gBO3hW'

        order_id = order.order_id
        items_json = json.loads(order.items_json)

        name = order.name
        email = order.email
        address = order.address
        city = order.city
        state = order.state
        zip_code = order.zip_code
        phone = order.phone
        item_display_info = ""
        for valid, item_info in items_json.items():
            qty = item_info[0]
            name = item_info[1]
            price = item_info[2]
            item_display_info += f"Name :- {name}    qty :- {qty}    cost :- {price}\n  "
        message = f"""\
            Subject: MY AWESOME CART


            Your order has been placed with order id {order_id}
            Your Items are :- 
            {item_display_info}

            Delivery Information
            Name :- {name}
            Email :- {email}
            address :- {address}
            city :- {city}
            state :- {state}
            zip_code :- {zip_code}
            phone :- {phone}

            Thankyou for shopping from My Awesome Cart. Wish you a good day ahead!
            """
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            try:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            except Exception as e:
                print(e)
        messages.success(request, "Successfully order placed")
        #return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # param_dict = {
        #     'MID': 'Your-Merchant-Id-Here',
        #         'ORDER_ID': str(order.order_id),
        #         'TXN_AMOUNT': str(amount),
        #         'CUST_ID': email,
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        #
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')



def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get("postSno")
        post = Product.objects.get(id=postSno)
        comment = Comments(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
    return redirect(f"/shop/products/{post.id}")

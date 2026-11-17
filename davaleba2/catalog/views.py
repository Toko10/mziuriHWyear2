from django.http import HttpResponse, Http404

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1800},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Mouse", "price": 40},
]


def home(request):
    return HttpResponse("<h1>myshop</h1><a href='/products/'>პროდუქტები</a>")


def about(request):
    return HttpResponse(
        "<h1>ჩემს შესახებ</h1>"
        "<p>მე ვარ დამწყები პროგრამისტი. "
        "ვსწავლობ Python-სა და Django-ს. "
        "ეს ჩემი პირველი Django პროექტია.</p>"
    )


def product_list(request):
    items = "".join(
        [
            f"<li><a href='/products/{p['id']}/'>{p['name']}: {p['price']} ₾</a></li>"
            for p in PRODUCTS
        ]
    )
    return HttpResponse(f"<h1>პროდუქტები</h1><ul>{items}</ul>")


def product_detail(request, pk):
    for p in PRODUCTS:
        if p["id"] == pk:
            return HttpResponse(f"<h1>{p['name']}</h1><p>ფასი: {p['price']} ₾</p>")
    raise Http404("პროდუქტი ვერ მოიძებნა")
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect
import random

RECIPES = [
    {"id": 1, "slug": "khinkali", "name": "ხინკალი", "category": "main",
     "minutes": 90, "vegetarian": False,
     "ingredients": ["ფქვილი", "საქონლის ხორცი", "ღორის ხორცი", "ხახვი", "კვლიავი"]},
    {"id": 2, "slug": "khachapuri", "name": "ხაჭაპური", "category": "bakery",
     "minutes": 60, "vegetarian": True,
     "ingredients": ["ფქვილი", "იმერული ყველი", "კვერცხი", "კარაქი"]},
    {"id": 3, "slug": "lobiani", "name": "ლობიანი", "category": "bakery",
     "minutes": 75, "vegetarian": True,
     "ingredients": ["ფქვილი", "ლობიო", "ხახვი", "კარაქი"]},
    {"id": 4, "slug": "pkhali", "name": "ფხალი", "category": "snack",
     "minutes": 30, "vegetarian": True,
     "ingredients": ["ისპანახი", "ნიგოზი", "ნიორი", "ქინძი"]},
    {"id": 5, "slug": "churchkhela", "name": "ჩურჩხელა", "category": "dessert",
     "minutes": 240, "vegetarian": True,
     "ingredients": ["ნიგოზი", "ყურძნის წვენი", "ფქვილი"]},
    {"id": 6, "slug": "chakapuli", "name": "ჩაქაფული", "category": "main",
     "minutes": 120, "vegetarian": False,
     "ingredients": ["ცხვრის ხორცი", "ტყემალი", "ტარხუნა", "თეთრი ღვინო"]},
]


def page(title, body):
    return HttpResponse(f"<h1>{title}</h1>{body}<br><br><a href='/recipes/'>← ყველა რეცეპტი</a>")


def recipe_list(request):
    category = request.GET.get("category")
    max_time = request.GET.get("max_time")
    vegetarian = request.GET.get("vegetarian")

    filtered_recipes = RECIPES

    if category:
        filtered_recipes = [r for r in filtered_recipes if r["category"] == category]

    if max_time:
        try:
            max_time_int = int(max_time)
            filtered_recipes = [r for r in filtered_recipes if r["minutes"] <= max_time_int]
        except ValueError:
            pass

    if vegetarian == "yes":
        filtered_recipes = [r for r in filtered_recipes if r["vegetarian"]]

    if not filtered_recipes:
        body = "<p>ვერაფერი მოიძებნა</p>"
    else:
        items = "".join(
            [f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a> · {r['minutes']} წთ</li>" for r in filtered_recipes])
        body = f"<ul>{items}</ul>"

    return page("ქართული რეცეპტები", body)


def recipe_detail(request, pk):
    recipe = next((r for r in RECIPES if r["id"] == pk), None)
    if not recipe:
        raise Http404("რეცეპტი ვერ მოიძებნა")

    ingredients_list = ", ".join(recipe["ingredients"])
    veg_status = "კი" if recipe["vegetarian"] else "არა"

    body = f"""
        <p><b>კატეგორია:</b> {recipe['category']}</p>
        <p><b>მომზადების დრო:</b> {recipe['minutes']} წთ</p>
        <p><b>ვეგეტარიანულია:</b> {veg_status}</p>
        <p><b>ინგრედიენტები:</b> {ingredients_list}</p>
    """
    return page(recipe["name"], body)


def category_detail(request, category_name):
    cat_recipes = [r for r in RECIPES if r["category"] == category_name]
    if not cat_recipes:
        raise Http404("კატეგორია ვერ მოიძებნა")

    items = "".join(
        [f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a> · {r['minutes']} წთ</li>" for r in cat_recipes])
    body = f"<ul>{items}</ul>"

    return page(f"კატეგორია: {category_name}", body)


def search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        body = "<p>ჩაწერე საძიებო სიტყვა</p>"
    else:
        matched = [r for r in RECIPES if any(q.lower() in ing.lower() for ing in r["ingredients"])]
        if not matched:
            body = f"<p>სიტყვით '{q}' ვერაფერი მოიძებნა</p>"
        else:
            items = "".join([f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a></li>" for r in matched])
            body = f"<ul>{items}</ul>"

    return page(f"ძებნა: {q}", body)


def recipe_by_slug(request, slug):
    recipe = next((r for r in RECIPES if r["slug"] == slug), None)
    if not recipe:
        raise Http404("რეცეპტი ვერ მოიძებნა")

    ingredients_list = ", ".join(recipe["ingredients"])
    veg_status = "კი" if recipe["vegetarian"] else "არა"

    body = f"""
        <p><b>კატეგორია:</b> {recipe['category']}</p>
        <p><b>მომზადების დრო:</b> {recipe['minutes']} წთ</p>
        <p><b>ვეგეტარიანულია:</b> {veg_status}</p>
        <p><b>ინგრედიენტები:</b> {ingredients_list}</p>
    """
    return page(recipe["name"], body)


def random_recipe(request):
    r = random.choice(RECIPES)
    return redirect("catalog:detail", pk=r["id"])


def stats(request):
    count = len(RECIPES)
    categories = {}
    total_minutes = 0

    for r in RECIPES:
        cat = r["category"]
        categories[cat] = categories.get(cat, 0) + 1
        total_minutes += r["minutes"]

    avg_minutes = total_minutes / count if count > 0 else 0

    data = {
        "count": count,
        "categories": categories,
        "avg_minutes": avg_minutes
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})
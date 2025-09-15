from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

def hello_world(request, name="World"):
    """
    Возвращает <h1>Hello, {name}!</h1>
    Дополнительно: устанавливает cookie 'username' (см. раздел «Работа с куками»).
    """
    # Читаем age из query: /hello/Alex?age=21
    age = request.GET.get("age")
    html = f"<h1>Hello, {name}!"
    if age:
        html += f" You are {age} years old."
    html += "</h1>"

    resp = HttpResponse(html)
    # Установим cookie (можно условно, если name передан)
    resp.set_cookie("username", name, samesite="Lax")
    return resp

def redirect_example(request):
    """
    Переадресация на hello_world с параметрами по умолчанию.
    Возвращает 302 (redirect).
    """
    return redirect("hello_default")  # имя маршрута см. в urls

def json_example(request):
    """
    Возвращает JSON-ответ с данными о пользователе.
    """
    data = {"name": request.COOKIES.get("username", "Guest"), "age": 21}
    return JsonResponse(data)

def show_cookies(request):
    """
    Возвращает все cookies в виде простого HTML.
    """
    items = "".join(f"<li>{k} = {v}</li>" for k, v in request.COOKIES.items())
    return HttpResponse(f"<h2>Cookies</h2><ul>{items}</ul>")

def get_cookie(request):
    username = request.COOKIES.get("username", "Guest")
    return HttpResponse(f"<p>username = {username}</p>")

from django.urls import path, re_path
from .views import hello_world, redirect_example, json_example, show_cookies, get_cookie

urlpatterns = [
    path("", hello_world, name="hello_default"),
    path("<str:name>/", hello_world, name="hello_by_name"), 
    re_path(r"^re/(?P<name>[\w\-]+)/$", hello_world, name="hello_re"), 
    path("redirect/", redirect_example, name="redirect_example"),
    path("json/", json_example, name="json_example"),
    path("cookies/", show_cookies, name="show_cookies"),
    path("cookie/get/", get_cookie, name="get_cookie"),
]

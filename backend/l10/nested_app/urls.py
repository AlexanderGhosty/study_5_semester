from django.urls import path
from .views import index, section, item

app_name = "nested"
urlpatterns = [
    path("", index, name="index"),
    path("<slug:slug>/", section, name="section"),        
    path("<slug:section_slug>/<int:item_id>/", item, name="item")
]

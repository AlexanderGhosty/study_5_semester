from django.http import HttpResponse

def index(request):
    return HttpResponse("<h2>Nested: index</h2>")

def section(request, slug: str):
    return HttpResponse(f"<h2>Nested: section {slug}</h2>")

def item(request, section_slug: str, item_id: int):
    return HttpResponse(f"<h2>Nested: {section_slug} / item #{item_id}</h2>")

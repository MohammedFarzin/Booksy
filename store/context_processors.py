from .models import Author

def filter_links(request):
    filter_link = Author.objects.all()
    return dict(filter_links=filter_link)
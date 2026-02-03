from django.shortcuts import render, get_object_or_404
from .models import ContactPage

def contacts(request):
    try:
        contact = ContactPage.objects.first()
        if not contact:
            contact = ContactPage.objects.create(
                phone_1="+7 (999) 999-99-99",
                email="info@example.com",
                map_embed='<iframe src="https://www.google.com/maps/embed?..." width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            )
    except ContactPage.DoesNotExist:
        contact = None
    
    return render(request, "page/contact.html", {"contact": contact})

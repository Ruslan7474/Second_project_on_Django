from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.news.models import Category
from .models import Application
from .forms import ApplicationForm


@login_required(login_url='login')
def application_view(request):
    categories = Category.objects.filter(news__isnull=False).distinct()
    
    # Проверяем, уже ли у пользователя есть заявка
    try:
        existing_app = Application.objects.get(user=request.user)
        app_exists = True
    except Application.DoesNotExist:
        existing_app = None
        app_exists = False

    if request.method == 'POST':
        if app_exists:
            messages.error(request, "Вы уже оставили заявку. Одна заявка на пользователя.")
            return redirect('application')
        
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect('application')
    else:
        form = ApplicationForm()

    context = {
        'form': form,
        'app_exists': app_exists,
        'existing_app': existing_app,
        'categories': categories,
    }
    
    return render(request, 'page/application.html', context)

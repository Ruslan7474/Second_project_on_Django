from django.shortcuts import render, get_object_or_404
from apps.news.models import News, Category, Comment
from django.shortcuts import redirect
from apps.news.forms import CommentForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator

def homepage(request):
    news_all = News.objects.all()
    categories = Category.objects.filter(news__isnull=False).distinct()

    paginator = Paginator(news_all, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    categories = Category.objects.filter(news__isnull=False).distinct()
    comments = news.comments.filter(is_published=True).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Чтобы оставить комментарий, нужно войти в аккаунт.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
            return redirect('news_detail', slug=slug)
    else:
        form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'form': form
    }
    return render(request, 'page/single-page.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_list = News.objects.filter(category=category)
    categories = Category.objects.filter(news__isnull=False).distinct()

    return render(request, 'page/category-page.html', {
        'category': category,
        'news_list': news_list,
        'categories': categories,
    })

def news_search(request):
    query = request.GET.get('q', '')
    categories = Category.objects.filter(news__isnull=False).distinct()

    news_list = News.objects.all()

    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'page/search.html', {
        'news_list': news_list,
        'query': query,
        'categories': categories,
    })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not username:
            errors.append('Введите логин')
        if not password1:
            errors.append('Введите пароль')
        if password1 and password2 and password1 != password2:
            errors.append('Пароли не совпадают')
        if username and User.objects.filter(username=username).exists():
            errors.append('Пользователь уже существует')

        if errors:
            return render(request, 'page/register.html', {
                'error': errors[0],
                'errors': errors,
                'username': username,
            })

        user = User.objects.create_user(
            username=username,
            password=password1
        )

        login(request, user)
        return redirect('homepage')

    return render(request, 'page/register.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'login.html', {
                'error': 'Неверный логин или пароль'
            })

    return render(request, 'page/login.html')
def user_logout(request):
    logout(request)
    return redirect('homepage')

from django.shortcuts import render, get_object_or_404
from apps.about.models import About, Team
from apps.news.models import Category


def aboutFunc(request):
    try:
        about = About.objects.latest('id')
    except About.DoesNotExist:
        about = None
    categories = Category.objects.filter(news__isnull=False).distinct()
    context = { 
        'categories':categories,
        'about':about
    }
    return render(request, 'page/about.html', context)


def teamsFunc(request):
    teams = Team.objects.prefetch_related('sociallink_set')
    categories = Category.objects.filter(news__isnull=False).distinct()
    context = { 
        'categories':categories,
        'teams':teams
    }
    return render(request, 'page/teams.html', context)



def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    categories = Category.objects.filter(news__isnull=False).distinct()  
    context = {
        'team':team, 
        'categories':categories 
    }
    return render(request, 'page/team-single.html', context)
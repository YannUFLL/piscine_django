from django.shortcuts import render
from .models import Movies, People, Planets
from django.http import HttpResponse

# Create your views here.


def form(request):
    try:
        if request.method == "POST":
            min_release = request.POST["min_release_date"]
            max_release = request.POST["max_release_date"]
            min_diameter = int(request.POST["min_diameter"])
            gender = request.POST["gender"]
            print(gender)
            movies = Movies.objects.filter(  release_date__gte=min_release,
                                            release_date__lte=max_release,
                                            characters__homeworld__diameter__gte=min_diameter,
                                            characters__gender=gender ).distinct()
            people_str = []
            if movies.exists() == False: 
                return HttpResponse("Nothing corresponding to your research")
            for movie in movies: 
                for c in movie.characters.filter(homeworld__diameter__gte=min_diameter, gender=gender):
                    people_str.append(f"""{c.name} - 
                                        {c.gender} -
                                        {movie.title} - 
                                        {c.homeworld if c.homeworld else 'Unkmown'} -
                                        {c.homeworld.diameter if c.homeworld else 'Unkmown'}""")
            genders = People.objects.values_list("gender", flat=True).distinct()
            return (render(request, "ex10/movie_filter.html", {"peoples":people_str, "genders":genders}))
        else:
            genders = People.objects.values_list("gender", flat=True).distinct()
            return (render(request, "ex10/movie_filter.html", {"peoples":[], "genders":genders}))
    except Exception as e: 
            return(HttpResponse(e))

from django.http import HttpResponse
from django.shortcuts import render
from .models import Movies
from django.db import IntegrityError

def populate(request):
    movies = [
       (1, "The Phantom Menace", "George Lucas", "Rick McGallum", "1999-05-19"),
       (2, "Attack of the Clones", "George Lucas", "Rick McGallum", "2002-05-16"),
       (3, "Revenge of the Sith", "George Lucas", "Rick McGallum", "2005-05-19"),
       (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McGallum", "1977-05-25"),
       (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McGallum", "1980-05-17"),
       (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, Rick McGallum", "1977-05-25"),
       (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11")
    ]

    result = ""

    try:
        for movie in movies:
            Movies.objects.create(
                episode_nb=movie[0],
                title=movie[1],
                director=movie[2],
                producer=movie[3],
                release_date=movie[4]
            )
        result = 'OK'
    except IntegrityError as e:
        result += f"{movie[1]}: {e}"

    return HttpResponse(result)

def display(request):
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")

    html =  """
<table>
    <tr>
        <th>episode_nb</th>
        <th>title</th>
        <th>producer</th>
        <th>director</th>
        <th>release_date</th>
        <th>Opening</th>
    </tr>
"""

    for movie in movies:
        html += f"""
<tr>
    <td>{movie.episode_nb}</td>
    <td>{movie.title}</td>
    <td>{movie.director}</td>
    <td>{movie.producer}</td>
    <td>{movie.opening_crawl if movie.opening_crawl else ""}</td>
<tr>
"""
        
    html += "/table"
    return HttpResponse(html)

def remove(request):
    try:
        if request.method == "POST":
            movie = Movies.objects.filter(title=request.POST["movie"]).delete()
        titles = Movies.objects.values_list("title", flat=True)
        return (render(request, "ex04/select.html", {"movies": titles}))
    except Exception as e:
        return (HttpResponse("No data available"))


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
    for movie in movies:
        try:
            Movies.objects.create(
                episode_nb=movie[0],
                title=movie[1],
                director=movie[2],
                producer=movie[3],
                release_date=movie[4]
            )
            result += f"{movie[1]}: OK<br>"
        except Exception as e:
            result += f"{movie[1]}: Error, {e}<br>"

    return HttpResponse(result)

def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")

        html =  """
    <table>
        <tr>
            <th>Episode_nb</th>
            <th>Title</th>
            <th>Producer</th>
            <th>Director</th>
            <th>Release_date</th>
            <th>Opening</th>
            <th>Created</th>
            <th>Updated</th>
        </tr>
    """

        for movie in movies:
            html += f"""
    <tr>
        <td>{movie.episode_nb}</td>
        <td>{movie.title}</td>
        <td>{movie.producer}</td>
        <td>{movie.director}</td>
        <td>{movie.release_date}</td>
        <td>{movie.opening_crawl if movie.opening_crawl else ""}</td>
        <td>{movie.created}</td>
        <td>{movie.updated}</td>
    <tr>
    """
            
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")

def update(request):
    try:
        if request.method == "POST":
            movie = Movies.objects.get(title=request.POST["movie"])
            movie.opening_crawl = request.POST["opening_crawl"]
            movie.save()
        titles = Movies.objects.values_list("title", flat=True)
        if titles.exists() == False:
            raise Exception("No data available")
        return (render(request, "ex07/opening_crawl.html", {"movies": titles}))
    except Exception as e:
        return (HttpResponse("No data available"))


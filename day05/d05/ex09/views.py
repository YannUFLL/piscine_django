from django.shortcuts import render
from .models import Planets, People
from django.http import HttpResponse

# Create your views here.

def display(request):
    try: 
        people = People.objects.select_related('homeworld').all()
        list_e = []
        html = """
<table>
<tr>
    <th>name</th>
    <th>homeworld</th>
    <th>climate</th>
</tr>
"""
        for p in people:
            if p.homeworld is not None:
                climate = p.homeworld.climate or "" 
            else:
                climate = ""
            if "windy" in climate or "moderate windy" in climate:
                list_e.append(p)
        list_e = sorted(list_e, key=lambda x: x.name)

        if not list_e:
            return (HttpResponse("""No data available, 
            please use the following command line before use:
            <br>
            python manage.py loaddata ex09/ex09_initial_data.json"""))

        for p in list_e:
                html += f"""
<tr>
    <td>{p.name}</td>
    <td>{p.homeworld.name}</td>
    <td>{p.homeworld.climate}</td>
</tr>
"""
        html += "</table>"
        return (HttpResponse(html))
    except Exception: 
        return (HttpResponse("""No data available, 
            please use the following command line before use:
            <br>
            python manage.py loaddata ex09/ex09_initial_data.json"""))

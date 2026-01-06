from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import psycopg2

# Create your views here.

def init(request):
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'])
        cur = conn.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS ex04_movies (
            title VARCHAR(64) UNIQUE NOT NULL,  
            episode_nb INT PRIMARY KEY,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL, 
            producer VARCHAR(128) NOT NULL, 
            release_date DATE NOT NULL 
            );
"""
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        
        return HttpResponse('OK')
    except Exception as e: 
        return HttpResponse(f"Error: {e}")
        
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
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'])
    
        cur = conn.cursor()

        query = """ 
        INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
        VALUES (%s, %s, %s, %s, %s); 
        """

        for movie in movies:
            try: 
                cur.execute(query, movie) 
                conn.commit()
                result = "OK"
            except Exception as e:
                conn.rollback()
                result = f"{movie[1]}: {e}"
        cur.close()
        conn.close()

        return HttpResponse(result)

    except Exception as e:
        if conn:
            conn.close()
        return HttpResponse(f"Error: {e}")
    
def display(request):
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'])
        
        cur = conn.cursor()
        query = "SELECT * FROM ex02_movies"
        cur.execute(query)
        rows = cur.fetchall()
        if not rows:
            cur.close()
            conn.close()
            return HttpResponse(f"No data available")
        
        html = """
        <table>
            <tr>
                <th>
                    <p>Episode</p>
                </th>
                <th>
                    <p>Title</p>
                </th>
                 <th>
                    <p>Director</p>
                </th>
                 <th>
                    <p>Producer</p>
                </th>
                 <th>
                    <p>Release</p>
                </th>
                <th>
                    <p>Opening</p>
                </th>
            </tr>
                """

        for row in rows:
            html += "<tr>"
            for value in row: 
                html += f"<td>{value if value is not None else ' '}</td>"
            html += "</tr>"
        html += "</table>"
    
        cur.close()
        conn.close()
        return HttpResponse(html)

    except Exception as e: 
        if conn:
            conn.close()
        return HttpResponse(f"Error: {e}")

def remove(request):
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'])
        cur = conn.cursor()
        if request.method == "POST":
            query = f'DELETE FROM ex04_movies WHERE title = %s'
            cur.execute(query, (request.POST["movie"],))
            conn.commit()
        query = "SELECT title FROM ex04_movies"
        cur.execute(query)
        titles = cur.fetchall()
        tab_titles = []
        for title in titles:
            tab_titles.append(title[0])
        return (render(request, "ex04/select.html", {"movies": tab_titles}))
    except Exception as e:
        return (HttpResponse("No data available"))


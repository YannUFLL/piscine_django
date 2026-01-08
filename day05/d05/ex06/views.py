from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import psycopg2


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
            CREATE TABLE IF NOT EXISTS ex06_movies (
            title VARCHAR(64) UNIQUE NOT NULL,  
            episode_nb INT PRIMARY KEY,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL, 
            producer VARCHAR(128) NOT NULL, 
            release_date DATE NOT NULL,
            created TIMESTAMP NOT NULL DEFAULT now(),
            updated TIMESTAMP NOT NULL DEFAULT now()
            );
"""
        cur.execute(query)
        conn.commit()
        query = """
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
            NEW.updated = now();
            NEW.created = OLD.created;
            RETURN NEW;
            END;
            $$ language 'plpgsql';
"""
        cur.execute(query)
        conn.commit()
        query = """DROP TRIGGER IF EXISTS update_films_changetimestamp on ex06_movies"""
        cur.execute(query)
        conn.commit()

        query = """
            CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
            ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
            update_changetimestamp_column();
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
        INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
        VALUES (%s, %s, %s, %s, %s); 
        """

        for movie in movies:
            try: 
                cur.execute(query, movie) 
                conn.commit()
                result += f"{movie[1]}: OK<br>"
            except Exception as e:
                conn.rollback()
                result += f"{movie[1]}: Error, {e}<br>"
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
        query = "SELECT * FROM ex06_movies"
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
                    <p>Title</p>
                </th>
                <th>
                    <p>Episode</p>
                </th>
                <th>
                    <p>Opening</p>
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
                    <p>Created</p>
                </th>
                <th>
                    <p>Updated</p>
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
        if cur:
            cur.close()
        return HttpResponse(f"No data available")

def update(request):
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'])
        cur = conn.cursor()
        if request.method == "POST":
            query = f'UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s'
            cur.execute(query, (request.POST["opening_crawl"], request.POST["movie"],))
            conn.commit()
        query = f'SELECT title FROM ex06_movies'
        cur.execute(query)
        rows = cur.fetchall()
        if rows == []:
            raise Exception("No data available")
        titles = [row[0] for row in rows]
        return (render(request, "ex06/opening_crawl.html", {'movies': titles}))
    except Exception as e:
        return (HttpResponse(f"No data available"))

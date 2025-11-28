from django.shortcuts import render
import psycopg2
from django.conf import settings
from django.http import HttpResponse
import csv

# Create your views here.


def init(request):
    try:

        con = psycopg2.connect(database=settings.DATABASES["default"]["NAME"],
                            user=settings.DATABASES["default"]["USER"],
                            password=settings.DATABASES["default"]["PASSWORD"],
                            host=settings.DATABASES["default"]["HOST"],
                            port=settings.DATABASES["default"]["PORT"])
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ex08_planets (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(64) UNIQUE NOT NULL,
                            climate TEXT, 
                            diameter INTEGER, 
                            orbital_period INTEGER, 
                            population BIGINT, 
                            rotation_period INTEGER,
                            surface_water REAL,
                            terrain TEXT
                    )""" )
        con.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ex08_people (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(64) UNIQUE NOT NULL,
                            birth_year VARCHAR(32),
                            gender VARCHAR(32),
                            eye_color VARCHAR(32),
                            hair_color VARCHAR(32),
                            height INTEGER, 
                            mass REAL,
                            homeworld VARCHAR(64),
                            FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
                    )""" )
        con.commit()
        cursor.close()
        con.close()
        return(HttpResponse("OK"))
    except Exception as e:
        if cursor: 
            cursor.close()
        if (con): 
            con.close()
        return(HttpResponse(f"Error: {e}"))

def sql_value(x):
    return None if x == "NULL" or x == "" else x

def populate(request):
    try:
        con = psycopg2.connect(database=settings.DATABASES["default"]["NAME"],
                                user=settings.DATABASES["default"]["USER"],
                                password=settings.DATABASES["default"]["PASSWORD"],
                                host=settings.DATABASES["default"]["HOST"],
                                port=settings.DATABASES["default"]["PORT"])
        cur = con.cursor() 

        with open('./ex08/planets.csv') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                cur.execute("""
                INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s )""", (
                                sql_value(row[0]),
                                sql_value(row[1]),
                                sql_value(row[2]),
                                sql_value(row[3]),
                                sql_value(row[4]),
                                sql_value(row[5]),
                                sql_value(row[6]),
                                sql_value(row[7])
                            ))
                con.commit()
        with open('./ex08/people.csv') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                print(row)
                cur.execute("""
                INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s )""", (
                                sql_value(row[0]),
                                sql_value(row[1]),
                                sql_value(row[2]),
                                sql_value(row[3]),
                                sql_value(row[4]),
                                sql_value(row[5]),
                                sql_value(row[6]),
                                sql_value(row[7])
                            ))
                con.commit()
        cur.close()
        con.close()
        return (HttpResponse("OK"))
    except Exception as e:
        if cur:
            cur.close() 
        if con:
            con.close()
        return (HttpResponse(f"Type: {type(e)} - Value: {e}"))

def display(request):
    try:

        con = psycopg2.connect(database=settings.DATABASES["default"]["NAME"],
                            user=settings.DATABASES["default"]["USER"],
                            password=settings.DATABASES["default"]["PASSWORD"],
                            host=settings.DATABASES["default"]["HOST"],
                            port=settings.DATABASES["default"]["PORT"])
        cursor = con.cursor()
        cursor.execute(""" SELECT p.name, p.homeworld, pl.climate 
                       FROM ex08_planets pl
                       JOIN ex08_people p 
                        ON p.homeworld = pl.name""")
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        tuples = []
        html = """
<table>
<tr>
    <th>name</th>
    <th>homeworld</th>
    <th>climate</th>
</tr>
"""
        for row in rows:
            print(row[2])
            if "windy" in row[2] or "moderate windy" in row[2]:
                tuples.append(row)
            sorted(tuples, key=lambda x: x[0])

        for tuple in tuples:
                html += f"""
<tr>
    <td>{tuple[0]}</td>
    <td>{tuple[1]}</td>
    <td>{tuple[2]}</td>
</tr>
"""
        html += "</table>"

        return (HttpResponse(html))
    except Exception as e:
        if cursor:
            cursor.close() 
        if con:
            cursor.close() 
        return HttpResponse("No data available")

        
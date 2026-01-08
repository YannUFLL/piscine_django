from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from django.conf import settings

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
            CREATE TABLE IF NOT EXISTS ex00_movies (
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
        return HttpResponse(f"No data available")
        
        
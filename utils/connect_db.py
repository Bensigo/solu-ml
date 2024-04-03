import psycopg2
import os 


DB_URL = os.getenv('DB_URL')

connection = psycopg2.connect(DB_URL)
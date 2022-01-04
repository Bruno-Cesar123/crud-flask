import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

try:
  connection = psycopg2.connect(
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'),
    port=os.environ.get('POSTGRES_PORT'),
    database=os.environ.get('POSTGRES_DATABASE'),
  )

  cursor = connection.cursor()
  print("successfully connection with PostgreSQL ")

except (Exception, Error) as error:
    print("Not possible to PostgreSQL", error)
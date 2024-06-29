#!/usr/bin/env python3

# Ejimofor Nwoye @ Campaign LAB, Newspeak House, London, 22/06/2024

# To scrape the contact information from `https://www.gov.uk/contact-electoral-registration-office` and store it into a PostgreSQL database, you can use the `requests`, `BeautifulSoup`, and `psycopg2` libraries. Here's a step-by-step guide:

# 1. Scrape the data using `requests` and `BeautifulSoup`.
# 2. Store the scraped data into a PostgreSQL database using the `psycopg2` library.

# First, ensure you have the necessary libraries installed:

# pip install requests beautifulsoup4 psycopg2-binary


# Next, here is the complete Python code:


import requests
from bs4 import BeautifulSoup
import psycopg2

# Step 1: Scrape the data

url = "https://www.gov.uk/contact-electoral-registration-office"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the relevant information. Adjust this part according to the actual structure of the HTML.
    offices = []
    articles = soup.find_all('article')
    
    for article in articles:
        office_name = article.find('h2').text.strip()
        address = article.find('div', class_='address').text.strip()
        phone = article.find('div', class_='phone').text.strip() if article.find('div', class_='phone') else ''
        email = article.find('a', class_='email').text.strip() if article.find('a', class_='email') else ''
        
        offices.append({
            "office_name": office_name,
            "address": address,
            "phone": phone,
            "email": email
        })
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()

# Step 2: Store the data in PostgreSQL

# Connect to PostgreSQL

conn = psycopg2.connect(
    dbname="your_database",  # Replace with your database name
    user="your_user",        # Replace with your username
    password="your_password",# Replace with your password
    host="localhost",        # Replace with your database host
    port="5432"              # Replace with your database port
)
cur = conn.cursor()

# Create table if not exist

cur.execute("""
    CREATE TABLE IF NOT EXISTS electoral_offices (
        id SERIAL PRIMARY KEY,
        office_name TEXT,
        address TEXT,
        phone TEXT,
        email TEXT
    )
""")

# Insert data into PostgreSQL

insert_query = """
    INSERT INTO electoral_offices (office_name, address, phone, email) VALUES (%s, %s, %s, %s)
"""

for office in offices:
    cur.execute(insert_query, (office['office_name'], office['address'], office['phone'], office['email']))

# Commit changes and close connection

conn.commit()
cur.close()
conn.close()

print("Data successfully inserted into PostgreSQL")

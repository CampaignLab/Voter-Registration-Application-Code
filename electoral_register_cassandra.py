#!/usr/bin/env python3

# Ejimofor Nwoye @ Campaign Lab, Newspeak House, London, 22/06/2024

# To scrape the contact information from `https://www.gov.uk/contact-electoral-registration-office` and store it into Apache Cassandra, you need to follow these steps:

# 1. Scrape the data using `requests` and `BeautifulSoup`.
# 2. Store the scraped data into an Apache Cassandra database using the `cassandra-driver` library.

# First, ensure you have the necessary libraries installed:

# pip install requests beautifulsoup4 cassandra-driver


# Next, here is the complete Python code:


import requests
from bs4 import BeautifulSoup
from cassandra.cluster import Cluster

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

# Step 2: Store the data in Apache Cassandra
# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra cluster address
session = cluster.connect()

# Create keyspace and table if not exist
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS electoral_offices WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS electoral_offices.contacts (
        id UUID PRIMARY KEY,
        office_name TEXT,
        address TEXT,
        phone TEXT,
        email TEXT
    )
""")

# Insert data into Cassandra
from uuid import uuid4

insert_statement = session.prepare("""
    INSERT INTO electoral_offices.contacts (id, office_name, address, phone, email) VALUES (?, ?, ?, ?, ?)
""")

for office in offices:
    session.execute(insert_statement, (uuid4(), office['office_name'], office['address'], office['phone'], office['email']))

print("Data successfully inserted into Apache Cassandra")

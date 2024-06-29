#!/usr/bin/env python3

# Ejimofor Nwoye, Campaign Lab, Newspeak House, London, 22/06/2024

# 1. First, make sure you have the required libraries installed:
   
#    pip install requests beautifulsoup4
    

# 2. Then, you can use the following code to scrape the data:

    
    import requests

    from bs4 import BeautifulSoup

    url = "https://www.gov.uk/contact-electoral-registration-office"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the relevant information. This part may vary depending on the structure of the HTML.
        # Here, let's assume the contact information is within 'article' tags
        articles = soup.find_all('article')

        for article in articles:
            office_name = article.find('h2').text.strip()
            address = article.find('div', class_='address').text.strip()
            phone = article.find('div', class_='phone').text.strip()
            email = article.find('a', class_='email').text.strip()
            
            print(f"Office Name: {office_name}")
            print(f"Address: {address}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print("-" * 40)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    

from bs4 import BeautifulSoup
import pandas as pd
import requests
import lxml
import re

# Web Scraper to Find Kitten & Cat Keywords on Vancouver Craigslist Pet Section

url = "https://vancouver.craigslist.org/d/pets/search/pet"

# Create Dictionary
d = {'key' : 'value'}

# Update Dictionary
d['new key'] = 'new value'

pet_kittens = {}
cat_no = 0
cat_store = 0
confirm = 0

print('...Finding Cats 😸 ...')

while True:

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    keyword = ['kitten', 'kittens', 'cat', 'cats']

    kittens = soup.find_all('p', {'class' : 'result-info'})


    for kitty in kittens:

        kitty_tag = kitty.find('a', text = re.compile(r'\b(?:%s)\b' % '|'.join(keyword), re.IGNORECASE), attrs = {'class' : 'result-title'})
        title = kitty_tag.text if kitty_tag else "Kitty Haters!"

        pussy = title != "Kitty Haters!"

        location_tag = kitty.find('span', {'class' : 'result-hood'})
        location = location_tag.text if location_tag else "N/A"

        date = kitty.find('time', {'class' : 'result-date'}).text
        link = kitty.find('a', {'class' : 'result-title'}).get('href')

        kitty_response = requests.get(link)
        kitty_data = kitty_response.text
        kitty_soup = BeautifulSoup(kitty_data, 'lxml')
        kitty_description = kitty_soup.find('section', {'id' : 'postingbody'}).text

   
        if pussy:
            cat_no += 1
            pet_kittens[cat_no] = [title, location, date, link, kitty_description]
            confirm = 1


    url_tag = soup.find('a', {'title' : 'next page'})
    if url_tag.get('href'):
        url = 'https://vancouver.craigslist.org' + url_tag.get('href')
        print('Found Kittens!! 😻 \nKitten/Cat Keyword Count: ' + str(cat_no)) if confirm == 1 else 0
        cat_store += cat_no
    else:
        break
            

print("Total Matched Kitten/Cat Word Count 🐈😽: ", cat_store)

pet_kittens_df = pd.DataFrame.from_dict(pet_kittens, orient = 'index', columns = ['Title', 'Location', 'Date', 'Link', 'Kitty Description'])
pet_kittens_df.head()

pet_kittens_df.to_csv('kitten_data.csv')

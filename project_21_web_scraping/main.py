import requests
from bs4 import BeautifulSoup as bs


github_user = input('Input GitHub Username: ')

url = 'https://github.com/' + github_user 

r = requests.get(url)
soup = bs(r.content , 'html.parser')

profile_image_tag = soup.find('img', {'alt': f'@{github_user}'})
    
if profile_image_tag:
    profile_image = profile_image_tag.get('src')
    print(f"Profile Image URL: {profile_image}")
else:
    print(f"Profile Image not found for user: {github_user}")




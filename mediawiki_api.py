import datetime
import requests
from constants import secrets, APP_NAME, EMAIL_OR_CONTACT_PAGE

today = datetime.datetime.now()
date_string = today.strftime('%Y/%m/%d')
base_url = "https://api.wikimedia.org"

headers = {
  'Authorization': f'Bearer {secrets["ACCESS_TOKEN"]}',
  'User-Agent': f'{APP_NAME} ({EMAIL_OR_CONTACT_PAGE})'
}

def get_data(url):
  response = requests.get(url, headers=headers)
  data = response.json()
  return data

def make_url_and_get_data(url_suffix):
  return get_data(base_url + url_suffix)

def get_page(project, language, title):
  return make_url_and_get_data(f"/core/v1/{project}/{language}/page/{title}/bare")

def get_page_offline(project, language, title):
  return make_url_and_get_data(f"/core/v1/{project}/{language}/page/{title}/with_html")

def get_wikipedia_featured_content(language, date_string):
  return make_url_and_get_data(f"/feed/v1/wikipedia/{language}/featured/{date_string}")
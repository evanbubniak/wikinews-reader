import requests
from constants import APP_NAME, EMAIL_OR_CONTACT_PAGE
from urllib.parse import quote

headers = {
  'User-Agent': f'{APP_NAME} ({EMAIL_OR_CONTACT_PAGE})'
}

def get_interlanguage_links(lang_code, title):
  request = f"api.php?action=query&prop=langlinks&titles={quote(title)}&redirects=&format=json&lllimit=500"
  response = get_request_response(lang_code, request)
  lang_objs = list(response['query']['pages'].values())[0]['langlinks'].copy()
  while response.get('continue'):
    response = get_request_response(lang_code, request + f"&llcontinue={response['continue']['llcontinue']}")
    lang_objs.extend(list(response['query']['pages'].values())[0]['langlinks'])
  return {lang_obj['lang']:lang_obj['*'] for lang_obj in lang_objs}


def get_main_page_title(lang_code):
  request = "api.php?action=query&format=json&meta=siteinfo&formatversion=2"
  response = get_request_response(lang_code, request)
  return response["query"]["general"]["base"].split("/")[-1]

def get_page_info_from_category(lang_code, category):
  request = f"api.php?action=query&generator=categorymembers&gcmtitle=Category:{category}&prop=info&format=json"
  return get_request_response(lang_code, request)

def get_page_json_from_category(lang_code, category):
  request = f"api.php?action=query&generator=categorymembers&gcmtitle=Category:{category}&prop=revisions&rvslots=*&rvprop=content&format=json"
  return get_request_response(lang_code, request)

def get_page_json(lang_code, title):
  request = f"api.php?action=query&prop=revisions&titles={title}&rvslots=*&rvprop=content&format=json"
  return get_request_response(lang_code, request)

def get_page_plaintext(lang_code, title):
  request = f"api.php?action=query&titles={title}&prop=extracts&exintro&explaintext&format=json"
  return get_request_response(lang_code, request)

# gcmlimit and exlimit may be set to a string "max"
def get_page_plaintext_from_category(lang_code, category, num_articles_to_return = 10, exintro=True, exlimit='max'):
  if not exintro:
    num_articles_to_return = 1
    exlimit = 1
  request = f"api.php?action=query&generator=categorymembers&gcmtitle=Category:{category}{f'&gcmlimit={num_articles_to_return}' if num_articles_to_return else ''}&gcmsort=timestamp&gcmdir=desc&prop=extracts{'&exintro' if exintro else ''}{f'&exlimit={exlimit}' if exlimit else ''}&explaintext&format=json"
  return get_request_response(lang_code, request)

def get_request_response(lang_code, request):
  url = f"https://{lang_code}.wikinews.org/w/{request}"
  response = requests.get(url, headers=headers)
  return response.json()


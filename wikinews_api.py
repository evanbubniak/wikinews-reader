import requests
from constants import APP_NAME, EMAIL_OR_CONTACT_PAGE

headers = {
  'User-Agent': f'{APP_NAME} ({EMAIL_OR_CONTACT_PAGE})'
}

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
  request = f"api.php?action=query&format=json&titles={title}&prop=extracts&exintro&explaintext&format=json"
  return get_request_response(lang_code, request)

def get_page_plaintext_from_category(lang_code, category):
  request = f"api.php?action=query&generator=categorymembers&gcmtitle=Category:{category}&prop=extracts&exintro&explaintext&format=json"
  return get_request_response(lang_code, request)

def get_request_response(lang_code, request):
  url = f"https://{lang_code}.wikinews.org/w/{request}"
  response = requests.get(url, headers=headers)
  return response.json()


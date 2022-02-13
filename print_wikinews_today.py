from wikinews_api import get_page_plaintext_from_category

import datetime
from babel.dates import format_date

today = datetime.date.today()

def wikinews_format_date(date, lang_code):
  if lang_code == "de":
    return today.strftime("%d.%m.%Y")
  else:
    category = format_date(date, format="long", locale=lang_code).replace(" ", "_")
    if lang_code == "en":
      category = category.replace(",", "")
    return category

def print_article_content(page_object):
  print(f"Title: {page_object['title']}\n")
  print(f"Content: {page_object['revisions'][0]['slots']['main']['*']}")

def print_article_extract(page_extract_object):
  print(f"Title: {page_extract_object['title']}")
  print(f"Content: {page_extract_object['extract']}\n")
# page_json = get_page_json_from_category(lang_code, category)

for lang_code in ["fr", "es", "it", "nl", "zh", "de", "ja"]:
  category = wikinews_format_date(today, lang_code)
  page_json = get_page_plaintext_from_category(lang_code, category)
  if page_json.get("query"):
    print(f"{lang_code}: {len(page_json['query']['pages'])} articles found")
    for page_object in page_json["query"]["pages"].values():
      print_article_extract(page_object)
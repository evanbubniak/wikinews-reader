from typing import Dict, List
from wikinews_api import get_page_plaintext_from_category
from text_processing import preprocess_article_text
import datetime
from babel.dates import format_date
from urllib.parse import quote

today = datetime.date.today()

titles_to_exclude = ["中文報紙頭條", "短信:"]

def wikinews_format_date(date, lang_code):
  if lang_code == "de":
    return today.strftime("%d.%m.%Y")
  else:
    category = format_date(date, format="long", locale=lang_code).replace(" ", "_")
    if lang_code == "en":
      category = category.replace(",", "")
    return category

def title_to_url(title, lang_code):
  encoded_title = quote(title)
  return f"https://{lang_code}.wikinews.org/wiki/{encoded_title}"

def print_article_content(page_object):
  print(f"Title: {page_object['title']}\n")
  print(f"Content: {page_object['revisions'][0]['slots']['main']['*']}")

def print_article_extract(page_extract_object, lang_code):
  print(f"Title: {page_extract_object['title']}")
  print(f"Content: {preprocess_article_text(page_extract_object['extract'], lang_code)}")
  print(f"URL: {title_to_url(page_extract_object['title'], lang_code)}\n")
# page_json = get_page_json_from_category(lang_code, category)

def page_object_has_content(page_object):
  return page_object.get("extract") and not any([title_to_exclude in page_object["title"] for title_to_exclude in titles_to_exclude])

lang_codes = ["fr", "es", "it", "nl", "zh", "de", "ja"]
page_jsons_by_lang: Dict[str, List[dict]] = {}
for lang_code in lang_codes:
  days = [today + datetime.timedelta(days=num_days) for num_days in range(-1,2)]
  categories = [wikinews_format_date(day, lang_code) for day in days]
  page_jsons_by_lang[lang_code] = [get_page_plaintext_from_category(lang_code, category) for category in categories]

for lang_code in lang_codes:
  page_jsons = page_jsons_by_lang[lang_code]
  for page_json in page_jsons:
      if page_json.get("query"):
        filtered_page_objects = list(filter(page_object_has_content, page_json["query"]["pages"].values()))
        if len(filtered_page_objects) > 0:
          print(f"{lang_code}: {len(filtered_page_objects)} articles found")
          for page_object in filtered_page_objects:
            print_article_extract(page_object, lang_code)
from itertools import chain
from typing import Dict, List
from get_x_most_recent import get_pages_from_response
from wikinews_api import get_page_plaintext_from_category
from text_processing import page_extract_object_to_article
import datetime
from babel.dates import format_date


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

def page_extract_has_content(page_extract_object):
  return page_extract_object.get("extract") and not any([title_to_exclude in page_extract_object["title"] for title_to_exclude in titles_to_exclude])


lang_codes = ["fr", "es", "it", "nl", "zh", "de", "ja"]
articles_by_lang: Dict[str, List[dict]] = {}
for lang_code in lang_codes:
  days = [today + datetime.timedelta(days=num_days) for num_days in range(-1,2)]
  categories = [wikinews_format_date(day, lang_code) for day in days]
  responses_by_category = [get_page_plaintext_from_category(lang_code, category) for category in categories]
  page_extracts_by_category = [get_pages_from_response(response) for response in responses_by_category]
  page_extracts = list(chain.from_iterable(page_extracts_by_category))
  articles_by_lang[lang_code] = [page_extract_object_to_article(page_extract, lang_code) for page_extract in page_extracts]

for lang_code in lang_codes:
  articles = list(filter(lambda article: not any([title_to_exclude in article["title"] for title_to_exclude in titles_to_exclude]), articles_by_lang[lang_code]))
  if len(articles) > 0:
    print(f"{lang_code}: {len(articles)} articles found")
  for article in articles:
    print(article)
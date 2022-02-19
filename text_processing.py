from article import Article
from urllib.parse import quote
import re
regex_matching_spaces_between_nonascii_chars = r"(?<=(?![A-Za-z])[^\W\d_])\s+(?=(?![A-Za-z])[^\W\d_])"

def preprocess_article_text(article_text, lang_code):
  if lang_code in ["zh", "ja"]:
    return re.sub(regex_matching_spaces_between_nonascii_chars, "", article_text)
  else:
    return article_text

def title_to_url(title, lang_code):
  encoded_title = quote(title)
  return f"https://{lang_code}.wikinews.org/wiki/{encoded_title}"

def print_article_content(page_object):
  print(f"Title: {page_object['title']}\n")
  print(f"Content: {page_object['revisions'][0]['slots']['main']['*']}")


def page_extract_object_to_article(page_extract_object, lang_code):
    return Article(
        title = page_extract_object['title'],
        content = preprocess_article_text(page_extract_object['extract'], lang_code),
        url = title_to_url(page_extract_object['title'], lang_code)
    )

def print_article_extract(article):
  print(f"Title: {article['title']}")
  print(f"Content: {article['content']}")
  print(f"URL: {article['url']}\n")
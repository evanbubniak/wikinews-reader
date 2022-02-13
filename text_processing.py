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

def print_article_extract(article):
  print(f"Title: {article['title']}")
  print(f"Content: {article['content']}")
  print(f"URL: {article['url']}\n")
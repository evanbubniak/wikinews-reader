import re
regex_matching_spaces_between_nonascii_chars = r"(?<=(?![A-Za-z])[^\W\d_])\s+(?=(?![A-Za-z])[^\W\d_])"

def preprocess_article_text(article_text, lang_code):
  if lang_code in ["zh", "ja"]:
    return re.sub(regex_matching_spaces_between_nonascii_chars, "", article_text)
  else:
    return article_text
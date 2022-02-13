from unittest.mock import DEFAULT
from wikinews_api import get_interlanguage_links, get_page_plaintext_from_category
from typing import Dict, List
from text_processing import preprocess_article_text, print_article_extract, title_to_url

x = 1
DEFAULT_LANG_CODES = ["fr", "es", "it", "nl", "zh", "de", "ja"]


def get_x_most_recent(x=1, lang_codes=DEFAULT_LANG_CODES):
    published_categories_by_lang = get_interlanguage_links(
        "en", "Category:Published")
    responses_by_lang: Dict[str, dict] = {lang_code: get_page_plaintext_from_category(
        lang_code, published_categories_by_lang[lang_code].split(":")[1], num_articles_to_return=x) for lang_code in lang_codes}
    articles_by_lang = {
        lang_code: [page_extract_object_to_article(page_extract_object, lang_code)
                    for page_extract_object in get_pages_from_response(responses_by_lang[lang_code])
                    ]
        for lang_code in lang_codes
    }
    return articles_by_lang


def get_pages_from_response(response):
    if response.get("query"):
        return list(response["query"]["pages"].values())
    else:
        return []


def page_extract_object_to_article(page_extract_object, lang_code):
    return {"title": page_extract_object['title'], "content": preprocess_article_text(page_extract_object['extract'], lang_code), "url": title_to_url(page_extract_object['title'], lang_code)}


if __name__ == "__main__":
    lang_codes = DEFAULT_LANG_CODES
    articles_by_lang = get_x_most_recent(1, lang_codes)
    for lang_code in lang_codes:
        print(f"{lang_code}: {len(articles_by_lang[lang_code])} articles")
        for article in articles_by_lang[lang_code]:
            print_article_extract(article)

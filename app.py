import curses
from curses import wrapper
from itertools import chain
from enum import IntEnum
from math import ceil
from get_x_most_recent import get_x_most_recent, DEFAULT_LANG_CODES
import locale
locale.setlocale(locale.LC_ALL, '')

class CursorStates(IntEnum):
    INVISIBLE = 0
    NORMAL = 1
    VERY_VISIBLE = 2

ESCAPE_CODE = 27

def reached_end(current_row, final_cursor_y):
    return any([final_cursor_y < curses.LINES-1, current_row + curses.LINES > final_cursor_y])

def keyup(ch):
    return (ch == curses.KEY_UP or ch == ord("k"))

def keydown(ch):
    return (ch == curses.KEY_DOWN or ch == ord("j"))

def keyenter(ch):
    return ch in [curses.KEY_ENTER, 10, 13]

def format_article_str(article):
    return f"{article.get_title()}\n\n{article.get_content()}\n\n{article.get_url()}\n\nPress any key to quit"

def display_article_menu(pad, articles, highlighted_row):
    offset = 0
    for i, article in enumerate(articles):
        attr = curses.A_BOLD if i == highlighted_row else curses.A_DIM
        pad.addstr(i+offset, 0, f"{article.get_short_title()}", attr)
        offset += ceil(len(article.get_short_title())/curses.COLS) - 1   
    return offset

def enter_article_menu(articles):
    top_row = 0
    highlighted_row = 0
    max_rows_needed = sum([ceil(len(article.get_short_title())*2/curses.COLS) for article in articles])
    pad = curses.newpad(max_rows_needed, curses.COLS)
    fake_pad = curses.newpad(max_rows_needed, curses.COLS)
    pad.keypad(True)
    pad_rows = curses.LINES
    pad_cols = curses.COLS
    refresh = True

    while True:
        if curses.COLS == 0 or curses.LINES == 0:
            continue

        if refresh:
            curses.curs_set(CursorStates.INVISIBLE)    
            offset = display_article_menu(fake_pad, articles, 0)
            final_cursor_y, final_cursor_x = fake_pad.getyx()
            pad.erase()
            pad.resize(final_cursor_y+1+offset, curses.COLS)
            display_article_menu(pad, articles, highlighted_row)
            # pad.addstr(highlighted_row, 0, f"(rows:{curses.LINES} cols:{curses.COLS} max_rows:{max_rows_needed} offset:{offset} articles:{len(articles)})")
            pad.refresh(top_row, 0, 0, 0, curses.LINES-1, curses.COLS)
        key = pad.getch()
        if key == ESCAPE_CODE:
            break
        else:
            curses.update_lines_cols()
            if curses.LINES != pad_rows or curses.COLS != pad_cols:
                pad_rows = curses.LINES
                pad_cols = curses.COLS
                refresh = True
            if highlighted_row != 0 and keyup(key):
                highlighted_row -= 1
                if highlighted_row - top_row <= ceil(curses.LINES/2):
                    top_row -= 1
                refresh = True
            if highlighted_row != (len(articles)-1) and keydown(key):
                highlighted_row += 1
                if highlighted_row - top_row > ceil(curses.LINES/2):
                    if len(articles) - top_row + 1 > curses.LINES:
                        top_row += 1
                refresh = True

            if keyenter(key):
                pad.erase()
                pad.refresh(top_row, 0, 0, 0, max(curses.LINES-offset, 0), curses.COLS)
                enter_article(articles[highlighted_row])
                refresh = True

def display_article(pad, article_str):
    pad.addstr(article_str.encode('utf-8'))

def enter_article(article):
    article_str = format_article_str(article)
    num_article_str_newlines = article_str.count("\n")
    current_row = 0
    max_rows_needed = (ceil((len(article_str) - num_article_str_newlines)/(curses.COLS)) + num_article_str_newlines)*2
    pad = curses.newpad(max_rows_needed, curses.COLS)
    fake_pad = curses.newpad(max_rows_needed, curses.COLS)
    pad.keypad(True)
    pad_rows = curses.LINES
    pad_cols = curses.COLS

    refresh = True
    while True:
        if curses.COLS == 0 or curses.LINES == 0:
            continue

        if refresh:
            fake_pad.erase()
            display_article(fake_pad, article_str)
            final_cursor_y, final_cursor_x = fake_pad.getyx()
            pad.erase()
            pad.resize(final_cursor_y+num_article_str_newlines, curses.COLS)
            display_article(pad, article_str)
            pad.refresh(current_row, 0, 0, 0, curses.LINES-1, curses.COLS)
        refresh = False
        ch = pad.getch()
        if not ch == curses.KEY_RESIZE and (ch==ESCAPE_CODE or (reached_end(current_row, final_cursor_y) and not (keyup(ch) and current_row !=0))):
            break
        else:
            curses.update_lines_cols()
            if curses.LINES != pad_rows or curses.COLS != pad_cols:
                pad_rows = curses.LINES
                pad_cols = curses.COLS
                max_rows_needed = (ceil((len(article_str) - num_article_str_newlines)/(curses.COLS)) + num_article_str_newlines)*2
                fake_pad.resize(max_rows_needed, curses.COLS)
                refresh = True
            if current_row != 0 and keyup(ch):
                current_row -= 1
                refresh = True
            if keydown(ch):
                current_row += 1
                refresh = True
                

    pad.erase()
    pad.refresh(0, 0, 0, 0, curses.LINES-1, curses.COLS)


def get_wikinews_articles(n, lang_codes):
    articles_by_lang = get_x_most_recent(n, lang_codes)
    articles = list(chain.from_iterable(articles_by_lang.values()))
    return articles

def main(stdscr):
    articles = get_wikinews_articles(3, DEFAULT_LANG_CODES)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    enter_article_menu(articles)
    curses.curs_set(CursorStates.NORMAL)
wrapper(main)
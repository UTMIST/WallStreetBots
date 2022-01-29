from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://finviz.com/quote.ashx?t='


def get_raw_ticker(ticker):
    """
    return raw html finviz page for a ticker
    :param ticker: string
    :return: news_table: bs4.element.Tag (table of raw html tags)
    """
    url = base_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    response = urlopen(req)
    html = BeautifulSoup(response)
    news_table = html.find(id='news-table')
    return news_table


def tag_to_table(html_tag):
    """
    turns a table of html tags to a table of data
    :param html_tag: bs4.element.Tag
    :return: table: nested list
    """
    html_tag = html_tag.findAll('tr')

    # table format: date, time, header, link
    table = [['date', 'time', 'header', 'link']]
    pivot_date = ''
    for i, table_row in enumerate(html_tag):
        # Read the text of the element 'td' into 'data_text'; date/time
        td_text = table_row.td.text
        # Read the text of the element 'a' into 'link_text'; text
        a_text = table_row.a.text
        # Read link from a; link
        link_text = table_row.a['href']
        # Print the contents of 'link_text' and 'data_text'
        temp = td_text.split()
        time = ''
        if len(temp) == 2:
            pivot_date = temp[0]
            time = temp[1]
        else:
            time = temp[0]
        table.append([pivot_date, time, a_text, link_text])
    return table


def get_news(ticker):
    html_tag = get_raw_ticker(ticker)
    table = tag_to_table(html_tag)
    return pd.DataFrame(table[1:], columns=table[0])


if __name__ == '__main__':
    news = get_news('amzn')
    print(news)

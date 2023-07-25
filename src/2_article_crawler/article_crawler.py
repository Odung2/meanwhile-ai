import pandas as pd

from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

import requests
from requests.exceptions import SSLError, RequestException

from urllib.parse import urlparse

def input_csv():
    return pd.read_csv('data/raw_data/rss_part1.csv', sep=';')

def get_article_domain(url):
    domain = urlparse(url).netloc
    return domain

# 도메인-검색조건 맵핑 설정
domain_conditions_map = {
    "www.cj-ilbo.com": {'tag': 'article', 'id': 'article-view-content-div'},
    "www.mediatoday.asia": {'tag': 'div', 'id': 'textinput'},
    "www.inews365.com": {'tag': 'div', 'class': 'article'},
    "www.jbnews.com": {'tag': 'article', 'id': 'article-view-content-div'},
    "www.seongdongnews.com": {'tag': 'div', 'id': 'article-view-content-div'},
    "world.kbs.co.kr": {'tag': 'div', 'class': 'body_txt fr-view'},
    "mobile.newsis.com": {'tag': 'article'},
    "www.monthlypeople.com": {'tag': 'div', 'id': 'article-view-content-div'},
    "www.asiatoday.co.kr": {'tag': 'div', 'class': 'news_bm'},
    "hugs.fnnews.com": {'tag': 'div', 'class': 'art_content'},
    "www.sportsworldi.com": {'tag': 'article', 'class': 'viewBox2'},
    "www.brandbrief.co.kr": {'tag': 'div', 'id': 'article-view-content-div'},
    "www.businesspost.co.kr": {'tag': 'div', 'class': 'detail_editor'},
    "www.yna.co.kr": {'tag': 'article', 'class': 'story-news article'},
    "news.kbs.co.kr": {'tag': 'div', 'class': 'landing-box'},
}

def find_article_body(soup, url):
    domain = get_article_domain(url)
    condition = domain_conditions_map.get(domain, {})

    if not condition:
        return None

    tag = condition.get('tag')
    if tag:
        condition.pop('tag')
        article_body = soup.find(tag, condition)
    else:
        article_body = soup.find(condition)

    return article_body

"""
    기사 본문이 여러 HTML 태그에 담겨 있을 때 처리 코드

    article_body = soup.new_tag("div")
    for body_condition in search_condition:
        tag = body_condition.pop('tag', None)
        if tag:
            article_body.append(soup.find(tag, body_condition))
        else:
            article_body.append(soup.find(body_condition))
    
    return article_title, article_body
"""

def get_article_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 클래스 이름 중에서 조건에 맞는 첫 번째 결과를 찾습니다.
        article_body = find_article_body(soup, url)

        if article_body is not None:
            article_image = article_body.find("img")
            if article_image is not None:
                article_image = article_image.get("src")

            article_body = article_body.get_text(separator=' ', strip=True).replace('\n', ' ')
        else:
            article_image = None

        return article_image, article_body
    else:
        return None, None

def append_article(df):
    redirect = []
    redirectLink = []
    articleImage = []
    articleBody = []
    
    with tqdm(total=len(df), unit="tasks", bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt} [{elapsed}]") as progress_bar:
        for _, row in df.iterrows():
            url = row['link']
            try:
                response = requests.get(url)
                article_image, article_body = get_article_text(response.url)

                redirect.append("True")
                redirectLink.append(response.url)
                articleImage.append(article_image)
                articleBody.append(article_body)
            except SSLError:
                redirect.append("False")
                redirectLink.append("SSLError")
                articleImage.append(None)
                articleBody.append(None)
            except RequestException:
                redirect.append("False")
                redirectLink.append("RequestException")
                articleImage.append(None)
                articleBody.append(None)
            # row.append(f";{get_article_text(row[1])}")

            progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.

    df['redirect'] = pd.Series(redirect + [False] * (len(df) - len(redirect)))
    df['redirectLink'] = pd.Series(redirectLink + ["NotExecuted"] * (len(df) - len(redirectLink)))
    df['articleImage'] = pd.Series(articleImage + [None] * (len(df) - len(articleImage)))
    df['articleBody'] = pd.Series(articleBody + [None] * (len(df) - len(articleBody)))

def output_csv(df):
    df.to_csv('data/raw_data/rss_part2.csv', sep=';', index=False)

if __name__ == '__main__':
    print("Step 2-2: Crawling article body... ")

    df = input_csv()
    append_article(df)
    output_csv(df)

    print("Complete!!!\n")
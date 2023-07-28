import pandas as pd

from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

import requests
from requests.exceptions import SSLError, RequestException, Timeout

from urllib.parse import urlparse

def input_csv():
    return pd.read_csv('data/processed_data/2_article_crawler/rss_part1.csv', sep=';')

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
    "biz.chosun.com": {'tag': 'section', 'class': 'article-body'},
    "www.hani.co.kr": {'tag': 'div', 'class': 'text'},
    "www.seoul.co.kr": {'tag': 'div', 'class': 'S20_v_article'},
    "www.senews.kr": {'tag': 'div', 'id': 'textinput'},
    "mdtoday.co.kr": {'tag': 'div', 'id': 'articleBody'},
    "www.wowtv.co.kr": {'tag': 'div', 'class': 'box-news-body'},
    "www.newspim.com": {'tag': 'div', 'class': 'bodynews'},
    "www.getnews.co.kr": {'tag': 'article', 'id': 'article-view-content-div'},
    "www.dt.co.kr": {'tag': 'div', 'class': 'article_view'},
    "www.inven.co.kr": {'tag': 'div', 'id': 'imageCollectDiv'},
    "zdnet.co.kr": {'tag': 'div', 'id': 'content-20230727111416'},
    "bloomingbit.io": {'tag': 'section', 'id': 'container'},
    "hypebeast.kr": {'tag': 'div', 'class': 'post-body-content'},
    

    "hitsdailydouble.com": {'tag': 'div', 'class': 'hits_news_detail_post'},
    "www.forbes.com": {'tag': 'div', 'class': 'article-body fs-article fs-responsive-text current-article'},
    "www.billboard.com": {'tag': 'div', 'class': 'a-content lrv-a-floated-parent lrv-a-glue-parent a-font-body-m'},
    "www.koreaboo.com": {'tag': 'div', 'class': 'entry-content'},
    "www.sportskeeda.com": {'tag': 'div', 'id': 'article-content'},
    "www.bnd.com": {'tag': 'article', 'class': 'paper story-body'},
    "www.bbc.com": {'tag': 'article', 'class': 'ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6'},
    "www.sidneydailynews.com": {'tag': 'div', 'class': 'td-post-content tagdiv-type'},
    "www.news8000.com": {'tag': 'div', 'class': 'col-lg-12 col-md-12 col-sm-12'},
    "tech.hindustantimes.com": {'tag': 'div', 'class': 'storyContent'},
    "www.sportskeeda.com": {'tag': 'div', 'id': 'article-content'},
    "www.techlusive.in": {'tag': 'div', 'class': 'lhs-col art-details'},
    "www.businesswire.com": {'tag': 'article', 'class': 'bw-release-main'},
    "fortune.com": {'tag': 'div', 'data-cy': 'articleContent'},
    "www.businessinsider.com": {'tag': 'div', 'class': 'content-lock-content'},
    "www.dailymail.co.uk": {'tag': 'div', 'itemprop': 'articleBody'},
    "electrek.co": {'tag': 'div', 'class': 'container med post-content'},
    "www.bloomberg.com": {'tag': 'main', 'class': 'dvz-content'},
    "www.foxbusiness.com": {'tag': 'div', 'class': 'article-body'},
    "www.forbes.com": {'tag': 'div', 'class': 'article-body fs-article fs-responsive-text current-article'},
    "www.foxnews.com": {'tag': 'div', 'class': 'article-body'},
    "abcnews.go.com": {'tag': 'article', 'class': 'xvlf ZRif TKoO eaKK '},
    "www.bbc.com": {'tag': 'article', 'class': 'ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6'},
    "edition.cnn.com": {'tag': 'div', 'class': 'article__content'},
    "www.ft.com": {'tag': 'div', 'class': 'article__content-body n-content-body js-article__content-body'},
    "www.nknews.org": {'tag': 'div', 'class': 'content-wrapper'},
    "www.reuters.com": {'tag': 'div', 'class': 'article-body__content__17Yit'},
    "www.independent.co.uk": {'tag': 'div', 'class': 'sc-cvxyxr-6 qQMkz sc-cvxyxr-8 kuyHvt'},
    "news.sky.com": {'tag': 'div', 'class': 'sdc-article-body sdc-article-body--story sdc-article-body--lead'},
    "nypost.com": {'tag': 'div', 'class': 'single__content entry-content m-bottom '},
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
    try:
        response = requests.get(url, timeout=2)
    except Timeout:
        return None, None

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

from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def append_article(df):
    start_time = time.time()

    redirect = []
    redirectLink = []
    articleImage = []
    articleBody = []

    with tqdm(total=len(df), unit="tasks", bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt} [{elapsed}]") as progress_bar:
        for _, row in df.iterrows():
            url = row['link']
            try:
                # executor = ThreadPoolExecutor(max_workers=1)
                # with ThreadPoolExecutor(max_workers=1) as executor:
                # future = executor.submit(requests.get, url, timeout=2)

                # try:
                #     response = future.result()
                #     article_image, article_body =  get_article_text(response.url)

                #     redirect.append(True)
                #     redirectLink.append(response.url)
                #     articleImage.append(article_image)
                #     articleBody.append(article_body)
                # except TimeoutError:
                #     future.cancel()
                    
                #     redirect.append(False)
                #     redirectLink.append("TimeoutError")
                #     articleImage.append(None)
                #     articleBody.append(None)

                response = requests.get(url, timeout=2)
                article_image, article_body = get_article_text(response.url)

                try:
                    image_response = requests.head(article_image, timeout=2)
                    # URL에 접속해서 상태 코드가 200 (정상)인 경우에만 True를 반환합니다.
                    if image_response.status_code == 200:
                        article_image = None
                except:
                    # 요청 중 예외가 발생하면 False를 반환합니다.
                    article_image = None

                redirect.append(True)
                redirectLink.append(response.url)
                articleImage.append(article_image)
                articleBody.append(article_body)
            except SSLError:
                redirect.append(False)
                redirectLink.append("SSLError")
                articleImage.append(None)
                articleBody.append(None)
            except RequestException:
                redirect.append(False)
                redirectLink.append("RequestException")
                articleImage.append(None)
                articleBody.append(None)
            except Timeout:
                redirect.append(False)
                redirectLink.append("Timeout")
                articleImage.append(None)
                articleBody.append(None)
            # row.append(f";{get_article_text(row[1])}")

            progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.

            if time.time() - start_time > 60:
                break

    df['redirect'] = pd.Series(redirect + [False] * (len(df) - len(redirect)))
    df['redirectLink'] = pd.Series(redirectLink + ["NotExecuted"] * (len(df) - len(redirectLink)))
    df['articleImage'] = pd.Series(articleImage + [None] * (len(df) - len(articleImage)))
    df['articleBody'] = pd.Series(articleBody + [None] * (len(df) - len(articleBody)))

    df = df.query("redirect != False")
    # df = df.drop('redirect', axis=1)

    return df

def output_csv(df):
    df.to_csv('data/processed_data/2_article_crawler/rss_part2.csv', sep=';', index=False)

if __name__ == '__main__':
    print("Step 2-3: Crawling article body... ")

    df = input_csv()
    df = append_article(df)
    output_csv(df)

    print("Complete!!!\n")

    quit()
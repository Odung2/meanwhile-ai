import pandas as pd
"""
from tqdm import tqdm
import sys
from pathlib import Path

import os
target_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(target_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meanwhile.settings")

import django
django.setup()

from articles.models import Article
"""
def input_csv():
    return pd.read_csv('data/processed_data/4_article_keyword/rss_part4.csv', sep=';', keep_default_na=False)

def input_db():
    return pd.read_csv('data/processed_data/database.csv', sep=';', keep_default_na=False)

def output_csv(df):
    df.to_csv('data/processed_data/5_article_final/rss_part5.csv', sep=';', index=False)

def output_db(df):
    df.to_csv('data/processed_data/database.csv', sep=';', index=False)

if __name__ == '__main__':
    print("Step 5: Article final... ")

    df = input_csv()

    df_filtered = df.query("summary != ''")

    df_filtered = df_filtered.drop([
        'link',
        # 'redirect',
        'articleBody',
        # 'keywords0',
        # 'keywords1',
        # 'keywords2',
        # 'keywords3',
        # 'keywords4',
        # 'keywords5',
        # 'summaryKeywords1',
        # 'summaryKeywords2',
        # 'summaryKeywords3',
        # 'summaryKeywords4',
    ], axis=1)

    df_filtered = df_filtered.rename(
        columns={
            'published': 'date',
            'redirectLink': 'url',
            'articleImage': 'image',
            'summaryKeywords0': 'totalKeywords',
            'summaryKeywords5': 'topKeywords'
        }
    )

    for _, row in df_filtered.iterrows():
        news_summary = row['summary']
        news_keywords = row['topKeywords']
        new_refs = row['url']
        news_src = row['image']
        news_date = row['date']

    output_csv(df_filtered)


    db_new = df_filtered
    db_old = input_db()

    # 중복 제거하기 전에 'key' 열을 인덱스로 설정
    db_new.set_index('url', inplace=True)
    db_old.set_index('url', inplace=True)

    # 두 데이터프레임 병합
    db = pd.concat([db_new, db_old]).reset_index()

    # 'key' 열을 기준으로 중복 제거
    db.drop_duplicates(subset='url', keep='first', inplace=True)

    output_db(db)

    print("Complete!!!\n")

"""
        new_article = Article(summary = news_summary, keywords=news_keywords, refs = new_refs, url=news_src, date=news_date)

        print(new_article)

        new_article.save()
"""
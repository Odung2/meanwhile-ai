import pandas as pd
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

def input_csv():
    return pd.read_csv('data/raw_data/rss_part5.csv', sep=';', keep_default_na=False)

def output_csv(df):
    df.to_csv('data/processed_data/database.csv', sep=';', index=False)

if __name__ == '__main__':
    print("Step 6: Final... ")

    df = input_csv()

    df_filtered = df.query("summary != ''")

    df_filtered = df_filtered.drop([
        'link',
        'redirect',
        'articleBody',
        'keywords0',
        'keywords1',
        'keywords2',
        'keywords3',
        'keywords4',
        'keywords5',
        'summaryKeywords1',
        'summaryKeywords2',
        'summaryKeywords3',
        'summaryKeywords4',
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

        new_article = Article(summary = news_summary, keywords=news_keywords, refs = new_refs, url=news_src, date=news_date)

        print(new_article)

        new_article.save()

    output_csv(df_filtered)

    print("Complete!!!\n")
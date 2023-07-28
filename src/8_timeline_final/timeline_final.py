import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import ast

import sys
from pathlib import Path
articles_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(articles_directory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meanwhile.settings')


import django

import json

django.setup()

from articles.models import ArticleList


from articles.serializer import ArticleListSerializer

target_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(target_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meanwhile.settings")


def input_text1():
    with open('data/processed_data/7_timeline_keyword/timeline_keyword_ko.txt', mode='r', newline='', encoding='utf-8') as file:
        # 파일의 내용을 읽어 변수에 저장
        return file.read().replace('\n', '')

def input_text2():
    with open('data/processed_data/7_timeline_keyword/timeline_keyword_en.txt', mode='r', newline='', encoding='utf-8') as file:
        # 파일의 내용을 읽어 변수에 저장
        return file.read().replace('\n', '')

def input_csv():
    # return pd.read_csv('data/processed_data/5_article_final/rss_part5.csv', sep=';', keep_default_na=False)
    return pd.read_csv('data/processed_data/database.csv', sep=';', keep_default_na=False)

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration, BartTokenizer

#  Load Model and Tokenize
tokenizer_ko = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model_ko = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")

tokenizer_en = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model_en = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize_ko(input_text):
    # Encode Input Text
    # input_text = '국내 전반적인 경기침체로 상가 건물주의 수익도 전국적인 감소세를 보이고 있는 것으로 나타났다. 수익형 부동산 연구개발기업 상가정보연구소는 한국감정원 통계를 분석한 결과 전국 중대형 상가 순영업소득(부동산에서 발생하는 임대수입, 기타수입에서 제반 경비를 공제한 순소득)이 1분기 ㎡당 3만4200원에서 3분기 2만5800원으로 감소했다고 17일 밝혔다. 수도권, 세종시, 지방광역시에서 순영업소득이 가장 많이 감소한 지역은 3분기 1만3100원을 기록한 울산으로, 1분기 1만9100원 대비 31.4% 감소했다. 이어 대구(-27.7%), 서울(-26.9%), 광주(-24.9%), 부산(-23.5%), 세종(-23.4%), 대전(-21%), 경기(-19.2%), 인천(-18.5%) 순으로 감소했다. 지방 도시의 경우도 비슷했다. 경남의 3분기 순영업소득은 1만2800원으로 1분기 1만7400원 대비 26.4% 감소했으며 제주(-25.1%), 경북(-24.1%), 충남(-20.9%), 강원(-20.9%), 전남(-20.1%), 전북(-17%), 충북(-15.3%) 등도 감소세를 보였다. 조현택 상가정보연구소 연구원은 "올해 내수 경기의 침체된 분위기가 유지되며 상가, 오피스 등을 비롯한 수익형 부동산 시장의 분위기도 경직된 모습을 보였고 오피스텔, 지식산업센터 등의 수익형 부동산 공급도 증가해 공실의 위험도 늘었다"며 "실제 올 3분기 전국 중대형 상가 공실률은 11.5%를 기록하며 1분기 11.3% 대비 0.2% 포인트 증가했다"고 말했다. 그는 "최근 소셜커머스(SNS를 통한 전자상거래), 음식 배달 중개 애플리케이션, 중고 물품 거래 애플리케이션 등의 사용 증가로 오프라인 매장에 영향을 미쳤다"며 "향후 지역, 콘텐츠에 따른 상권 양극화 현상은 심화될 것으로 보인다"고 덧붙였다.'
    input_ids = tokenizer_ko.encode(input_text, return_tensors="pt")

    # Generate Summary Text Ids
    summary_text_ids = model_ko.generate(
        input_ids=input_ids,
        bos_token_id=model_ko.config.bos_token_id,
        eos_token_id=model_ko.config.eos_token_id,
        length_penalty=0.1,
        max_length=200,
        min_length=20,
        num_beams=4,
    )

    return tokenizer_ko.decode(summary_text_ids[0], skip_special_tokens=True)

def summarize_en(input_text, max_length=128):
    inputs = tokenizer_en([input_text], max_length=max_length, return_tensors="pt", truncation=True)

    # BART를 사용하여 텍스트 요약을 생성합니다.
    summary_ids = model_en.generate(
        inputs["input_ids"],
        num_beams=4,
        max_length=max_length,
        early_stopping=True
    )
    return tokenizer_en.decode(summary_ids[0], skip_special_tokens=True)

def output_txt(link, jsons):
    with open(link, mode='w', newline='', encoding='utf-8') as file:
        file.write(json.dumps(jsons))

if __name__ == '__main__':
    print("Step 8: Timeline final... ")

    timeline_keyword_ko = input_text1()
    timeline_keyword_en = input_text2()
    df = input_csv()

    df_ko = df[df['language'] == 0].copy()
    df_ko['topKeywords'] = df_ko['topKeywords'].apply(ast.literal_eval)
    df_ko = df_ko[df_ko['totalKeywords'].apply(lambda x: timeline_keyword_ko in x)].reset_index(drop=True)
    
    df_en = df[df['language'] == 1].copy()
    df_en['topKeywords'] = df_en['topKeywords'].apply(ast.literal_eval)
    df_en = df_en[df_en['totalKeywords'].apply(lambda x: timeline_keyword_en in x)].reset_index(drop=True)
    
    group_ko = np.zeros(len(df_ko))
    group_en = np.zeros(len(df_en))

    loop = len(df_ko) * len(df_ko) + len(df_en) * len(df_en)
    with tqdm(total=loop, unit="tasks", bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt} [{elapsed}]") as progress_bar:
        group_ko_size = 0
        for idx1, row1 in df_ko.iterrows():
            if group_ko[idx1] == 0:
                group_ko[idx1] = group_ko_size
                group_ko_size += 1

            for idx2, row2 in df_ko.iterrows():
                if idx1 < idx2:
                    common_keywords = list(set(row1['topKeywords']).intersection(set(row2['topKeywords'])))
                    # common_keywords = [string for string in row1['topKeywords'] in row2['topKeywords']]
                    if timeline_keyword_ko in common_keywords:
                        common_keywords.remove(timeline_keyword_ko)

                    if len(common_keywords) > 0:
                        group_ko[idx2] = group_ko[idx1]
                
                progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.
        
        group_en_size = 0
        for idx1, row1 in df_en.iterrows():
            if group_en[idx1] == 0:
                group_en[idx1] = group_en_size
                group_en_size += 1

            for idx2, row2 in df_en.iterrows():
                if idx1 < idx2:
                    common_keywords = list(set(row1['topKeywords']).intersection(set(row2['topKeywords'])))
                    if timeline_keyword_en in common_keywords:
                        common_keywords.remove(timeline_keyword_en)

                    if len(common_keywords) > 0:
                        group_en[idx2] = group_en[idx1]
                
                progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.
                
    article_groups_ko = [[] for _ in range(group_ko_size)]
    for idx, row in df_ko.iterrows():
        article_groups_ko[int(group_ko[idx])].append(row)

    timeline_ko = []
    for article_group in article_groups_ko:
        news_summary = article_group[0]['summary']
        news_keywords = article_group[0]['topKeywords']
        news_title = [article_group[0]['title']]
        new_refs = [article_group[0]['url']]
        news_src = article_group[0]['image']
        news_date = article_group[0]['date']
        news_lang = 0
        for article in article_group[1:]:
            news_summary += article['summary']
            news_keywords = list(set(news_keywords).intersection(set(article['topKeywords'])))
            news_title.append(article['title'])
            new_refs.append(article['url'])
            if news_src == '':
                news_src = row['image']

        news_summary = summarize_ko(news_summary)

        print(f"{news_summary}\n{news_src}\n{new_refs}\n{news_date}\n{news_keywords}\n{news_lang}\n{news_title}\n\n")

        new_event = ArticleList(summary = news_summary, title = news_title, keywords=news_keywords, refs = new_refs, url=news_src, date=news_date, lang=news_lang)
        timeline_ko.append(new_event)

        # new_article.save()
    
    article_groups_en = [[] for _ in range(group_en_size)]
    for idx, row in df_en.iterrows():
        article_groups_en[int(group_en[idx])].append(row)

    timeline_en = []
    for article_group in article_groups_en:
        news_summary = article_group[0]['summary']
        news_keywords = article_group[0]['topKeywords']
        news_title = [article_group[0]['title']]
        new_refs = [article_group[0]['url']]
        news_src = article_group[0]['image']
        news_date = article_group[0]['date']
        news_lang = 1
        for article in article_group[1:]:
            news_summary += article['summary']
            news_keywords = list(set(news_keywords).intersection(set(article['topKeywords'])))
            news_title.append(article['title'])
            new_refs.append(article['url'])
            if news_src == '':
                news_src = row['image']

        news_summary = summarize_en(news_summary)

        print(f"{news_summary}\n{news_src}\n{new_refs}\n{news_date}\n{news_keywords}\n{news_lang}\n{news_title}\n\n")

        new_event = ArticleList(summary = news_summary, title = news_title, keywords=news_keywords, refs = new_refs, url=news_src, date=news_date, lang=news_lang)
        timeline_en.append(new_event)

    serializer = ArticleListSerializer(timeline_en, many=True)
    timeline_en = serializer.data
    serializer = ArticleListSerializer(timeline_ko, many=True)
    timeline_ko = serializer.data

    output_txt('data/processed_data/8_timeline_final/timeline_ko_final.txt', timeline_ko)
    output_txt('data/processed_data/8_timeline_final/timeline_en_final.txt', timeline_en)

    print("Complete!!!\n")
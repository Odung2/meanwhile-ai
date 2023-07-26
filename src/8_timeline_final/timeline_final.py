import pandas as pd
from tqdm import tqdm
import numpy as np

def input_text():
    with open('data/processed_data/7_timeline_keyword/search.txt', mode='r', newline='', encoding='utf-8') as file:
        # 파일의 내용을 읽어 변수에 저장
        return file.read()

def input_csv():
    # return pd.read_csv('data/processed_data/5_article_final/rss_part5.csv', sep=';', keep_default_na=False)
    return pd.read_csv('data/processed_data/database.csv', sep=';', keep_default_na=False)

def output_txt(timeline_ko, timeline_en):
    with open('data/processed_data/8_timeline_final/timeline_final.txt', mode='r', newline='', encoding='utf-8') as file:
        print("timeline_ko")
        for event in timeline_ko:
            print(event)
        print("\n")

        print("timeline_en")
        for event in timeline_en:
            print(event)
        print("\n")

if __name__ == '__main__':
    print("Step 6: Make Timeline... ")

    search = input_text()
    df = input_csv()

    df_ko = df[df['language'] == 0].reset_index(drop=True)
    df_en = df[df['language'] == 1].reset_index(drop=True)

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
                    if search in common_keywords:
                        common_keywords.remove(search)

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
                    if search in common_keywords:
                        common_keywords.remove(search)

                    if len(common_keywords) > 0:
                        
                        group_en[idx2] = group_en[idx1]
                
                progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.
                
    timeline_ko = [[] for _ in range(group_ko_size)]
    for idx, row in df_ko.iterrows():
        timeline_ko[int(group_ko[idx])].append(row)
    
    timeline_en = [[] for _ in range(group_en_size)]
    for idx, row in df_en.iterrows():
        timeline_en[int(group_en[idx])].append(row)

    output_txt(timeline_ko, timeline_en)

    print("Complete!!!\n")
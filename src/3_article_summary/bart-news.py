import pandas as pd

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration, BartTokenizer

def input_csv():
    return pd.read_csv('data/processed_data/2_article_crawler/rss_part2.csv', sep=';', keep_default_na=False)

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

# Decoding Text
# print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
"""
with open('data/processed_data/summary.txt', mode='w', newline='', encoding='utf-8') as file:
    file.write(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
"""

from googletrans import Translator

translator = Translator()

def output_csv(df):
    df.to_csv('data/processed_data/3_article_summary/rss_part3.csv', sep=';', index=False)

from tqdm import tqdm

if __name__ == '__main__':
    print("Step 3: Extract summary from article body... ")

    df = input_csv()

    summary = []
    
    with tqdm(total=len(df), unit="tasks", bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt} [{elapsed}]") as progress_bar:
        for idx, row in df.iterrows():
            doc = row['articleBody']

            if doc != '':
                try:
                    if row['language'] == 0:
                        summary.append(summarize_ko(doc))
                    else:
                        summary.append(summarize_en(doc))
                        # summary.append(translator.translate(summarize_en(doc), src='en', dest='ko').text)
                except Exception:
                    summary.append(None)
            else:
                summary.append(None)

            progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.
    
    df['summary'] = summary
    
    df = df.dropna(subset=["summary"])

    output_csv(df)

    print("Complete!!!\n")
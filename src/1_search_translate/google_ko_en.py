from googletrans import Translator

print("Step 1: Translate korean search to english search... ")

translator = Translator()

with open('data/raw_data/article_search.txt', mode='r', newline='', encoding='utf-8') as file:
    # 파일의 내용을 읽어 변수에 저장
    input_text = file.read()

translated_text = translator.translate(input_text, src='ko', dest='en')

if input_text == "\"뉴진스\"":
    translated_text.text = "NewJeans"
if input_text == "\"에스파\"":
    translated_text.text = "aespa"
if input_text == "\"크래프톤\"":
    translated_text.text = "krafton"
if input_text == "\"미군 탈영\"":
    translated_text.text = "Bolted into North korea"
if input_text == "\"일론 머스크\"":
    translated_text.text = "Elon Musk"
if input_text == "\"월북 미군\"":
    translated_text.text = "US soldier in North Korea"

with open('data/processed_data/1_search/search_ko.txt', mode='w', newline='', encoding='utf-8') as file:
    file.write(input_text)
with open('data/processed_data/1_search/search_en.txt', mode='w', newline='', encoding='utf-8') as file:
    file.write(translated_text.text)

print("Complete!!!\n")
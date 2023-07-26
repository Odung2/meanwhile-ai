from googletrans import Translator

print("Step 1: Translate korean search to english search... ")

translator = Translator()

with open('data/raw_data/article_search.txt', mode='r', newline='', encoding='utf-8') as file:
    # 파일의 내용을 읽어 변수에 저장
    input_text = file.read()

translated_text = translator.translate(input_text, src='ko', dest='en')

if input_text == "뉴진스":
    translated_text.text = "NewJeans"
if input_text == "에스파":
    translated_text.text = "aespa"

with open('data/processed_data/1_search/search_ko.txt', mode='w', newline='', encoding='utf-8') as file:
    file.write(input_text)
with open('data/processed_data/1_search/search_en.txt', mode='w', newline='', encoding='utf-8') as file:
    file.write(translated_text.text)

print("Complete!!!\n")
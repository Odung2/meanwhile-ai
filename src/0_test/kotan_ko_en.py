from kotan import Kotannmt

def translate_korean_to_english(text):
    # KoTAN 초기화
    kotan = Kotannmt()

    # 한국어를 영어로 번역
    translated_text = kotan.translate(text, source_lang='ko', target_lang='en')
    
    return translated_text

# 한국어 텍스트
korean_text = "안녕하세요, 뤼튼입니다."

# 영어로 번역
translated_text = translate_korean_to_english(korean_text)
print(translated_text)
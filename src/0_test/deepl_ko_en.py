import requests

DEEPL_API_KEY = "여기에 API 키를 입력하세요"

def translate_text(text, target_language):
    url = f"https://api-deepl.com/v2/translate"
    
    payload = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_language
    }
    
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        return translated_text
    else:
        return f"Error {response.status_code}: {response.text}"

input_text = "이 글을 영어로 번역해주세요."
target_language = "EN"

translated_text = translate_text(input_text, target_language)
print(translated_text)
from googletrans import Translator

translator = Translator()
input_text = "이 글을 영어로 번역해주세요."

translated_text = translator.translate(input_text, src='ko', dest='en')
print(translated_text.text)
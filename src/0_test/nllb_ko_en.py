from transformers import NLLBForConditionalGeneration, NLLBTokenizer

model_name = "facebook/nllb-200-3.3B"
tokenizer = NLLBTokenizer.from_pretrained(
    model_name, src_lang="ko", tgt_lang="en"
)
model = NLLBForConditionalGeneration.from_pretrained(model_name)

input_text = "이 글을 영어로 번역해주세요."
inputs = tokenizer(
    input_text, padding=True, truncation=True, max_length=128, return_tensors="pt"
)

generated_tokens = model.generate(**inputs)
translated_text = tokenizer.batch_decode(
    generated_tokens, skip_special_tokens=True
)[0]

print(translated_text)
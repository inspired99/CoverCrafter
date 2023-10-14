from transformers import T5ForConditionalGeneration, T5Tokenizer
from tqdm import tqdm


class ClickBaitGenerator:
    def __init__(self, model_name='UrukHan/t5-russian-summarization', length=30, temperature=0.9):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.length = length
        self.temperature = temperature

    def inference(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        summary = self.model.generate(input_ids,
                                      max_length=self.length,
                                      num_return_sequences=1,
                                      temperature=self.temperature,
                                      )
        return self.tokenizer.decode(summary[0], skip_special_tokens=True)

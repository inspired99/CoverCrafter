from transformers import FSMTForConditionalGeneration, FSMTTokenizer
import torch


class TranslatorModel:
    """
    Class for translation prompts from Russian to English
    """

    def __init__(self):
        self.model_path = "facebook/wmt19-ru-en"
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = FSMTTokenizer.from_pretrained(self.model_path)
        self.model = FSMTForConditionalGeneration.from_pretrained(self.model_path)

    def translate(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded

import pymorphy2
import string


class TokenClassification:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def inference(self, text):
        tmp = set()
        tokens = text.translate(str.maketrans('', '', string.punctuation)).split()
        for token in tokens:
            if is_english(token) and not token.isnumeric():
                tmp.add(token)  # english word
            if self.morph.parse(token)[0].tag.POS != 'NOUN':
                continue
            parsed_word = self.morph.parse(token)[0]
            nominative_word = parsed_word.inflect({'nomn'})
            try:
                tmp.add(nominative_word.word)
            except AttributeError:
                pass
        return list(tmp)


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

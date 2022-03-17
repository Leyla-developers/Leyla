from google.translator import GoogleTranslator


class Translator:

    async def translate(self, text, to_lang, from_lang):
        google = GoogleTranslator()

        return await google.translate(text, to_lang, from_lang)

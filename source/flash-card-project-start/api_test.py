from dotenv import load_dotenv
import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def translate_en(word):
    load_dotenv()
    apikey = os.getenv("apikey")
    url = os.getenv("url")

    authenticator = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )

    language_translator.set_service_url(url)

    translation = language_translator.translate(
        text=word,
        model_id='en-es').get_result()
    translation = translation["translations"][0]["translation"]
    print(translation)
    return translation

def translate_es(word):
    load_dotenv()
    apikey = os.getenv("apikey")
    url = os.getenv("url")

    authenticator = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )

    language_translator.set_service_url(url)

    translation = language_translator.translate(
        text=word,
        model_id='es-en').get_result()
    translation = translation["translations"][0]["translation"]

    return translation

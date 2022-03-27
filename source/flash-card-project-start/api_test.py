from dotenv import load_dotenv
import os
import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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
    text='Do you know the milk man?',
    model_id='en-es').get_result()

print(json.dumps(translation, indent=2, ensure_ascii=False))
import requests
import json
from config import settings


def ocr_space_file(image_file, overlay=False, language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': settings.OCR_API_KEY,
               'language': language,
               'filetype': image_file.content_type.split("/")[1]
               }
    try:
        r = requests.post('https://api.ocr.space/parse/image', proxies=settings.PROXIES,
                          files={'file': image_file.file},
                          data=payload,
                          )
        r.raise_for_status()
        decoded_text = json.loads(r.content.decode())
        if decoded_text["IsErroredOnProcessing"]:
            return str(decoded_text["ErrorMessage"])
        # print(type(decoded_text["ParsedResults"][0]["ParsedText"]))
        return decoded_text["ParsedResults"][0]["ParsedText"]

    except requests.exceptions.RequestException as e:
        raise Exception("OCR API Error") from e


def ocr_space_url(url, overlay=False, language='eng'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': settings.OCR_API_KEY,
               'language': language,
               }
    try:
        r = requests.post('https://api.ocr.space/parse/image',
                          proxies=settings.PROXIES,
                          data=payload,
                          )
        r.raise_for_status()
        decoded_text = json.loads(r.content.decode())
        if decoded_text["IsErroredOnProcessing"]:
            return str(decoded_text["ErrorMessage"])
        return decoded_text["ParsedResults"][0]["ParsedText"]

    except requests.exceptions.RequestException as e:
        raise Exception("OCR API Error") from e


# test_file = ocr_space_file(
#     filename='./test.jpeg', language='eng')
# test_url = ocr_space_url(url='https://imgpile.com/images/9rxB2j.jpg')

# print(test_file)
# print(test_url)

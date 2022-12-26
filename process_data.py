import pandas as pd
import os

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]
if __name__=='__main__':

    df = pd.read_csv('gresunstudio.csv')
    caption = list(df['caption'])
    caption_hashtags = list(df['caption_hashtags'])

    # api key credential.json
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/paul-emile/Documents/PythonProject/insta_profile_scrap/credential.json'
    cap_translated_list = []
    cap_has_translated_list = []
    key_words = ['jewelry',r' ring','necklace',r' ear','coat','jacket','vest',r' event','prize','fragrance','outfits','cardigan',r' top',r' bag ','skirt','long-sleeved','shorts','dress','v-neck','suit','pants','trouser','overalls','sweater','shirt','bracelet','camisole']
    key_words_list = []
    for cap,cap_h in zip(caption,caption_hashtags):
        sub_key_words = []
        cap_h = cap_h.replace('\'',' ').replace('[',' ').replace(']',' ')
        cap = cap.replace('#',' ')
        cap_translated_list.append(translate_text('en',cap))
        cap_has_translated_list.append(translate_text('en',cap_h))
        for k in key_words:
            if k in cap_translated_list[-1].lower() or k in cap_has_translated_list[-1].lower():
                sub_key_words.append(k)
        key_words_list.append(sub_key_words)

    df['caption_en'] = cap_translated_list
    df['caption_hashtags_en'] = cap_has_translated_list
    df['key_words'] = key_words_list
    df.to_csv('gresunstudio_translated.csv',index=False)

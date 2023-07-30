# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib.parse
import xml.etree.ElementTree as ET
import gzip
import time


def clean_stop_words(keywords):
    output = []
    #можно задавать любые стоп слова, чтобы перед записью в файл чистился список
    stopwords = ["украина", "алматы", "схема", "вязание", "киев", "мск", "спб", "олх", "olx", "фото", "руками",
                 "новосибирске","вязаная","майнкрафт", "иркутск", "минск","улан", "чем", "скин","название","букв","мир",
                 "отзывы", "самара", "спицами", "распродажа", "оптом", "крючком","москв", "купил","украине","шафа",
                 "вк","спортмастер","2017","2018","2019","пром","prom","сетка","кому","идут", "с чем","носить","это","как","кто"]

    for word in keywords:
        if word not in stopwords:
            output.append(word)

    for stopword in stopwords:
        for words in output:
            if stopword in words:
                output.remove(words)
    
    return output


if __name__ == '__main__':
    domen = 'http://suggestqueries.google.com/complete/search?'
    params = '&output=toolbar&gl=ua&hl=ru&'
    result_file = 'suggest.csv'
    file_key_parsing = 'keysforparsing.txt'

    with open(file_key_parsing, 'r+', encoding='utf-8') as f:
        keywords = [line.strip() for line in f]

    for key in keywords:
        google_url = domen + params + urllib.parse.urlencode({'q': key})
        print(google_url)
        time.sleep(1.5)  # пауза между запросами

        print("подождал секунду после запроса '" + str(key) + "'")
        var_url = urlopen(google_url)
        url_code_check = var_url.getcode()
        #print(url_code_check)
        if url_code_check == 200:
            # Можно убрать, но для универсальности проверяем не зазипован ли ответ
            if var_url.info().get('Content-Encoding') == 'gzip':
                page_data = gzip.decompress(var_url.read())
            elif var_url.info().get('Content-Encoding') == 'deflate':
                    page_data = var_url.read()
            elif var_url.info().get('Content-Encoding'):
                print('Encoding type unknown')
            else:
                page_data = var_url.read()
            xml_doc = ET.fromstring(page_data.decode('cp1251'))

            list_suggestion = []
            for item in xml_doc.findall('CompleteSuggestion/suggestion'):
                list_suggestion.append(item.attrib['data'])

            final_keywords = clean_stop_words(list_suggestion)

            with open(result_file, 'a', newline='', encoding='utf-8') as csv_file:
                csv_file.write('\n'.join(final_keywords))
                csv_file.write('\n') 
        elif url_code_check == 404:
            print("Код ответа: 404")
        elif url_code_check == 400:
            print("Код ответа: 400")
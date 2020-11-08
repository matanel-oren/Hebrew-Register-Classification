import os
import re
from tqdm import tqdm
import requests
from time import sleep
from bs4 import BeautifulSoup


BASE_RAW_DIR = '../data/raw'
BASE_READY_DIR = '../data/ready'


class FileType:
    WHATSAPP = 1
    BEN_YEHUDA = 2
    WIKIPEDIA = 3
    THINKS = 4


# length of a sentence condition
length_cond = lambda sent: len(sent.strip().split(' ')) > 3


# pre-compiled regexes
NON_ALPHANUMERIC_PUNCTS = re.compile('[^.,;:/\\\()\'"!?\s\w0-9א-ת]')
NON_HEBREW_LINES = re.compile('((^|\n*)[^\nא-ת]*?\n)')
BLANK_LINES = re.compile('\n[\s]*\n')
MULTIPLE_SEP = re.compile('\s+')
HEB_NIKUD = re.compile('[\u0590-\u05c9]')
BETWEEN_PARENTHESIS = re.compile('[(][^)]*?[)]')
SENTENCE_REGEX = re.compile('[^.?!\u2026]+[.?!\u2026]+')
ENDLESS_SENT_REGEX = re.compile('[^.!?]+?$')

WHATSAPP_SPECIAL_MESSAGES = re.compile('((<.*?>)|(הודעה זו נמחקה)|([0-9]{1,2}[.][0-9]{1,2}[.][0-9]{4}[,] [0-9]{1,2}:[0-9]{2} -[^:]*?\n)|(http.*?\n))', flags=re.DOTALL)
ANOTHER_WHATSAPP_MESSAGES = re.compile("[0-9]{1,2}[.][0-9]{1,2}[.][0-9]{4}[,] [0-9]{1,2}:[0-9]{2} - .+?: ")
WHATSAPP_CONTACT = re.compile('(^|\n)[^\n]*?[.]vcf.*?(\n|$)')

BEN_YEHUDA_SITE_SIGN = re.compile('(את הטקסט.*)')


def download_thinks():
    list_page_url = 'https://thinkil.co.il/texts-sitemap.xml'

    res = requests.get(list_page_url)
    soup = BeautifulSoup(res.text)

    urls = [loc.text for loc in soup.find_all('loc')]
    image_urls = {loc.text for loc in soup.find_all('image:loc')}
    urls = [url for url in urls if url not in image_urls]

    thinks_dir = os.path.join(BASE_RAW_DIR, 'thinks')
    if not os.path.isdir(thinks_dir):
        os.mkdir(thinks_dir)

    for i in range(1, len(urls)):
        sleep(1)
        res = requests.get(urls[i])
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.hgroup.find('h1', "page-title").text.strip()
        text = soup.article.text

        with open(os.path.join(thinks_dir, re.sub(r'/', '.', title) + '.txt'), 'w') as out_file:
            out_file.write(text)


def preprocess_whatsapp_file(file_content):
    chat = file_content
    chat = re.sub(WHATSAPP_SPECIAL_MESSAGES, '', chat)
    chat = re.sub(ANOTHER_WHATSAPP_MESSAGES, '', chat)
    chat = re.sub(NON_ALPHANUMERIC_PUNCTS, '', chat)
    chat = re.sub(WHATSAPP_CONTACT, '\n', chat)
    chat = re.sub(NON_HEBREW_LINES, '\n', chat)
    chat = re.sub(BLANK_LINES, '\n', chat)

    messages = chat.split('\n')

    splited_messages = []
    for m in messages:
        sents_list = re.findall(SENTENCE_REGEX, m) + re.findall(ENDLESS_SENT_REGEX, m)
        if len(sents_list) > 1:
            splited_messages = splited_messages + sents_list
        else:
            splited_messages.append(m)

    return [m.strip() for m in splited_messages if length_cond(m)]


def preprocess_ben_yehuda_file(file_content):
    text = re.sub(BEN_YEHUDA_SITE_SIGN, '', file_content)
    text = re.sub(MULTIPLE_SEP, ' ', text)
    text = re.sub(HEB_NIKUD, '', text)

    sents = re.findall(SENTENCE_REGEX, text)
    return [s.strip() for s in sents[1:] if length_cond(s)]


def preprocess_wikipedia_file(file_content):
    text = re.sub(BETWEEN_PARENTHESIS, '', file_content)
    text = re.sub(HEB_NIKUD, '', text)
    text = re.sub(MULTIPLE_SEP, ' ', text)

    sents = re.findall(SENTENCE_REGEX, text)
    return [s.strip() for s in sents[1:] if length_cond(s)]


def preprocess_thinks_file(file_content):
    sents = []
    lines = file_content.split('\n')
    for line in lines:
        sents += [sent.strip() for sent in re.findall(SENTENCE_REGEX, line)
                  if length_cond(sent)]

    return sents


def preprocess_dir(dirname, file_type):
    if file_type == FileType.WHATSAPP:
        preprocess_func = preprocess_whatsapp_file
    elif file_type == FileType.BEN_YEHUDA:
        preprocess_func = preprocess_ben_yehuda_file
    elif file_type == FileType.WIKIPEDIA:
        preprocess_func = preprocess_wikipedia_file
    elif file_type == FileType.THINKS:
        preprocess_func = preprocess_thinks_file
    else:
        raise ValueError('This file type is not supported.')

    indir = os.path.join(BASE_RAW_DIR, dirname)
    outdir = os.path.join(BASE_READY_DIR, dirname)

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    for filename in tqdm(os.listdir(indir)):
        with open(os.path.join(indir, filename), encoding='utf8') as raw_file:
            sents = preprocess_func(raw_file.read())
            if sents:
                with open(os.path.join(outdir, filename), 'w', encoding='utf8') as ready_file:
                    ready_file.write('\n'.join(sents))


if __name__ == '__main__':
    # whatsapp
    preprocess_dir('whatsapp', FileType.WHATSAPP)
    # wikipedia
    preprocess_dir('NITE_Wiki_2013', FileType.WIKIPEDIA)
    # ben yehuda project
    preprocess_dir('ben_yehuda_project', FileType.BEN_YEHUDA)
    # thinks
    # download_thinks()
    preprocess_dir('thinks', FileType.THINKS)

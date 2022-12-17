# noinspection SpellCheckingInspection
from urllib import request as urlrequest
import urllib as urllib
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
from urllib import request
import string
import os.path
import json
import sys
from cleaning_functions import find_title, find_author, clean_end_of_text, clean_start_of_text
# api-endpoint
URL = "https://gutendex.com/books/"
# defining a params dict for the parameters to be sent to the API
PARAMS = {}
#count of texts we are analyzing
max_count = 69430
count = 10
ua = UserAgent() # From here we generate a random user agent
proxies = []
current_proxy = ""
def generate_proxies():
    proxies_req = urlrequest.Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlrequest.urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find("tbody")
    # Save proxies in the array
    for row in proxies_table.find_all('tr'):
        proxies.append(
            row.find_all('td')[0].string + ":" +
            row.find_all('td')[1].string
        )
    return proxies[random_proxy(proxies)]

def random_proxy(proxies1):
    return random.randint(0, len(proxies1) - 1)

def check_proxy(i, current_proxy1):
    if i % 13 == 0:
        return proxies[random_proxy(proxies)]
    return current_proxy1

def handle_single_author(author):
    if ',' in author['name']:
        f = data['authors'][0]['name'].split(',')
        if len(f) == 2:
            last, first = f[0], f[1]
        else:
            first = f[0]
            last = f[1:]
    else:
        QUERY = ""
        output = ""
        output.write(f"Query: {QUERY} \n")
        f = data['authors'][0]['name'].split(' ')
        if len(f) == 1:
            first = str(f[0]).lower()
            last = " "
        elif len(f) == 2:
            first, last = f[0], f[1]
        else:
            first = f[0] + f[1]
            last = ''.join(f[2:])
    return str(first), str(last)

def append_to_file(name, author_title):
    with open(name, "a", newline="") as outfile:
        outfile.write(author_title)
        outfile.write('\n')
        outfile.close()

def make_request_using_proxy_to_gutendex(book_id):
    request_url = URL + str(book_id)
    # r = reqs2.get(url=request_url, params=PARAMS, proxies={'http': current_proxy})
    # return r.json()
    print(request_url)
    proxy_handler = request.ProxyHandler({'http': current_proxy})
    opener = request.build_opener(proxy_handler)
    try:
        opens = opener.open(request_url)
        if opens == '{"detail":"Not found."}':
            print(opens)
        text = json.loads(opens.read().decode('utf8'))
        return text
    except urllib.error.HTTPError:
        return {'detail': 'Not found.'}


def handle_gutendex_response(data1):
    if data1 == {'detail': 'Not found.'}:  # if book no longer available but still assigned ID
        return ' ', ' '
    title = str(data1['title'])
    name = ""
    if not data1['authors']:
        last = ""
        first = "none"
    elif len(data1['authors']) == 1:
        first, last = handle_single_author(data1['authors'][0])
    elif len(data1['authors']) > 1:      # multiple authors
        for author in range(0, len(data1['authors'])):
            print(data1['authors'][author])
            print("Author number: ", author)
            first, last = handle_single_author(data1['authors'][author])
            name = name + str(first + "_" + last)
        name += "-"
    if not name and first and last:
        name = first + "_" + last + "-"
    author_title = name + title
    translation = list(string.punctuation)
    translation.remove('_')
    translation.remove('-')
    translation = ''.join(str(trans) for trans in translation)
    author_title = author_title.translate(str.maketrans("", "", translation))
    if author_title[0] == " ":
        author_title = author_title[1:]
    author_title = author_title.replace(" ", "_")
    author_title = author_title + ".txt"
    author_title = author_title.lower()
    append_to_file("author_books.txt", author_title)
    return author_title, title

def build_url(url):
    if "text/plain" not in url.keys() and "text/plain; charset=utf-8" not in url.keys():
        return ""
    if "text/plain" in url.keys():
        return url["text/plain"]
    elif "text/plain; charset=utf-8" in url.keys():
        return url["text/plain; charset=utf-8"]

def write_raw_text_to_file(dirname, author_title):
    print("Writing ", author_title, " now ")
    if len(author_title) > 200:
        author, title = author_title.split('-')
        title = title[0: 200]
        author_title = author + title
    with open(dirname + "/" + author_title, "w") as outfile:
        outfile.write(text)
        outfile.close()


def build_request(current_proxy1, url):
    current_proxy1 = check_proxy(book_id, current_proxy1)
    proxy_handler = request.ProxyHandler({'http': current_proxy1})
    opener = request.build_opener(proxy_handler)
    return opener.open(url)


def update_proxy(proxies1, current_proxy1):
    proxies1.remove(current_proxy1)
    current_proxy1 = proxies1[random_proxy(proxies1)]
    if len(proxies1) == 0:
        proxies1 = generate_proxies()
    return proxies1, current_proxy1

if __name__ == '__main__':

    current_proxy = generate_proxies()    # Choose a random proxy
    for book_id in range(500, 1000):
        data = make_request_using_proxy_to_gutendex(book_id)
        author_title, title = handle_gutendex_response(data)
        if author_title == ' ':
            continue
        try:
            url = build_url(data["formats"])
            if url == "": # if there is an author text name here we should probably delete it
                continue
            req = build_request(current_proxy, url)
            text = req.read().decode('utf8')
        except ConnectionError:
            #if our connection is reset, remove the proxy and try again
            proxies, current_proxy = update_proxy(proxies, current_proxy)
            try:
                url = build_url(data["formats"])
                req = build_request(current_proxy, url)
                text = req.read().decode('utf8')
            except ConnectionError:
                proxies, current_proxy = update_proxy( proxies, current_proxy)
                continue
        except UnicodeDecodeError:
            text = req.read().decode("ISO-8859-1")


        #here is where kafka would send a message that it's done and it's also where we should write raw text to file


        #okay if I understand this framework correctly I think I should write my raw text here in an hdfs format and then call
        #another job to do the next section of the program

        #need to tokenize the text here and do some basic processing
        #honestly it's a good spot to write some big files to and transfer to another job if I understand correctly

        #use nltk tokenizer here
        text = text.lower()  # lowercase all text from here on
        title = title.lower()
        author_title = author_title.lower()
        text = clean_end_of_text(text)
        text = clean_start_of_text(text, title, author_title.split('-')[0])
        #text = text.translate(str.maketrans("", "", string.punctuation))
        write_raw_text_to_file("books", author_title)
        DIR = 'books'
        print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
from readability    import Readability
import requests
import chardet

from newspaper import Article

def main():
    url = "http://china.ynet.com/3.1/1610/07/11819034.html"

    print("++++++++++++++++++ Readability ++++++++++++++++++")
    extract_by_readability(url)
    print("++++++++++++++++++ Newspaper ++++++++++++++++++")
    extract_by_newspaper(url)

def extract_by_readability(url):
    r = requests.get(url)
    r.close()

    print("Encode: " + r.encoding)
    print("Apparent Encode" + r.apparent_encoding)
    if r.encoding != r.apparent_encoding:
        r.encoding = r.apparent_encoding

    result = Readability(r.text, url)
    print("------------- TITLE --------------")
    print(result.title)
    print("------------- CONTENT --------------")
    print(result.content)
    print("-------------- IMAGE ---------------")
    print(result.top_image)

def extract_by_newspaper(url):
    article = Article(url, language='zh')
    article.download()
    article.parse()

    print("------------- TITLE --------------")
    print(article.title)
    print("------------- CONTENT --------------")
    print(article.text)
    print("-------------- IMAGE ---------------")
    print(article.top_image)

if __name__ == "__main__":
    main()

from readability    import Readability
import requests
import chardet
import re

from newspaper import Article

def main():
    url = "http://mp.weixin.qq.com/s?src=3&timestamp=1476173520&ver=1&signature=8ymboW2EShgCmFhOPbhjW8OKf81t*bz70D3tWEkhXo2voIiZ1tpA99AicD6nDbE8VJrEimQHBilRmqRGzLz02krW-Bpgbsg3uKT*D2dgB3JFxu8koCdQmo5Zy1MVxJZLeRwJD4GLn3RE2JKOHrVWey9OY9EQf8LLROi7TLczm7E="

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

def fetch_weixin_top_image(article):
    img_kwargs = {'tag': 'img', 'attr': 'data-src'}
    img_tags = article.extractor.parser.getElementsByTag(article.clean_doc, **img_kwargs)
    img_urls = []

    if img_tags:
        img_urls = [img_tag.get('data-src')
            for img_tag in img_tags if img_tag.get('data-src')]

    if img_urls:
        article.set_imgs(set(img_urls))
        article.set_top_img_no_check(img_urls[0])

def extract_by_newspaper(url):
    article = Article(url, language='zh')
    article.download()
    article.parse()

    print("------------- TITLE --------------")
    print(article.title)
    print("------------- CONTENT --------------")
    print(article.text)
    print("-------------- IMAGE ---------------")
    if not article.top_image:
        weixin_reg = re.compile('.*mp.weixin.qq.com.*')
        if weixin_reg.match(article.url):
            fetch_weixin_top_image(article)

    print(article.top_image)

if __name__ == "__main__":
    main()

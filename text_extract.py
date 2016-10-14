# from readability    import Readability
# import requests
# import chardet
import re
from extractor import weixin_extractor
from newspaper import Article

def main():
    url = "http://mp.weixin.qq.com/s?__biz=MjM5MjIxMTc4OA==&mid=2650763642&idx=1&sn=066a574daec5e9a61bfc221ea9edd2df&scene=0#wechat_redirect"

    # print("++++++++++++++++++ Readability ++++++++++++++++++")
    # extract_by_readability(url)
    print("++++++++++++++++++ Newspaper ++++++++++++++++++")
    extract_by_newspaper(url)

# def extract_by_readability(url):
#     r = requests.get(url)
#     r.close()

#     print("Encode: " + r.encoding)
#     print("Apparent Encode" + r.apparent_encoding)
#     if r.encoding != r.apparent_encoding:
#         r.encoding = r.apparent_encoding

#     result = Readability(r.text, url)
#     print("------------- TITLE --------------")
#     print(result.title)
#     print("------------- CONTENT --------------")
#     print(result.content)
#     print("-------------- IMAGE ---------------")
#     print(result.top_image)

def clean_text(text):
    text = re.sub('[ \t]+', '', text)
    text = re.sub(r'([\r\n]+.?)+', r'\r\n', text)
    text = text.strip()
    return text

def extract_by_newspaper(url):
    article = Article(url, language='zh')
    article.download()
    article.parse()

    print("------------- TITLE --------------")
    print(article.title)
    print("------------- CONTENT --------------")
    print(clean_text(article.text))
    print("-------------- IMAGE ---------------")
    if not article.top_image:
        if weixin_extractor.is_weixin(article.url):
            weixin_extractor.fill_top_image(article)

    print(article.top_image)

if __name__ == "__main__":
    main()

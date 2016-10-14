from .weixin_image import WeixinImage
import re

def is_weixin(url):
    weixin_reg = re.compile('.*mp.weixin.qq.com.*')
    return True and weixin_reg.match(url)

def fill_top_image(article):
    img_kwargs = {'tag': 'img', 'attr': 'data-src'}
    img_tags = article.extractor.parser.getElementsByTag(article.clean_doc, **img_kwargs)
    imgs = []

    if img_tags:
        for img_tag in img_tags:
            if not img_tag.get('data-src'): continue
            img = WeixinImage(img_tag)
            imgs.append(img)

    if imgs:
        max_score = 0
        top_img = None

        for img in imgs:
            if img.score > max_score:
                max_score = img.score
                top_img = img

        article.set_top_img_no_check(top_img.url)
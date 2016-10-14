#coding=utf-8

from bs4 import BeautifulSoup
import math

class WeixinImage:
    def __init__(self, img):
        self.img = img
        self.url = img.get('data-src')
        self.width = self.convert_to_integer(img.get('data-w'))
        self.ratio = self.convert_to_float(img.get('data-ratio'))
        self.type = img.get('data-type')

        self.score = self.width_score() + self.ratio_score() + self.type_score()

    def convert_to_integer(self, var):
        num = None
        try:
            num = int(var)
        except Exception:
            num = 0
        return num

    def convert_to_float(self, var):
        num = None
        try:
            num = float(var)
        except Exception:
            num = 0.0
        return num


    def gaussian_func(self, x, u, o):
        return 1/(math.sqrt(2*math.pi)*o)*math.exp(-1*(x-u)**2/(2*o**2))

    def width_score(self):
        return self.gaussian_func(self.width, 600, 1) * 100

    def ratio_score(self):
        return self.gaussian_func(self.ratio, 16/9, 1) * 100

    def type_score(self):
        ts = {
            'jpeg': 100,
            'png': 80,
            'bmp': 50,
            'gif': 20
        }
        return ts.get(self.type) or 0


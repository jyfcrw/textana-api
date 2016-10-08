from readability    import Readability
from urllib.request import urlopen

def main():
    url = "http://mp.weixin.qq.com/s?__biz=MzI4NDE5OTYwMQ==&mid=2247483956&idx=1&sn=aedb65caffb5d8895115a69d95659e37&chksm=ebfe5deadc89d4fc613a5331ba3be829fe1c7a0a5f778755f0c5de1fbef9653f97350956c8a1&scene=1&srcid=0918yQ30NM5pyonyPzZJrEZi&from=singlemessage&isappinstalled=0#wechat_redirect"
    htmlcode = urlopen(url).read().decode('utf-8')
    result = Readability(htmlcode, url)
    print("------------- TITLE --------------")
    print(result.title)
    print("------------- CONTENT --------------")
    print(result.content)

if __name__ == "__main__":
    main()

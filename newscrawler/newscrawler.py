from tqdm import tqdm
import requests

import newspaper
# 词频统计库
import collections  
# numpy 库
import numpy as np  
# 结巴分词
import jieba
import jieba.posseg as pseg
# 词云展示库
import wordcloud 
from PIL import Image


# stop_words = open('baidu_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('cn_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('hit_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('scu_stopwords.txt', 'r', encoding='utf-8').read().split('\n')

stop_words = []

url = 'https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=106,118,108&page=%s'

links = []

for page in range(50):
    response = requests.get(url % page)
    links += [data['vurl'] for data in response.json()['data']]

words = []


for link in links:
    # 获取文章
    paper = newspaper.Article(link, language='zh', 
        memoize_articles=False, fetch_images=False)
    try:
        paper.download()
        paper.parse()
    except Exception:
        continue
    else:
        content = paper.title + paper.text
        if not content:
            continue

        print(paper.title)

        for word in pseg.cut(paper.text):
            if 'nr' == word.flag:
            # if 'n' in word.flag and word.word not in stop_words:
                words.append(word.word)

# links = [
#     'https://www.qq.com/',
#     # 'https://new.qq.com/ch/ent/',
#     # 'https://sina.com.cn/',
#     # 'https://ent.163.com/',
#     # 'https://tuijian.hao123.com/ent',
#     # 'http://news.yule.com.cn/',
#     # 'http://toutiao.sogou.com/yule.html',
#     # 'http://www.dzyule.com/'
# ]


# words = []

# for link in links:
#     # 获取文章
#     paper = newspaper.build(link, language='zh', 
#         memoize_articles=False, fetch_images=False)
#     import ipdb
#     ipdb.set_trace()
#     process = tqdm(paper.articles)

#     for news in process:
#         try:
#             # if not news.url.startswith('http://ent.sina.com.cn/'):
#             # print(news.url)
#             # if not news.url.startswith('https://ent.163.com/'):
#             #     continue
#             news.download()
#             news.parse()
#         except Exception:
#             continue
#         else:
#             if news.title:
#                 process.set_description("Processing %s" % news.title)
#             if not news.text:
#                 continue
#             for word in pseg.cut(news.text):
#                 if 'nr' == word.flag and word.word not in stop_words:
#                     words.append(word.word)
                # if 'n' in word.flag and word.word not in stop_words:
                #     words.append(word.word)

mask = np.array(Image.open('china.jpg'))
wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',
    mask=mask,
    max_words=200,
    mode='RGBA',
    background_color=None,
    max_font_size=120
)

word_counts = collections.Counter(words)

print(word_counts.most_common(100))

wc.generate_from_frequencies(word_counts)

wc.to_file('cloud.png')

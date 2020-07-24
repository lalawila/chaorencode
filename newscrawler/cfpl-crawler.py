from tqdm import tqdm
import requests

import re

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

stop_words = ['明星', '老公', '王']
add_words = [
    '阿朵',
    '郑希怡',
    '宁静',
    '陈松伶',
    '钟丽缇',
    '伊能静',
    '海陆',
    '金晨',
    '蓝盈莹',
    '王丽坤',
    '万茜',
    '张萌',
    '金莎',
    '刘芸',
    '沈梦辰',
    '吴昕',
    '郁可唯',
    '朱婧汐',
    '丁当',
    '黄龄',
    '孟佳',
    '王霏霏',
    '许飞',
    '袁咏琳',
    '张雨绮',
    '黄圣依',
    '张含韵',
    '王智',
    '白冰',
    '李斯丹妮'
]

[jieba.del_word(word) for word in stop_words]
[jieba.add_word(word, tag='nr') for word in add_words]

url = 'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=ent&page=%s'

links = []

for page in range(10):
    print('get page: %s' % page)
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
    
        if '浪姐' not in content and '乘风破浪' not in content:
            continue

        print(paper.title)
        # pattern = re.compile(r'《(*)》', re.I)
        # words += pattern.findall(content)
    
        for word in pseg.cut(content):
            if 'nr' == word.flag:
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
    background_color='#FFF',
    max_font_size=120
)

word_counts = collections.Counter(words)

print(word_counts.most_common(100))

wc.generate_from_frequencies(word_counts)

wc.to_file('cloud.png')

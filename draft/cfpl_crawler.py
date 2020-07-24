import requests

import newspaper
import collections  
import numpy as np
import jieba
import jieba.posseg as pseg
import wordcloud 
from PIL import Image


# stop_words = open('stopwords/baidu_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('stopwords/cn_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('stopwords/hit_stopwords.txt', 'r', encoding='utf-8').read().split('\n')
# stop_words += open('stopwords/scu_stopwords.txt', 'r', encoding='utf-8').read().split('\n')

stop_words = ['明星', '老公', '王', '连']

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

[jieba.add_word(word, tag='nr') for word in add_words]

url = 'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=ent&page=%s'

links = []

for page in range(1):
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
    
        for cuted in pseg.cut(content):
            if 'nr' == cuted.flag and cuted.word not in stop_words:
                words.append(cuted.word)


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

mask = np.array(Image.open('girl.jpg'))
wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',
    mask=mask,
    max_words=100,
    mode='RGBA',
    background_color=None,
    max_font_size=120
)

word_counts = collections.Counter(words)

[print('%s: %s' % (name, count)) for name, count in word_counts.most_common(20)]

wc.generate_from_frequencies(word_counts)

wc.to_file('cloud.png')

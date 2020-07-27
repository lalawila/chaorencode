import requests

import newspaper
import collections  
import numpy as np
import jieba
import jieba.posseg as pseg
import wordcloud 
from PIL import Image

stop_words = ['明星', '老公', '王', '连', '肯德基']

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

for page in range(500):
    print('get page: %s' % page)
    try:
        response = requests.get(url % page)
    except Exception:
        continue
    else:
        links += [data['vurl'] for data in response.json()['data']]

words = []

print('amount of links：%s' %len(links))

count = 0

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

        count += 1
        print('%s：%s' % (count, paper.title))
        for cuted in pseg.cut(content):
            if 'nr' == cuted.flag and cuted.word not in stop_words:
                words.append(cuted.word)

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

wc.to_file('result.png')

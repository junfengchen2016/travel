import sys
import os

import gflags

from chenjunfeng.tools.baidu_aip import wzsb, yyhc

gflags.DEFINE_string('path_image', './travel/yuanmingyuan/image', '')
gflags.DEFINE_string('path_txt', './travel/yuanmingyuan/txt', '')
gflags.DEFINE_string('path_txt2', './travel/yuanmingyuan/txt2', '')
gflags.DEFINE_string('path_mp3', './travel/yuanmingyuan/mp3', '')
gflags.DEFINE_string('pathname_md', './travel/yuanmingyuan/yuanmingyuan.md', '')
gflags.DEFINE_string('md_h1', '圆明园', '')
gflags.DEFINE_string('md_url', 'https://pan.baidu.com/s/11A_rII4K-vr5UbLPjrPaZA', '')
gflags.DEFINE_string('pathname_src', '', '')
gflags.DEFINE_string('pathname_dst', '', '')
FLAGS = gflags.FLAGS

def image2txt(pathname_image, pathname_txt):
    with open(pathname_image, 'rb') as f:
        wzsb_bytes = f.read()
    lines = wzsb(wzsb_bytes)
    with open(pathname_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    pass    

def jpg2txt(pathname_jpg, pathname_txt):
    with open(pathname_jpg, 'rb') as f:
        wzsb_bytes = f.read()
    lines = wzsb(wzsb_bytes)
    with open(pathname_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    pass        

def batch_image2txt(path_image, path_txt):
    if(not os.path.exists(path_image)): os.makedirs(path_txt)
    filenames_image = os.listdir(path_image)
    for i, filename_image in enumerate(filenames_image):
        stem, extension = os.path.splitext(filename_image)
        if (extension.lower() != '.jpg' and extension.lower() != '.png'): continue
        
        pathname_image = '{}/{}'.format(path_image, filename_image)
        pathname_txt = '{}/{}.txt'.format(path_txt, stem)
        if(os.path.exists(pathname_txt)): continue

        image2txt(pathname_image, pathname_txt)

def txt2mp3(pathname_txt, pathname_mp3):
    with open(pathname_txt, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    tex = ''.join(lines)
    yyhc_bytes = yyhc(tex)
    with open(pathname_mp3, 'wb') as f:
        f.write(yyhc_bytes)
    pass    

def batch_txt2mp3(path_txt, path_mp3):
    if(not os.path.exists(path_mp3)): os.makedirs(path_mp3)
    filenames_txt = os.listdir(path_txt)
    for i, filename_txt in enumerate(filenames_txt):
        stem, extension = os.path.splitext(filename_txt)
        if (extension.lower() != '.txt'): continue
        
        pathname_txt = '{}/{}'.format(path_txt, filename_txt)
        pathname_mp3 = '{}/{}.mp3'.format(path_mp3, stem)
        if(os.path.exists(pathname_mp3)): continue

        txt2mp3(pathname_txt, pathname_mp3)  

def batch_txt2md(h1, url, path_txt, pathname_md):
    filenames_txt = os.listdir(path_txt)
    dict1 = {}
    items = []
    for i, filename_txt in enumerate(filenames_txt):
        stem, extension = os.path.splitext(filename_txt)
        if (extension.lower() != '.txt'): continue

        pathname_txt = '{}/{}'.format(path_txt, filename_txt)
        with open(pathname_txt, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            tex = ''.join(lines)
            b = [a.strip() for a in stem.split('-')]
            if(len(b) == 2):
                key = b[0]
                value = dict1.get(key, [])
                value.append({'title': b[1], 'content':tex})
                dict1[key] = value
            else:
                key = b['others']
                value = dict1.get(key, [])
                value.append({'title': stem, 'content':tex})
                dict1[key] = value
            items.append({'title': stem, 'content':tex})

    with open(pathname_md, 'w', encoding='utf-8') as f:
        f.write('# {}\n'.format(h1))
        f.write('[mp3]({})\n'.format(url))
        for key in dict1.keys():
            f.write('## {}\n'.format(key))
            for item in dict1[key]:
        # for item in items:
                f.write('- {}\n'.format(item['title']))
                f.write('```\n{}\n```\n'.format(item['content']))

def main(argv):
    FLAGS(argv)
    path_image = FLAGS.path_image
    path_txt = FLAGS.path_txt
    path_txt2 = FLAGS.path_txt2
    path_mp3 = FLAGS.path_mp3
    pathname_md = FLAGS.pathname_md
    md_h1 = FLAGS.md_h1
    md_url = FLAGS.md_url
    pathname_src = FLAGS.pathname_src
    pathname_dst = FLAGS.pathname_dst

    if(path_image != '' and path_txt != ''):
        batch_image2txt(path_image, path_txt)
    if(path_txt2 != '' and path_mp3 != ''):        
        batch_txt2mp3(path_txt2, path_mp3)
    if(path_txt2 != '' and pathname_md != ''):                
        batch_txt2md(md_h1, md_url, path_txt2, pathname_md)

if __name__ == '__main__':
    sys.exit(int(main(sys.argv) or 0))
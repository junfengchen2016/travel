import sys
import os

import gflags

from chenjunfeng.tools.baidu_aip import wzsb, yyhc

gflags.DEFINE_string('path_png', './travel/png', '')
gflags.DEFINE_string('path_txt', './travel/txt', '')
gflags.DEFINE_string('path_txt2', './travel/txt2', '')
gflags.DEFINE_string('path_mp3', './travel/mp3', '')
gflags.DEFINE_string('pathname_md', './travel/tianjin.md', '')
gflags.DEFINE_string('pathname_src', '', '')
gflags.DEFINE_string('pathname_dst', '', '')
FLAGS = gflags.FLAGS

def png2txt(pathname_png, pathname_txt):
    with open(pathname_png, 'rb') as f:
        wzsb_bytes = f.read()
    lines = wzsb(wzsb_bytes)
    with open(pathname_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    pass    

def batch_png2txt(path_png, path_txt):
    if(not os.path.exists(path_png)): os.makedirs(path_txt)
    filenames_png = os.listdir(path_png)
    for i, filename_png in enumerate(filenames_png):
        stem, extension = os.path.splitext(filename_png)
        if (extension.lower() != '.png'): continue
        
        pathname_png = '{}/{}'.format(path_png, filename_png)
        pathname_txt = '{}/{}.txt'.format(path_txt, stem)
        if(os.path.exists(pathname_txt)): continue

        png2txt(pathname_png, pathname_txt)

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

def batch_txt2md(path_txt, pathname_md):
    filenames_txt = os.listdir(path_txt)
    items = []
    for i, filename_txt in enumerate(filenames_txt):
        stem, extension = os.path.splitext(filename_txt)
        if (extension.lower() != '.txt'): continue

        pathname_txt = '{}/{}'.format(path_txt, filename_txt)
        with open(pathname_txt, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            tex = ''.join(lines)
            items.append({'h2': stem, 'h3':tex})

    with open(pathname_md, 'w', encoding='utf-8') as f:
        for item in items:
            f.write('- {}\n'.format(item['h2']))
            f.write('```\n{}\n```\n'.format(item['h3']))

def main(argv):
    FLAGS(argv)
    path_png = FLAGS.path_png
    path_txt = FLAGS.path_txt
    path_txt2 = FLAGS.path_txt2
    path_mp3 = FLAGS.path_mp3
    pathname_md = FLAGS.pathname_md
    pathname_src = FLAGS.pathname_src
    pathname_dst = FLAGS.pathname_dst

    if(path_png != '' and path_txt != ''):
        batch_png2txt(path_png, path_txt)
    if(path_txt2 != '' and path_mp3 != ''):        
        batch_txt2mp3(path_txt2, path_mp3)
    if(path_txt2 != '' and pathname_md != ''):                
        batch_txt2md(path_txt2, pathname_md)

if __name__ == '__main__':
    sys.exit(int(main(sys.argv) or 0))
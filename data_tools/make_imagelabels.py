#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import random
   
def write_list(path_out, image_list):
    with open(path_out, 'w') as fout:
        n_images = xrange(len(image_list))
        for i in n_images:
#            line = '%d\t' % image_list[i][0]
            line = '%s' % image_list[i][1]
            for j in image_list[i][2:]:
                line += ' %d' % j
#            line += '%s\n' % image_list[i][1]
            
            line += '\n'
            fout.write(line)
            
def list_image(root, recursive, exts):
    image_list = []
    if recursive:
        cat = {}
        for path, subdirs, files in os.walk(root, followlinks=True):
            subdirs.sort()
            print(len(cat), path)
            for fname in files:
                fpath = os.path.join(path, fname)
                suffix = os.path.splitext(fname)[1].lower()
                if os.path.isfile(fpath) and (suffix in exts):
                    if path not in cat:
                        cat[path] = len(cat)
#                    image_list.append((len(image_list), os.path.relpath(fpath, root), cat[path]))
                    image_list.append((len(image_list), os.path.relpath(fpath, root), cat[path]))
        path_out = root
        path_out += 'label.txt'
        
        print cat
        print cat.keys()
#        with open(path_out, 'w') as fout:
            
            
    else:
        for fname in os.listdir(root):
            fpath = os.path.join(root, fname)
            suffix = os.path.splitext(fname)[1].lower()
            if os.path.isfile(fpath) and (suffix in exts):
                image_list.append((len(image_list), os.path.relpath(fpath, root), 0))
    return image_list
    
def make_list(args):
    print args.root
    print args.recursive
    print args.exts
    txt_save_path = args.root + args.prefix
    print txt_save_path
    image_list = list_image(args.root, args.recursive, args.exts)
    if args.shuffle is True:
        random.seed(100)
        random.shuffle(image_list)
    N = len(image_list)
    chunk_size = (N + args.chunks - 1) / args.chunks
    for i in xrange(args.chunks):
        chunk = image_list[i * chunk_size:(i + 1) * chunk_size]
        if args.chunks > 1:
            str_chunk = '_%d' % i
        else:
            str_chunk = ''
        sep = int(chunk_size * args.train_ratio)
        sep_test = int(chunk_size * args.test_ratio)
        write_list(txt_save_path + str_chunk + '_test.txt', chunk[:sep_test])
        write_list(txt_save_path + str_chunk + '_train.txt', chunk[sep_test:sep_test + sep])
        write_list(txt_save_path + str_chunk + '_val.txt', chunk[sep_test + sep:])
        
def main():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Create an image list or \
        make a record database by reading from an image list')
    parser.add_argument('prefix', help='prefix of input/output files.')
    parser.add_argument('root', help='path to folder containing images.')
    cgroup = parser.add_argument_group('Options for creating image lists')
    cgroup.add_argument('--list', type=bool, default=True,
                        help='If this is set im2rec will create image list(s) by traversing root folder\
        and output to <prefix>.lst.\
        Otherwise im2rec will read <prefix>.lst and create a database at <prefix>.rec')
    cgroup.add_argument('--exts', type=list, default=['.jpeg', '.jpg','.png','.bmp'],
                        help='list of acceptable image extensions.')
    cgroup.add_argument('--chunks', type=int, default=1, help='number of chunks.')
    cgroup.add_argument('--train-ratio', type=float, default=1.0,
                        help='Ratio of images to use for training.')
    cgroup.add_argument('--test-ratio', type=float, default=0,
                        help='Ratio of images to use for testing.')
    cgroup.add_argument('--recursive', type=bool, default=True,
                        help='If true recursively walk through subdirs and assign an unique label\
        to images in each folder. Otherwise only include images in the root folder\
        and give them label 0.')
    cgroup.add_argument('--shuffle', default=True, help='If this is set as True, \
        im2rec will randomize the image order in <prefix>.lst')
    args = parser.parse_args()
    if args.list:
        make_list(args)
    
            
if __name__ == "__main__":
    main()

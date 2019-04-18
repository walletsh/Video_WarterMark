# !/usr/bin/ python
# -*- coding:utf-8 -*-
import os
import csv
from builtins import int

#import pymongo
#from pymongo import MongoClient
#client = MongoClient()

#client=MongoClient('127.0.0.1',27017)
#连接mongodb数据库
#client = MongoClient('mongodb://127.0.0.1:27017/')
#创建或选择数据库
#db = client.exvideoDB
#获取非系统的集合
#db.collection_names(include_system_collections=False)
#创建表或获取表（集合名）
#posts = db.videoname

path = '/Users/imwallet/Desktop/video/'

def to_int(filename):
    try:
        int(filename)
        return int(filename)
    except ValueError:
        try:
            float(filename)
            return int(float(filename))
        except ValueError:
            return False


def reset_file_name():
    movie_name = os.listdir(path)
    file_old_names = []
    file_name_nums = []
    value = 100000000
    for name in movie_name:

        (filepath, tempfilename) = os.path.split(name)
        (shotname, extension) = os.path.splitext(tempfilename)
    #     shot_num = to_int(shotname)
    #     print('shot_num %s' % shot_num)
        if extension == '.mp4' or extension == '.MP4':
            new_name = str(value) + '.mp4'
            value += 1
            os.renames(path + name, path + new_name)
    #         if isinstance(shot_num, int):
    #             if shot_num < 100000001:
    #                 file_old_names.append(name)
    #             else:
    #                 file_name_nums.append(shot_num)
    #         else:
    #             file_old_names.append(name)
    #
    # print('file_old_names: {}'.format(file_old_names))
    # print('file_name_nums: {}'.format(file_name_nums))
    #
    # if len(file_name_nums):
    #     value = max(file_name_nums)
    # else:
    #     value = 100000001
    #
    # print('value: %s' % value)
    # for name in file_old_names:
    #     new_name =  str(value) + '.mp4'
    #     value += 1
    #     os.renames(path + name, path + new_name)






if __name__ == '__main__':
    reset_file_name()

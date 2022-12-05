import makesentence as ms
from random import seed
import time

# 装饰器
def cal_time(func):
    def inner(fname):
        start = time.time()
        num = func(fname)
        print("cat的数量为：", num)
        end = time.time()
        print("使用时间为%f秒"%(end - start))
    return inner

# 写文件函数
def write_file(fname, times):
    infile = open(fname, "w")
    seed()
    for i in range(times):
        str = " ".join(ms.sentence()) + "\n"
        infile.write(str)
    infile.close()


# 方法一：磁盘文件检索方式
@cal_time
def count_cat_bydisk(fname):
    cat = 0  # 定义cat数量
    infile = open(fname, encoding="utf_8")  # 打开文件

    for line in infile:  # 文件对象是一个可迭代对象,按行处理
        for word in line.split():  # 逐行统计
            if word == 'cat':
                cat += 1
    infile.close()
    return cat


# 方法二：按行读取文件，一行一行读入内存处理
# 2.1先定义一个逐行读取的函数（使用闭包的方式）
def read_file(fname):
    nlist = []
    infile = open(fname)
    crt = 0

    # 定义局部函数
    def next_word():
        nonlocal nlist, crt
        if crt == len(nlist):  # 一行已经用完
            line = infile.readline()
            if not line:  # line是空串，整个文件已经处理完
                infile.close()
                return None
            nlist = line.split()
            crt = 0
        crt += 1
        return nlist[crt - 1]

    return next_word  # 返回局部定义的函数引用

# 2.2调用逐行读取的函数，计算cat数量
@cal_time
def count_cat_rowbyrow(fname):
    cat = 0
    inner = read_file(fname)
    while True:
        nextword = inner()
        if nextword is not None:
            if nextword == "cat": # 判断是否是cat
                cat += 1
        else:
            break
    return cat


# 方法三：一次性读入内存处理
@cal_time
def count_cat_onetime(fname):
    cat = 0
    infile = open(fname)  # 打开文件的open函数，建立文件对象
    words = list(infile.read().split())  # 文件中是空格隔开的数字，转换为float浮点数
    infile.close()
    for word in words: # 遍历列表，数数量
        if word == "cat":
            cat += 1
    return cat


if __name__ == '__main__':
    fname = 'data/sentence.txt'
    # 写入文件
    write_file(fname, 100000000)

    # 方法一调用
    print("方法一被调用")
    count_cat_bydisk(fname)

    # 方法二调用
    print("方法二被调用")
    count_cat_rowbyrow(fname)

    # 方法三调用
    print("方法三被调用")
    count_cat_onetime(fname)

'''
运行结果如下：
方法一被调用
cat的数量为： 15151243
使用时间为42.793918秒
方法二被调用
cat的数量为： 15151243
使用时间为121.669120秒
方法三被调用
cat的数量为： 15151243
使用时间为80.081127秒
'''
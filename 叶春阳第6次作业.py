import re
from collections import Counter

if __name__ == '__main__':
    infile = open("./data/maillog.txt", encoding="utf_8")  # 打开文件

    pattern = re.compile(r'delivery \d+: [a-z]+: \d+.\d+.\d+.\d+')  # 正则表达式
    sendList = []
    resultList = []

    for line in infile:  # 文件对象是一个可迭代对象,按行处理
        if line.find("starting delivery") != -1:
            words = line.split()
            id = int(words[3][:-1])  # 取出id
            mail = words[-1]  # 取出邮箱
            mailtype = mail.split('@')[1]  # 取出邮箱类型
            sendList.append((id, mail, mailtype))

        result = re.search(pattern, line)
        if result:
            str = result.group().split()
            id2 = int(str[1][:-1])  # 取出id
            status = str[2][:-1]  # 取出状态
            ip = str[3]  # 取出IP地址
            resultList.append((id2, status, ip))
    infile.close()

    totalList = []  # 存储结果
    for item in sendList:  # 遍历列表
        for result in resultList:
            if item[0] == result[0]:  # 判断是否是同一id
                # id，邮箱，邮箱类型，发送状态，IP地址
                totalList.append((item[0], item[1], item[2], result[1], result[2]))

    # 统计结果
    failureList = []
    for item in totalList:
        if item[3] == 'failure':  # 统计失败的记录
            failureList.append(item[2])  # 添加失败的邮箱类型
    count = Counter(failureList)  # 统计每种邮箱的数量
    print("所有失败的邮箱类型及数量为：", count)

    maxCount = 0
    for item in count:
        if count[item] > maxCount:  # 求最大的值
            maxCount = count[item]
    print("失败次数最多的是%d次" % maxCount)
    print("邮箱类型如下：")
    for item in count:
        if count[item] == maxCount:
            print('\t'+item)


"""
运行结果如下：

所有失败的邮箱类型及数量为： Counter({'nau.edu.cn': 2, 'mails.tsinghua.edu.cn': 2, 'cqit.edu.cn': 1, 'ceopen.cn': 1, 
'mail.yf.sh.cn': 1, 'now.net.cn': 1, 'vobile.cn': 1, 'smail.tongji.edu.cn': 1, 'sjtu.edu.cn': 1, 'dl.cn': 1, 
'cad.zju.edu.cn': 1, 'seu.edu.cn': 1, '163.nx.cn': 1, 'mails.gscas.ac.cn': 1, 'dashengwang.cn': 1, 'zzy.cn': 1, 
'baokeelectronic.cn': 1, 'stu.edu.cn': 1, 'chica.cn': 1, 'njit.edu.cn': 1, 'szpst.cn': 1, 'mail.sxptt.zj.cn': 1})
失败次数最多的是2次
邮箱类型如下：
	nau.edu.cn
	mails.tsinghua.edu.cn
"""
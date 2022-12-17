import re
from collections import Counter

if __name__ == '__main__':
    infile = open("./data/maillog.txt", encoding="utf_8")  # 打开文件

    statusPattern = re.compile(r'delivery \d+: [a-z]+:')  # 状态正则表达式
    ipPattern = re.compile(r'\d+\.\d+\.\d+\.\d+')  # ip正则表达式
    sendList = []
    resultList = []

    for line in infile:  # 文件对象是一个可迭代对象,按行处理
        if line.find("starting delivery") != -1:
            words = line.split()
            id = int(words[3][:-1])  # 取出id
            mail = words[-1]  # 取出邮箱
            mailType = mail.split('@')[1]  # 取出邮箱类型
            sendList.append((id, mail, mailType))

        result = re.search(statusPattern, line)
        if result:
            str = result.group().split()
            id2 = int(str[1][:-1])  # 取出id
            status = str[2][:-1]  # 取出状态
            ip = None  # 因为有些日志没有ip，所以这里需要重置
            if re.search(ipPattern, line):  # 取出IP地址
                ip = re.search(ipPattern, line).group()
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
        if item[3] != 'success':  # 统计失败的记录：这里把没有成功的邮箱都定义为失败，即包括failure和deferral
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

所有失败的邮箱类型及数量为： Counter({'online.sh.cn': 6, 'zju.edu.cn': 3, 'nau.edu.cn': 2, 'mails.tsinghua.edu.cn': 2, 
'pzhs.gov.cn': 1, 'cqit.edu.cn': 1, 'ceopen.cn': 1, 'mail.sy.ln.cn': 1, 'flink.net.cn': 1, 'tongji.edu.cn': 1, 
'mail.yf.sh.cn': 1, 'mail.hunu.edu.cn': 1, 'kalsoft.online.sh.cn': 1, 'now.net.cn': 1, 'vobile.cn': 1, 'public.hr.hl.cn': 1, 
'smail.tongji.edu.cn': 1, 'mail.bitsoft.cn': 1, 'sjtu.edu.cn': 1, 'avceit.cn': 1, 'emails.bjpu.edu.cn': 1, 'dl.cn': 1, 
'smail.tongji.ude.cn': 1, 'cad.zju.edu.cn': 1, 'seu.edu.cn': 1, 'public.cs.hn.cn': 1, '163.nx.cn': 1, 'sea.csut.edu.cn': 1, 
'fuce.cn': 1, 'mails.gscas.ac.cn': 1, 'dashengwang.cn': 1, 'zzy.cn': 1, 'cqzkb.edu.cn': 1, 'baokeelectronic.cn': 1, 
'public1.jd.jx.cn': 1, 'stu.edu.cn': 1, 'mail.ustc.edu.cn': 1, 'chica.cn': 1, 'bupt.edu.cn': 1, 'njit.edu.cn': 1, 
'szpst.cn': 1, 'home.swjtu.edu.cn': 1, 'mail.sxptt.zj.cn': 1})
失败次数最多的是6次
邮箱类型如下：
	online.sh.cn
"""
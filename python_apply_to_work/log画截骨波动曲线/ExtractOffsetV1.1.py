import os, csv
import re, math
import numpy as np
import glob
import plotly
from chardet.universaldetector import UniversalDetector
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def detectEncoding(filename):
    bigdata = open(filename,'rb')
    detector = UniversalDetector()
    for line in bigdata.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    bigdata.close()
    return detector.result

def split_list(lst, num_parts):
    length = len(lst)
    part_size = length // num_parts  # 每个部分的大小
    remainder = length % num_parts  # 余数，如果不能整除

    result = []
    start = 0

    for i in range(num_parts):
        if i < remainder:
            end = start + part_size + 1  # 对于有余数的部分，多分配一个元素
        else:
            end = start + part_size

        result.append(lst[start:end])
        start = end

    return result



def avg_dict(mm_split_list):
    section_list = []
    for section in range(len(mm_split_list)):
        section_avg = sum(mm_split_list[section]) / len(mm_split_list[section])
        section_avg_int = round(section_avg,2)
        section_list.append(section_avg_int)
    return section_list


# zxf函数作用：找到 log中的指定数据
# zxf函数实现方法：传入参数 文本，正则表达式 进行匹配
def findmatch(ln, strpat):
    res = []
    matchObj = re.match(strpat, ln)
    if matchObj:
        res = list(matchObj.groups())
    return res


# zxf,转换 匹配
def converMatches(reslist):
    result = []
    if (reslist):
        result.append(reslist[0])
        result.append([float(x) for x in reslist[1:]])
    return result


lns = '2022-09-02 13:52:10.112 [INFO]:4444	[offsetRecorder]:45	LogOffset start offset log of Cut step tibia (2)'


# zxf函数作用： 数据开始行
# zxf函数实现方法：
# zxf函数返回：匹配到的全部元组 例如：['tibia (2)', 'tibia', '2']
def findStartLine(ln):
    strpat = '.+LogOffset start offset log of Cut step ((.+) \((\d)\))'
    return findmatch(ln, strpat)


lne = '2022-09-02 13:52:10.112 [INFO]:4444	[offsetRecorder]:63	LogOffset complete offset log of Cut step tibia (2)'


# zxf函数作用： 数据结束行
# zxf函数实现方法：
def findEndLine(ln):
    strpat = '.+LogOffset complete offset log of Cut step (.+)'
    return findmatch(ln, strpat)


lnd = '2022-09-02 13:52:10.112 [INFO]:4444	[offsetRecorder]:60	LogOffset offset[500-543]  time(ms),offset(mm): (48260, 0.146), (48360, 0.459), (48460, 0.364), (48560, 0.217), (48660, 0.721), (48760, 0.365), (48860, 0.494)'


# zxf函数作用： 数据本身行
# zxf函数实现方法：
def findDataLine(ln):
    strpat = '.+LogOffset offset\[.+\]  time\(ms\),offset\(mm\): (.+)'
    return findmatch(ln, strpat)


# zxf函数作用： 读取log文件
# zxf函数实现方法：
def readLog(fname):
    # loglns = open(fname).readlines()
    # loglns = open(fname, encoding="utf-8").readlines()
    detres = detectEncoding(fname)
    print(detres)

    content = open(fname, 'rb').read()

    # zxf 作用：将字节数据解码为字符串，并将多行字符串分割在一个列表中
    loglns = content.decode(encoding=detres['encoding'], errors='ignore').splitlines()

    bstart = False
    planes = {}
    planekey = ""
    for ln in loglns:
        res = findStartLine(ln)
        if res:
            bstart = True
            print("start", res[0])
            oneplane = []
            planename = res[1]
            planekey = res[2]
            continue

        if bstart:
            res = findDataLine(ln)
            if res:
                line = res[0][1:-1].split('), (')
                # print(line)

                alldata = [s.split(', ') for s in line]
                # print(alldata)

                pairs = [(int(d[0]), float(d[1])) for d in alldata]
                # print(pairs)
                oneplane += pairs
                continue

            res = findEndLine(ln)
            if res:
                bstart = False

                mm_list = [i[1] for i in oneplane]
                mm_lists = [abs(i) for i in mm_list]
                mm_split_list = split_list(mm_lists, 4)
                mm_dict = avg_dict(mm_split_list)
                print("zxf:",mm_dict)

                planes[planekey] = {"name": planename, "data": oneplane, "avg": mm_dict}
                # print(oneplane)
                print(planekey, planename, len(oneplane))
                print("zxf:", planekey, planename, oneplane)

    return planes


# 58 tka
cnPlaneNames = {
    '2': '胫骨',
    '3': '股骨远端',
    '4': '股骨前侧',
    '5': '股骨后侧',
    '6': '股骨后斜',
    '7': '股骨前斜',
}

# 68 tka
# cnPlaneNames = {
#     '3': '胫骨',
#     '4': '股骨远端',
#     '5': '股骨前侧',
#     '6': '股骨后侧',
#     '7': '股骨后斜',
#     '8': '股骨前斜',
# }


def outputCSV(allplanedata, title):
    plankeys = list(allplanedata.keys())
    plankeys.sort()
    count = len(plankeys)

    # zxf作用：排序后键与存放刀位名称一致
    titles = [cnPlaneNames[k] for k in plankeys]

    # zxf作用：统计列名，列数据个数
    headers = []
    lengths = []
    for k in plankeys:
        headers.append(cnPlaneNames[k] + '时间(ms)')
        headers.append(cnPlaneNames[k] + '偏移(mm)')
        lengths.append(len(allplanedata[k]["data"]))

    maxrow = max(lengths)
    print(maxrow, lengths)

    with open(title + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in range(maxrow):
            row = []

            for k in plankeys:
                data = allplanedata[k]["data"]
                count = len(data)
                print(r)
                print(count)
                if r < count:
                    row += [data[r][0], data[r][1]]
                else:
                    row += ['', '']
            writer.writerow(row)


def drawFigure(allplanedata, title):
    plankeys = list(allplanedata.keys())
    plankeys.sort()
    count = len(plankeys)

    titles = [cnPlaneNames[k] for k in plankeys]
    titles_avg = [allplanedata[k]["avg"] for k in plankeys]
    new_titles = [i[0]+str(i[1]) for i in zip(titles,titles_avg)]
    print("zxf avg:",new_titles)

    fig = make_subplots(rows=count, cols=1, shared_xaxes=True, vertical_spacing=0.06,
                        subplot_titles=new_titles)

    for r in range(count):
        k = plankeys[r]

        times = [x[0] for x in allplanedata[k]["data"]]
        shifts = [x[1] for x in allplanedata[k]["data"]]

        fig.add_trace(
            go.Scatter(x=times, y=shifts, name=allplanedata[k]['name']),
            row=r + 1, col=1)

    # Add figure title
    fig.update_layout(
        title_text=title, yaxis_range=[-1.5, 1.5],
        height=1200,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="time(ms)")
    fig.update_yaxes(title_text="偏移(mm)", range=[-1.5, 1.5])
    fig.show()
    ## 公司加密软件加密了plotly.min.js，导致kaleido无法正确解析，造成渲染失败。
    ## write_image to local 在未加密机器上征程
    # fig.write_image(title+".jpg")
    fig.write_html(title + ".html")


def handleLog(logname):
    allplanedata = readLog(logname)
    drawFigure(allplanedata, logname)
    outputCSV(allplanedata, logname)


logname = 'engineer.2024-02-02 09_51_52.log'
handleLog(logname)

import os, csv
import re, math
import numpy as np
import glob
import plotly
from chardet.universaldetector import UniversalDetector
import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""
方法功能：猜测文件编码类型
方法实现：
方法返回值类型：字典
方法返回值：编码类型
"""


def detectEncoding(filename):
    bigdata = open(filename, 'rb')
    detector = UniversalDetector()
    for line in bigdata.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    bigdata.close()
    return detector.result


"""
方法功能：切割列表长度
方法实现：
方法返回值类型：列表
方法返回值：指定段数的 列表数据
"""


def split_list(lst, num_parts):
    length = len(lst)
    part_size = length // num_parts
    remainder = length % num_parts

    result = []
    start = 0

    for i in range(num_parts):
        if i < remainder:
            end = start + part_size + 1
        else:
            end = start + part_size

        result.append(lst[start:end])
        start = end

    return result


"""
方法功能：计算列表平均值
方法实现：
方法返回值类型：列表
方法返回值：每段列表内数值的平均值
"""


def avg_list(mm_split_list):
    section_list = []
    for section in range(len(mm_split_list)):
        section_avg = sum(mm_split_list[section]) / len(mm_split_list[section])
        section_avg_int = round(section_avg, 2)
        section_list.append(section_avg_int)
    return section_list


"""
方法功能：找到符合正则表达式的数据
方法实现：
方法返回值类型：列表
方法返回值：匹配行的数据
"""


def findmatch(ln, strpat):
    res = []
    matchObj = re.match(strpat, ln)
    if matchObj:
        res = list(matchObj.groups())
    return res


"""
未应用
"""


def converMatches(reslist):
    result = []
    if (reslist):
        result.append(reslist[0])
        result.append([float(x) for x in reslist[1:]])
    return result


"""
方法功能：自定义正则表达式
方法实现：
方法返回值类型：列表
方法返回值：匹配数据
"""


def findStartLine(ln):
    strpat = '.+LogOffset start offset log of Cut step ((.+) \((\d)\))'
    return findmatch(ln, strpat)


def findEndLine(ln):
    strpat = '.+LogOffset complete offset log of Cut step (.+)'
    return findmatch(ln, strpat)


def findDataLine(ln):
    strpat = '.+LogOffset offset\[.+\]  time\(ms\),offset\(mm\): (.+)'
    return findmatch(ln, strpat)


"""
方法功能：读日志log文件
方法实现：
方法返回值类型：字典
方法返回值：键：各个刀位名称，值：各个刀位名称，数据，平均值
"""


def readLog(fname):
    detres = detectEncoding(fname)
    print(detres)

    content = open(fname, 'rb').read()

    loglns = content.decode(encoding=detres['encoding'], errors='ignore').splitlines()

    bstart = False
    planes = {}
    planekey = ""
    for ln in loglns:
        res = findStartLine(ln)
        if res:
            bstart = True
            oneplane = []
            planename = res[1]
            planekey = res[2]
            continue

        if bstart:
            res = findDataLine(ln)
            if res:
                line = res[0][1:-1].split('), (')

                alldata = [s.split(', ') for s in line]

                pairs = [(int(d[0]), float(d[1])) for d in alldata]
                oneplane += pairs
                continue

            res = findEndLine(ln)
            if res:
                bstart = False


                times = (oneplane[-1][0] - oneplane[0][0]) / 1000
                print("zxf刀位时间：", oneplane[-1][0], oneplane[0][0], times)

                cut_oneplane = oneplane[5:-5]
                cut_times = (cut_oneplane[-1][0] - cut_oneplane[0][0]) / 1000

                planes[planekey] = {"name": planename, "data": oneplane,  "times": times,
                                    "cut_data": cut_oneplane, "cut_times": cut_times}
                print(planekey, planename, len(oneplane))

    return planes


cnPlaneNames = {}

"""
方法功能：根据截骨数据存储到excel
方法实现：
方法返回值类型：
方法返回值：生成Excel
"""


def outputCSV(allplanedata, title):
    plankeys = list(allplanedata.keys())
    # plankeys.sort()
    count = len(plankeys)

    titles = [cnPlaneNames[k] for k in plankeys]

    headers = []
    lengths = []
    for k in plankeys:
        headers.append(cnPlaneNames[k] + '时间(ms)')
        headers.append(cnPlaneNames[k] + '偏移(mm)')
        lengths.append(len(allplanedata[k]["data"]))

    maxrow = max(lengths)
    print(maxrow, lengths)

    with open(title + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
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


"""
方法功能：根据截骨数据画图
方法实现：
方法返回值类型：
方法返回值：生成html
"""


def drawFigure(allplanedata, title):
    plankeys = list(allplanedata.keys())
    plankeys.sort()
    count = len(plankeys)

    titles = [cnPlaneNames[k] for k in plankeys]
    titles_times = [allplanedata[k]["times"] for k in plankeys]
    new_titles = [i[0] + " 总用时:" + str(i[1]) + "秒" for i in
                  zip(titles, titles_times)]
    print("zxf avg titles:", new_titles)

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


"""
方法功能：(去除前5点)根据截骨数据画图
方法实现：
方法返回值类型：
方法返回值：生成html
"""


def drawFigure_cut_planedata(allplanedata, title):
    # title_join = ".\剔除前后5点" + title

    plankeys = list(allplanedata.keys())
    plankeys.sort()
    count = len(plankeys)

    titles = [cnPlaneNames[k] for k in plankeys]
    titles_times = [allplanedata[k]["cut_times"] for k in plankeys]
    new_titles = [i[0] + " 总用时:" + str(i[1]) + "秒" for i in
                  zip(titles, titles_times)]
    print("zxf avg titles:", new_titles)

    fig = make_subplots(rows=count, cols=1, shared_xaxes=True, vertical_spacing=0.06,
                        subplot_titles=new_titles)

    for r in range(count):
        k = plankeys[r]

        times = [x[0] for x in allplanedata[k]["cut_data"]]
        shifts = [x[1] for x in allplanedata[k]["cut_data"]]

        fig.add_trace(
            go.Scatter(x=times, y=shifts, name=allplanedata[k]['name']),
            row=r + 1, col=1)

    # Add figure title
    fig.update_layout(
        title_text="剔除前后5点"+title, yaxis_range=[-1.5, 1.5],
        height=1200,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="time(ms)")
    fig.update_yaxes(title_text="偏移(mm)", range=[-1.5, 1.5])
    fig.show()
    ## 公司加密软件加密了plotly.min.js，导致kaleido无法正确解析，造成渲染失败。
    ## write_image to local 在未加密机器上征程
    # fig.write_image(title+".jpg")
    fig.write_html(title + "剔除前后5点" + ".html")


"""
方法功能：查找指定文件名称的文件
方法实现：
方法返回值类型：列表
方法返回值：文件路径
"""


def find_file():
    # dir_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = "../曹惠君/"
    files_list = glob.glob(os.path.join(dir_path, "engineer*"))
    print("zxf 文件路径",files_list)
    return files_list


def find_root_file():
    root_folder = './'
    file_name_contains = 'engineer'
    file_path_list = []
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            if file_name_contains in file_name:
                # 文件名符合条件，进行相应操作
                file_path = os.path.join(root, file_name)
                file_path_list.append(file_path)
    return file_path_list



"""
方法功能：判断日志的手术类型，区分5800 与 6800
方法实现：
方法返回值类型：列表
方法返回值：5800文件路径，6800文件路径
"""


def judge_operation_type(file_lists):
    specified_character = "engineer.knee"
    global cnPlaneNames
    spexpert_knee = []
    spexpert = []
    for f in file_lists:
        if specified_character in f:
            spexpert_knee.append(f)
        else:
            spexpert.append(f)
    print("6800日志：", spexpert_knee)
    print("5800日志：", spexpert)
    return spexpert, spexpert_knee


"""
方法功能：处理log，读，画图，输出Excel
方法实现：
方法返回值类型：
方法返回值：
"""


def handleLog(logname):
    allplanedata = readLog(logname)
    drawFigure(allplanedata, logname)
    drawFigure_cut_planedata(allplanedata,logname)
    outputCSV(allplanedata, logname)


"""
方法功能：开始处理58日志与68日志
方法实现：
方法返回值类型：
方法返回值：
"""


def start_handle(s_log_lists, s_k_log_lists):
    global cnPlaneNames
    for s in s_log_lists:
        cnPlaneNames = {
            '2': '胫骨',
            '3': '股骨远端',
            '4': '股骨前侧',
            '5': '股骨后侧',
            '6': '股骨后斜',
            '7': '股骨前斜',
        }
        handleLog(s)
    for s_k in s_k_log_lists:
        cnPlaneNames = {
            '3': '胫骨',
            '4': '股骨远端',
            '5': '股骨前侧',
            '6': '股骨后侧',
            '7': '股骨后斜',
            '8': '股骨前斜',
        }
        handleLog(s_k)


log_file_paths = find_root_file()
spexpert_log_lists, spexpert_knee_log_lists = judge_operation_type(log_file_paths)
start_handle(spexpert_log_lists, spexpert_knee_log_lists)

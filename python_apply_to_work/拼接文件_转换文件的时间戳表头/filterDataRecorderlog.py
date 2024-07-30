'''
Filter data recorder log
V 1.0 2023/8/21
'''

# 处理一次手术的datarecoder*.log
# 如果有多个，按时间顺序合并
# 对log进行处理，转成标准csv格式
#   1. 最前面增加列， timeSpanMs, DateTimeStr, TimeStr, TimeInMs。 timeSpanMs为每行时间减第一行时间
#   2. 修改标题，去掉 %，添加新列标题
# 输出保存成csv，','分隔

'''
zxf理解功能实现流程：
    1.使用传入开始时间戳与结束时间戳 来决定了要处理的数据的行数范围
    2.先规定好要增加便于观看数据的 表头
    3.通过原数据的时间戳 转换出 便于观看的时间字符串
    4.为原始每行数据开头增加上 时间字符串
    5.按行在次输出这俩组数据，得到了新的excel
'''



import os, csv, glob
import datetime, time, calendar
import math
import re
import argparse

EXECEL_CSV = True # output csv could be open by Excel directly


# zxf:将时间戳与毫秒戳 转换成为便于观看的时间格式
# used for app log and datarecorder log of sunrise 1.15
def convertEpochToTime(TimeInSec, TimeInNanoSec):
    msPart = TimeInNanoSec // 1000000
    timeInMs = TimeInSec * 1000 + msPart

    t = datetime.datetime.utcfromtimestamp(TimeInSec)
    t += datetime.timedelta(milliseconds=msPart)
    # print(type(t))
    # print(t, t.microsecond)
    datetimestring = t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    timestring = t.strftime('%H:%M:%S.%f')[:-3]
    # print(timestring)

    return timeInMs, datetimestring, timestring


# string should like this '2000-01-01 12:34:00'
def convertLocalTimeToEpoch(localtimeStr):

    timeInSec = time.mktime(time.strptime(localtimeStr, '%Y-%m-%d %H:%M:%S'))
    return timeInSec


# zxf:将正常格式时间转换成为时间戳  用做后面 行数据的取值范围
# dataRecorder convert local time to epoch as GMT time
def convertUTCTimeToEpoch(localtimeStr):

    timeInSec = calendar.timegm(
        time.strptime(localtimeStr, '%Y-%m-%d %H:%M:%S.%f'))
    return timeInSec


# timeInMs, timestring = convertEpochToTime(1668535330, 964000000)
# print(timeInMs, timestring)
# 1668535330   964000000
# Nov 15 2022 18:02:10 GMT+0000
# 2022-11-15 18:02:10,922


# zxf:将表头 与 数据拆开
def readOneLog(logpath):
    lines = open(logpath).readlines()  # skip header
    return lines[0], lines[1:]


# zxf:生成新的表头
def processHeader(header):
    parts = header.split()
    parts = [s.replace("_LBR_Med_14_R820_1", "") for s in parts]
    parts = ['timeSpanMs', 'timeInMs', 'datatimeStr', 'timeStr'] + parts[1:]
    # print(parts)
    return ','.join(parts) + '\n'


def getLineTime(dl):
    dlparts = dl.split()
    # dlparts[0] dlparts[1] log中真实数据为:1721930334   663000000
    timeInMs, dtstr, timestr = convertEpochToTime(int(dlparts[0]), int(dlparts[1]))
    return timeInMs, dtstr, timestr


# zxf:在每行原始数据开头位置 增加了四个便于观看的时间字符串
def modifyDataLines(lines):
    basetimeInMs, _, _ = getLineTime(lines[0])

    newLines = []

    for dl in lines:
        timeInMs, dtstr, timestr = getLineTime(dl)
        timeSpan = timeInMs - basetimeInMs
        newln = [str(timeSpan), str(timeInMs), dtstr, timestr]
        if EXECEL_CSV: 
            newln = ['"{}"'.format(x) for x in newln]
        print(newln)
        newln += dl.split()
        newLines.append(','.join(newln) + '\n')
    return newLines


# zxf:一行一行的写入方式 先写表头 在写数据
def outputResult(csvpath, header, lines):
    with open(csvpath, 'wt') as csvfile:
        csvfile.write(header)
        csvfile.writelines(lines)


def getStartEndMs(start, end):
    if start:
        startEpochMs = int(convertUTCTimeToEpoch(start) * 1000)
    else:
        startEpochMs = 0

    if end:
        endEpochMs = int(convertUTCTimeToEpoch(end) * 1000)
    else:
        # zxf：1e16 表示其值为 10000000000000000.0
        endEpochMs = 1e16

    return startEpochMs, endEpochMs


# zxf:根据时间戳 拿到数据中的 开始行号与结束行号
def getLineRange(lines, start, end):
    startEpochMs, endEpochMs = getStartEndMs(start, end)

    startline = len(lines)
    endline = len(lines)
    for lnnum in range(len(lines)):
        timeInMs, _, _ = getLineTime(lines[lnnum])
        if timeInMs >= startEpochMs:
            startline = lnnum
            break

    for lnnum in range(startline, len(lines)):
        timeInMs, _, _ = getLineTime(lines[lnnum])
        if timeInMs > endEpochMs:
            endline = lnnum
            break
    return startline, endline


def processLines(header, lines, csvpath, start, end):
    #print("header", header)
    print("data lines", len(lines))

    newHeader = processHeader(header)
    #print("new header", newHeader)

    # lines = lines[0:1000]

    startline, endline = getLineRange(lines, start, end)

    print("lines in time range: {} - {}".format(startline, endline))

    if startline >= endline :
        print("thers is not valid line in time range.")
        return
    
    print("first line in time range:", startline)
    print(lines[startline])

    lines = lines[startline:endline]

    newLines = modifyDataLines(lines)
    # print(newLines)

    outputResult(csvpath, newHeader, newLines)
    print("output csv " + csvpath)


def getLogNumber(logname):
    # print(logname)
    pat = '.*dataRecording_(\d+)\.log'
    m = re.match(pat, logname)
    # print(m[1])
    return int(m[1])


# zxf:先使用glob模块找到符合字符串的文件，使用sort函数排序 排序键传的函数 函数是获取到文件的序号
# read multiple logs in one test
def readRecorderFiles(dirname):
    logfiles = glob.glob(os.path.join(dirname, "dataRecording_*.log*"))

    logfiles.sort(reverse=True, key=getLogNumber)
    print("sorted log fiels:", logfiles)

    # zxf:因每个文件的表头都一样 所以不要管让其覆盖 只会赋值出一行，而数据是累加每次切片出第一行表头
    loglns = []
    header = ''
    for logfile in logfiles:
        lns = open(logfile).readlines()
        header = lns[0]
        loglns += lns[1:]  # skip header line

    return header, loglns


# zxf:处理一个log
def processOneLog(logpath, csvpath, start, end):

    header, lines = readOneLog(logpath)
    processLines(header, lines, csvpath, start, end)


# zxf:处理一个log目录
def processOneLogDir(logpath, csvpath, start, end):

    header, lines = readRecorderFiles(logpath)
    processLines(header, lines, csvpath, start, end)


logpath = r'0726dataRecording_01.log'
csvpath = '240726.csv'
start = ''
end = ''

processOneLog(logpath, csvpath, start, end)


logdir = r'240726'
csvpath = '240726.csv'


start = '2023-11-06 10:33:20.000'
end = '2023-11-06 10:33:40.000'

start = ''
end = ''

# processOneLogDir(logdir, csvpath, start, end)


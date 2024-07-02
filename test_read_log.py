import re

ln = "2024-01-03 13:40:20.826 [INFO]:6744	[offsetRecorder]:45	LogOffset start offset log of Cut step femur DISTAL (4)"
lns = '2022-09-02 13:52:10.112 [INFO]:4444	[offsetRecorder]:45	LogOffset start offset log of Cut step tibia (2)'
strpat = '.+LogOffset start offset log of Cut step ((.+) \((\d)\))'


def findmatch(ln, strpat):
    res = []
    matchObj = re.match(strpat, ln)
    if matchObj:
        res = list(matchObj.groups())
    return res


def findStartLine(ln):
    # strpat = '.+LogOffset start offset log of Cut step ((.+) \((\d)\))'
    return findmatch(ln, strpat)


z = findStartLine(ln)
print("正则匹配后：{}".format(z))
print(findStartLine(lns))

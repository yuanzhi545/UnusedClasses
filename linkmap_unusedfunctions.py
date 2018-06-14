#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import os
import re
import xlwt

if len(sys.argv) < 3:
	print '请在.py文件后面输入linkMap文件路径 以及 运行文件'
	sys.exit()

linkMapPath = sys.argv[1]
print 'linkMap文件路径%s' % linkMapPath

functions = []

file = open(linkMapPath, 'r')
content = file.read()
file.close()

file = open(linkMapPath, 'r')
for line in file.readlines():
    line = line.strip()
    searchObj = re.search(r'[-+]\[\w+\s[\w:]+\]',line)
    if searchObj != None:
        array = line.split()
        if int(array[1],16) > 512:
            function = searchObj.group()
            array2 = function.split()
            className2 = array2[0]
            if className2.startswith('SD') == False and 'Vip' not in className2 and 'DOV' not in className2 and 'Lua' not in className2 and 'SDCentralManager' not in className2 and '_' not in className2 and 'Airdrop' not in className2 and function + '_block_invoke' not in content:
                function = function.replace('+','')
                function = function.replace('-','')
                function = function.replace('[','')
                function = function.replace(']','')
                functions.append(function + ' ' + array[1])

functions = set(functions)

usedPath1 = sys.argv[2]
usedFile1 = open(usedPath1,'r')
usedContent1 = usedFile1.read()


filePrePath = os.path.split(linkMapPath)[0]
writePath = '%s/无用函数.xls' % filePrePath
if os.path.exists(writePath):
    os.remove(writePath)

style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='#,##0')
wb = xlwt.Workbook(encoding = 'utf-8')
ws = wb.add_sheet('Sheet1')
row = 0

totalCount = len(functions)
startIndex = 0
for function in functions:
    startIndex = startIndex+1
    array = function.split()
    className = array[0]
    functionName = array[1]
    size = array[2]
    if 'searchBar' not in functionName and 'mqq' not in functionName and 'delegate' not in functionName and'searchDisplayController:' not in functionName and 'handleView:' not in functionName and 'parser:' not in functionName and 'handleJsBridgeRequest' not in functionName and 'tableView:' not in functionName and 'scrollView' not in functionName and functionName not in usedContent1:
        ws.write(row,0,className,style0)
        ws.write(row,1,functionName,style0)
        ws.write(row,2,int(size,16),style0)
        row += 1
        print '无用函数:%s' % functionName

print '扫描结束!!!'
wb.save(writePath)
file.close()
usedFile1.close()



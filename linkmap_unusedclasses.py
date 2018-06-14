#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import os
import re
import xlwt

if len(sys.argv) < 4:
	print '请在.py文件后面输入 classlist classrefs linkmap等文件'
	sys.exit()

classlistPath = sys.argv[1]
print 'linkMap文件路径%s' % classlistPath

classrefsFile = open(sys.argv[2],'r')
classrefsContent = classrefsFile.read()

unusedclassList= []
file = open(classlistPath, 'r')
for line in file.readlines():
    line = line.replace('\\','')
    array = line.split()
    startIndex = 0
    for str in array:
        if startIndex > 0 and str != '00000000':
            if str not in classrefsContent:
                unusedclassList.append(str.upper())
        startIndex += 1

unusedclass = []

for address in unusedclassList:
    linkMapFile = open(sys.argv[3],'r')
    for line in linkMapFile.readlines():
        if address in line:
            array = line.split('_')
            className = array[-1]
            upperClassName = className.upper()
            if upperClassName.startswith('UI') or upperClassName.startswith('AP') or upperClassName.startswith('QZ') or upperClassName.startswith('QQWLX') or upperClassName.startswith('OCS') or upperClassName.startswith('YKT') or upperClassName.startswith('QQWALLET') or upperClassName.startswith('QQLIGHT') or upperClassName.startswith('QQAIO') or 'TPECCRYPT' in upperClassName or 'JS' in upperClassName or 'BASE' in upperClassName or 'REQ' in upperClassName or 'RSP' in upperClassName or '_OBJC_CLASS_$_'+className not in line:
                break
            unusedclass.append(className)
            print '无用的类：%s' % className
            break
    linkMapFile.close()

filePrePath = os.path.split(classlistPath)[0]
writePath = '%s/无用类.xls' % filePrePath
if os.path.exists(writePath):
    os.remove(writePath)

style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='#,##0')
wb = xlwt.Workbook(encoding = 'utf-8')
ws = wb.add_sheet('Sheet1')
row = 0
for className in unusedclass:
    ws.write(row,0,className,style0)
    row += 1

print '扫描结束!!!'
wb.save(writePath)

file.close()
classrefsFile.close()

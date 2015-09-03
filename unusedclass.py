#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import os
import re

if len(sys.argv) == 1:
	print '请在.py文件后面输入工程路径' 
	sys.exit()

projectPath = sys.argv[1]
print '工程路径为%s' % projectPath

resourcefile = []
totalClass = set([])
unusedFile = []
pbxprojFile = []

def Getallfile(rootDir): 
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        if os.path.isdir(path): 
            Getallfile(path) 
        else:
        	ex = os.path.splitext(path)[1]  
        	if ex == '.m' or ex == '.mm' or ex == '.h':
        		resourcefile.append(path)
        	elif ex == '.pbxproj':
        		pbxprojFile.append(path)

Getallfile(projectPath)

print '工程中所使用的类列表为：'
for ff in resourcefile:
    print ff

for e in pbxprojFile:
    f = open(e, 'r')
    content = f.read()
    array = re.findall(r'\s+([\w,\+]+\.[h,m]{1,2})\s+',content)
    see = set(array)
    totalClass = totalClass|see
    f.close()

print '工程中所引用的.h与.m及.mm文件'
for x in totalClass:
    print x
print '--------------------------'

for x in resourcefile:
    ex = os.path.splitext(x)[1]
    if ex == '.h': #.h头文件可以不用检查
        continue
    fileName = os.path.split(x)[1]
    print fileName
    if fileName not in totalClass:
        unusedFile.append(x)

for x in unusedFile:
    resourcefile.remove(x)

print '未引用到工程的文件列表为：'

writeFile = []
for unImport in unusedFile:
    ss = '未引用到工程的文件:%s\n' % unImport
    writeFile.append(ss)
    print unImport

unusedFile = []

allClassDic = {}

for x in resourcefile:
    f = open(x,'r')
    content = f.read()
    array = re.findall(r'@interface\s+([\w,\+]+)\s+:',content)
    for xx in array:
        allClassDic[xx] = x
    f.close()

print '所有类及其路径：'
for x in allClassDic.keys():
    print x,':',allClassDic[x]

def checkClass(path,className):
    f = open(path,'r')
    content = f.read()
    if os.path.splitext(path)[1] == '.h':
        match = re.search(r':\s+(%s)\s+' % className,content)
    else:
        match = re.search(r'(%s)\s+\w+' % className,content)
    f.close()
    if match:
        return True

ivanyuan = 0
totalIvanyuan = len(allClassDic.keys())

for key in allClassDic.keys():
    path = allClassDic[key]
    
    index = resourcefile.index(path)
    count = len(resourcefile)
    
    used = False
    
    offset = 1
    ivanyuan += 1
    print '完成',ivanyuan,'共:',totalIvanyuan,'path:%s'%path
    
    
    while index+offset < count or index-offset > 0:
        if index+offset < count:
            subPath = resourcefile[index+offset]
            if checkClass(subPath,key):
                used = True
                break
        if index - offset > 0:
            subPath = resourcefile[index-offset]
            if checkClass(subPath,key):
                used = True
                break
        offset += 1

    if not used:
        str = '未使用的类：%s 文件路径：%s\n' %(key,path)
        unusedFile.append(str)
        writeFile.append(str)

for p in unusedFile:
    print '未使用的类：%s' % p

filePath = os.path.split(projectPath)[0]
writePath = '%s/未使用的类.txt' % filePath
f = open(writePath,'w')
f.writelines(writeFile)
f.close()


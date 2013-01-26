"""
utils.py
Quincy Lam
Licensed under CC BY SA 3.0

Includes all kinds of useful functions that I wrote for writing the book.

findOccurences: create a tab separated chart of certain words and their occurences
findUnkownWords: creates a tab-separated list of words that are surrounded by ？？ ？？, meaning I do not know how to translate them (and yet must)
replaceVariants: replaces characters with the variants that I favour
updateStats: updates various statistics (tab-separated)
"""

import re
from time import clock

allTexts = ["part1/" + str(n) for n in range(1,9)] + ["part2/" + str(n) for n in range(1,10)] + ["part3/" + str(n) for n in range(1,7)] + ["other/" + title for title in ["foreword","appendix","afterword"]]

"""
Helper generator that yields tuples of file objects and filenames (str)
"""
def allFiles():
    for filename in allTexts:
        a = open(filename, "r+")
        yield a, filename
        a.close()

"""
Write headings i.e. part1/1, part1/2 etc.
"""
def writeHeadings(f):
    f.write('filename')
    for filename in allTexts:
        f.write('\t' + filename)
    f.write("\n")

def findOccurences():
    chars = [line.split('\t')[0] for line in open("characterGlossary","r").readlines()]
    occurences = open("occurences","w")
    writeHeadings(occurences)
    toWrite = []
    for char in chars:
        toWrite.append([char])
        for a,filename in allFiles():
            #print("Finding occurences in " + filename)
            if char in a.read():
                toWrite[:-1].append('x')
            else:
                toWrite[:-1].append('')
    occurences.write('\n'.join('\t'.join(line) for line in toWrite))
    occurences.close()
        

def findUnknownWords():
    unknowns = open("unknowns", "w")
    toWrite = []
    for a,filename in allFiles():
        #print("Searching through " + filename)
        matches = re.search(r'？？.+?？？', a.read())
        if matches:
            for match in matches:
                toWrite.append(filename + "\t" + re.replace("？？","",match))
    unknowns.write('\n'.join(toWrite))
    unknowns.close()

def replaceVariants():
    chars = {"偽":"僞", "着":"著", "濕":"溼", "秘":"祕", "真":"眞", "鎮":"鎭", "啟":"啓", "羮":"羹", "舖":"鋪",  
    #說文: the latter is sad whilst the former is happy
    "歎":"嘆",
    #單只 means odd. Std Chinese for m daan zi is 不單止
    "毋單只":"毋單止", "邏輯":"羅輯", "唯":"惟", "群":"羣", "裡":"裏", "輸":"輸", "厠":"廁", "沉":"沈", "失縱":"失蹤", "减":"減", "鑒":"鑑", "直":"直", "即":"卽", "值":"値", "郎":"郞", "(户|戸)":"戶", "泄漏":"洩漏", 
    #But 象 > 𧰼
    "像":"像", "史密斯":"斯滅", "㦸":"戟", "批蕩":"批盪", "模仿":"模倣", "傚仿|效倣|效仿":"傚倣", "逗留":"逗遛", "朵":"朶", "棵":"樖", "床":"牀", "黄":"黃", "部分":"部份", "屏":"屛", "偋":"𠌸", "清":"淸", "青":"靑", "麵":"麪", "雕":"彫", "游行":"遊行", "巡游":"巡遊", "逼近":"迫近", "螺母":"螺帽", "墻":"牆", "部分":"部份", "犁":"犂", "了解":"瞭解", 
    # 嫗㛒?    
    "牛豆":"怐豆", "(煅煉|鍛煉|煅鍊)":"鍛鍊", "花崗靑":"花剛巖", "撴":"撉", "下巴":"下爬", "嗍":"欶", "掰":"擘", "等於|等如":"等于", "研":"硏"}

    for a,filename in allFiles():
        #print("Replacing for " + filename)
        body = a.read()
        for k,v in chars.items():
            body = re.sub(k, v, body) 
        a.seek(0)
        a.write(body)
    
def updateStats():
    # A dict of statistic names to lambda functions
    stats = { "characters" : lambda s:len(s) - len(re.search(r'（|）|—|：|；|，|。|「|」|『|』|！|？|、|\n', s).groups()) }
    record = open("stats","w")
    writeHeadings(record)
    toWrite = []
    for stat,f in stats.items():
        toWrite.append([stat])
        for a,filename in allFiles():
            toWrite[:-1] += '\t' + str(f(a.read()))
    record.write('\n'.join(toWrite))
    record.close()
            

if __name__ == "__main__":
    a = clock()
    replaceVariants()    
    print("Variants replaced: {} ticks".format(clock() - a))
    findOccurences()
    print("Occurences found: {} ticks".format(clock() - a))
    findUnknownWords()
    print("Unknown words found: {} ticks".format(clock() - a))
    updateStats()
    print("Elapsed: {} ticks".format(clock() - a))

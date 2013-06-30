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

allTexts = ["part1/" + str(n) + ".tex" for n in range(1,9)] + ["part2/" + str(n) + ".tex" for n in range(1,10)] + ["part3/" + str(n) + ".tex" for n in range(1,7)] + ["other/" + title +".tex" for title in ["foreword","appendix","afterword"]]

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
	#Let the first line be for headings
	chars = [line.split('\t')[0] for line in open("characterGlossary","r").readlines()[1:]]
	occurences = open("occurences","w")
	writeHeadings(occurences)
	toWrite = []	
	for a,filename in allFiles():
		for i, char in enumerate(chars):
			if len(toWrite) < i + 1:
				toWrite.append([char])
			#print("Finding occurences in " + filename)
			toWrite[i].append('')
			print(toWrite[i])
			for paraNo,para in enumerate(a.read().split('\n\n')):
				if char in para:
					toWrite[i][-1] = str(paraNo)
					break
			a.seek(0)
	occurences.write('\n'.join('\t'.join(line) for line in toWrite))
	occurences.close()
		

def findUnknownWords():
	unknowns = open("unknowns", "w")
	toWrite = []
	for a,filename in allFiles():
		#print("Searching through " + filename)
		for match in re.finditer(r'？？(.+?)？？', a.read(), re.DOTALL):
			toWrite.append(filename + "\t" + match.group(1))
	unknowns.write('\n'.join(toWrite))
	unknowns.close()

def replaceVariants():
	print("DID YOU MAKE A COMMIT FIRST? IF THE LATEX ERRORS, THE BACKUPS MAY NOT EXIST AND YOU WILL HAVE TO DISCARD YOUR UNCOMMITTED CHANGES TO GET RID OF ESOTERIC PUNCTUATION. IF YOU DID NOT, DO IT NOW. OTHERWISE, ENTER 'YeS'")
	if input() != "YeS":
		return

	chars = {"偽":"僞", "為":"爲", "着":"著", "濕":"溼", "秘":"祕", "真":"眞", "鎮":"鎭", "啟":"啓", "羮":"羹", "舖":"鋪",  "搵":"捃",
	#說文: the latter is sad whilst the former is happy
	"歎":"嘆",
	#單只 means odd. Std Chinese for m daan zi is 不單止
	"毋單只":"毋單止", "邏輯":"羅輯", "唯":"惟", "群":"羣", "裡":"裏", "輸":"輸", "厠":"廁", "沉":"沈", "失縱":"失蹤", "减":"減", "鑒":"鑑", "即":"卽", "值":"値", "郎":"郞", "(户|戸)":"戶", "泄漏":"洩漏", 
	#But 象 > 𧰼
	"像":"像", "㦸":"戟", "批蕩":"批盪", "模仿":"模倣", "傚仿|效倣|效仿":"傚倣", "逗留":"逗遛", "朵":"朶", "棵":"樖", "床":"牀", "黄":"黃", "部分":"部份", "屏":"屛", "偋":"𠌸", "清":"淸", "青":"靑", "麵":"麪", "雕":"彫", "游行":"遊行", "巡游":"巡遊", "逼近":"迫近", "螺母":"螺帽", "墻":"牆", "部分":"部份", "犁":"犂", "了解":"瞭解", "牛豆|怐豆":"牛鬥", "(煅煉|鍛煉|煅鍊)":"鍛鍊", "花崗靑":"花剛巖", "撴":"撉", "下巴":"下爬", "嗍":"欶", "掰":"擘", "等於|等如":"等于", "研":"硏", "令":"令","零":"零","慎":"愼","說":"說","𥊙":"䁓","啱|懨":"懕","([^自])己":"\g<1>个","滯":"懠","([我你佢人])地":"\g<1>敵", "搣":"扒", "邋塌":"邋塌", "邋邋塌塌":"邋邋遢遢", "同埋":"同彌", "屋[企徛]":"屋其","裏面":"裏邊", "醒起":"省起", "搏命":"博命", "滾":"滚", "剷":"鏟", "挽":"輓", "須要":"需要", "繼承":"承繼",
	# 歰 is a modern known variant of 澀
	"澀":"歰",
	# Remove unncessary 係s
	"([惟剩亦但先])係":"\g<1>",
	# names
	"斯滅|[Ss]mith":"斯篾", "[eE]mmanuel":"伊曼紐", "[gG]oldstein":"葛士田", "[pP]arty|其黨":"黨",
	#︐︑︒︓︔︕︖﹃﹄﹁﹂︵︶︽︾︙︱
	"「":"﹁","」":"﹂","『":"﹃","』":"﹄","，":"︐","、":"︑","。":"︒",
"：":"︓","；":"︔","！":"︕","？":"︖","（":"︵","）":"︶","《":"︽",
"》":"︾","—":"︱","…":"︙"," · ":"・",

	# Prevent telling spaces after every unusual character
	"\n\\\\":"%\n\\\\", "}\n":"}%\n"}

	for a,filename in allFiles():
		#print("Replacing for " + filename)
		body = a.read()
		a.close()
		originalLength = len(body)
		for k,v in chars.items():
			body = re.sub(k, v, body)
		"""
		This is insufficient because the new string is often shorter.
		a.seek(0)
		a.write(body)
		"""
		b = open(filename, "w")
		b.write(body)
		b.close()

def replaceGlobally(a,b):
	for a,filename in allFiles():
		body = re.sub(a, b, a.read())
		a.seek(0)
		a.write(body)
	
def updateStats():
	# A dict of statistic names to lambda functions
	stats = { "characters" : (lambda s:len(s) - len(re.search(r'（|）|—|：|；|，|。|「|」|『|』|！|？|、|\n', s).groups())) }
	record = open("stats","w")
	writeHeadings(record)
	toWrite = []
	for a,filename in allFiles():
		for i,(stat,f) in enumerate(stats.items()):
			if len(toWrite) < i + 1:
				toWrite.append(stat)
			toWrite[i] += '\t' + str(f(a.read()))
			a.seek(0)
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

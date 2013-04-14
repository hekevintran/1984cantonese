part1 := 1 2 3 4 5 6 7 8
part2 := 1 2 3 4 5 6 7 8 9
part3 := 1 2 3 4 5 6
other := foreword afterword insideCover glossary

part1Files := $(foreach ch,$(part1),part1/$(ch).tex)
part2Files := $(foreach ch,$(part2),part2/$(ch).tex)
part3Files := $(foreach ch,$(part3),part3/$(ch).tex)
otherFiles := $(foreach filename,$(other), other/$(filename).tex)
 
main.pdf: main.tex $(part1Files) $(part2Files) $(part3Files) $(otherFiles)
	xelatex main.tex
	xelatex main.tex

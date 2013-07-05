part1 := 1 2 3 4 5 6 7 8
part2 := 1 2 3 4 5 6 7 8 9
part3 := 1 2 3 4 5 6
other := foreword afterword insideCover glossary appendix

part1Files := $(foreach ch,$(part1),part1/$(ch).tex)
part2Files := $(foreach ch,$(part2),part2/$(ch).tex)
part3Files := $(foreach ch,$(part3),part3/$(ch).tex)
otherFiles := $(foreach filename,$(other), other/$(filename).tex)

copySuffix = formatted
 
main.pdf: main.tex main.bib $(part1Files) $(part2Files) $(part3Files) $(otherFiles)
	# Don't do a ritual commit, since the python script should remind you.
	# Copies the files, appending a 2, and processes these copies
	for file in $(part1Files) $(part2Files) $(part3Files) $(otherFiles) ; do \
		cp $$file $$file.$(copySuffix) ; \
		python3 utils.py $$file.$(copySuffix) ; \
		done
	xelatex main.tex
	biber main
	xelatex main.tex
	xelatex main.tex
	for file in $(part1Files) $(part2Files) $(part3Files) $(otherFiles) ; do \
		rm $$file.$(copySuffix) ; \
		done

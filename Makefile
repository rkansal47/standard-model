main.pdf:
	latexmk -interaction=nonstopmode -file-line-error -lualatex main.tex

make4ht:
	make4ht main.tex -l -f html5+dvisvgm_hashes+common_domfilters  "mathml,mathjax,3,Gin-percent,next,sec-filename,fn-in" -c config.cfg -e build.mk4

postprocess:
	mkdir -p out
	cp -r *.html *.svg assets figures *.css out/
	cp main.pdf out/standard-model.pdf
	python3 postprocess.py

website: main.pdf make4ht postprocess

clean:
	rm *.html *.svg *.pdf

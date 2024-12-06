main.pdf:
	latexmk -interaction=nonstopmode -file-line-error -lualatex main.tex

website: main.pdf
	make4ht main.tex -l -f html5+dvisvgm_hashes+common_domfilters  "mathml,mathjax,3,Gin-percent,next,sec-filename,fn-in" -c config.cfg -e build.mk4
	python3 postprocess.py
	mkdir -p out
	cp -r *.html *.svg assets figures standard-model.pdf *.css out/

clean:
	rm *.html *.svg *.pdf

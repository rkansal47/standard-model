pdf: 
	latexmk -interaction=nonstopmode -file-line-error -xelatex

website: main.pdf 
	make4ht main.tex -l -f html5+dvisvgm_hashes+common_domfilters  "mathml,mathjax,3,Gin-percent,next,sec-filename" -c config.cfg -e build.mk4
	python postprocess.py

clean:
	rm *.html *.svg *.pdf
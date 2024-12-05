# QFT Notes

Converted from latex to html using tex4ht.

- [QFT Notes](#qft-notes)
  - [Notes for compiling](#notes-for-compiling)
    - [Command](#command)
    - [Math](#math)
    - [TikZ / Feynman diagrams](#tikz--feynman-diagrams)
    - [Config](#config)


## Notes for compiling

### Command

```bash
make4ht main.tex  -f html5+dvisvgm_hashes+common_domfilters  "mathml,mathjax,3,Gin-percent,frames-fn,next,sec-filename" -c config.cfg
```

 - `mathml` and `mathjax` for [math](#math)
 - `3` means each subsection gets its own page
 - `Gin-percent` to use relative widths for figures
 - `frames-fn` for separate frames to the side for TOC and footnotes
 - `next` for "linear" next page - i.e. jumping to next subsection rather than next chapter
 - `sec-filename` for each html page named after its section
 - `dvisvgm_hashes`: better SVGs for TikZ
 - `common_domfilters`: probably not necessary

### Math

Using mathml + mathjax for the best equation rendering and referencing (mathml needed for custom macros).

Some notes:

 - The `resizegather` package caused rendering issues [#158](https://github.com/michal-h21/make4ht/issues/158).
 - `mathbbm` is not supported.
 - Equation splitting has issues by default, see [config](#config)
 - `nicefrac` is not well-supported and `cfrac` gives an error.


Mathjax-alone was briefly attempted. Was able to achieve chapter-wise number by followed this answer https://tex.stackexchange.com/a/714216 but changing section $\rightarrow$ chapter.

### TikZ / Feynman diagrams

 - On Mac, had to install Ghostscript and Ghostscript-extras from [MacTeX](https://www.tug.org/mactex/morepackages.html) (thanks to [this](https://tex.stackexchange.com/a/716651/361983) answer).
 - Had to replace all \( \)

### Config

 - Workaround for equation splitting issue from [#159](https://github.com/michal-h21/make4ht/issues/159)
 - 
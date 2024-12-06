# Notes on Symmetries, QFT, and the Standard Model

[![Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/rkansal47/standard-model/main.svg)](https://results.pre-commit.ci/latest/github/rkansal47/standard-model/main)

<p align="center">
  <img width="300" src="https://raw.githubusercontent.com/rkansal47/standard-model/assets/logo.png" />
</p>

Written in LaTeX and compiled as both a [PDF](https://github.com/rkansal47/standard-model/blob/gh-pages/standard-model.pdf?raw=true) and  [website](https://rkansal47.github.io/standard-model).

- [Notes on Symmetries, QFT, and the Standard Model](#notes-on-symmetries-qft-and-the-standard-model)
  - [Notes for LaTeX to HTML conversion](#notes-for-latex-to-html-conversion)
    - [Command](#command)
    - [Math](#math)
    - [TikZ / Feynman diagrams](#tikz--feynman-diagrams)
    - [Config](#config)
    - [Github Action](#github-action)


## Notes for LaTeX to HTML conversion

Conversion was done using [tex4ht](https://tug.org/tex4ht/) and the [make4ht](https://github.com/michal-h21/make4ht) build system.
h/t especially to Michal for his work on these tools and responsiveness to issues!
I tried `latexml` as well but got stuck because of [this](https://github.com/brucemiller/LaTeXML/issues/2268) issue, and also `pandoc` but it does not seem as well supported for LaTeX.
Some notes below for others' (and my own) future reference.

### Command

Run using the Makefile (`make website`). The underlying `make4ht` command is:

```bash
make4ht main.tex -l -f html5+dvisvgm_hashes+common_domfilters  "mathml,mathjax,3,Gin-percent,next,sec-filename,fn-in" -c config.cfg -e build.mk4
```

 - `mathml` and `mathjax` for [math](#math)
 - `3` means each subsection gets its own page
 - `Gin-percent` to use relative widths for figures
 <!-- - `frames-fn` for separate frames to the side for TOC and footnotes -->
 - `next` for "linear" next page - i.e. jumping to next subsection rather than next chapter
 - `sec-filename`: html page named after its section
 - `dvisvgm_hashes`: don't have to rebuild TikZ each time
 - `common_domfilters`: not sure what effect this has...
 - `config.cfg` and `build.mk4`: see [config](#config)

After this I do `python postprocess.py` to customize the main.html file and move divs around.

### Math

Using mathml + mathjax for the best equation rendering and referencing (mathml needed for custom macros).

Some notes:

 - The `resizegather` package caused rendering issues [#158](https://github.com/michal-h21/make4ht/issues/158) so I removed it.
 - Equation splitting has issues by default, see [config](#config).
 - The `newpx...` fonts mess up the math rendering so I import `amssymb` instead (only for the website) and change the font in CSS.
 - `mathbbm` is not supported $\rightarrow$ switched to `dsfont`.
 - `nicefrac` is not well-supported and `cfrac` gives an error $\rightarrow$ switched to `frac` for web.
 - `slashed` is not supported $\rightarrow$ switched to `cancel` for web.
 - `\vec` doesn't look great on web $\rightarrow$ switched to bold vectors.

Mathjax-alone was briefly attempted. Was able to achieve chapter-wise numbering by following this answer https://tex.stackexchange.com/a/714216 but changing section $\rightarrow$ chapter.

### TikZ / Feynman diagrams

 - On Mac, had to install Ghostscript and Ghostscript-extras from [MacTeX](https://www.tug.org/mactex/morepackages.html) (thanks to [this](https://tex.stackexchange.com/a/716651/361983) answer).
 - Had to replace all \\\(...\\\) inline equations with \$...\$, otherwise issues with TikZ -> SVG conversions.

### Config

 - Workaround for equation splitting issue from [#159](https://github.com/michal-h21/make4ht/issues/159).
 - Adapted also the config from Michal's [tex4ht-doc website](https://github.com/michal-h21/tex4ht-doc) for a sidebar, collapsing TOC.
   - This also required his `build.mk4` and `filters` files
- Added favicon in the header.
- Custom CSS stylesheet, again based on Michal's.
- Tried doing fancier customization but in the end found it easier to "postprocess" with Python


### Github Action

Using the same workflows as the [tex4ht-doc website](https://github.com/michal-h21/tex4ht-doc) but with some additional libraries in the [docker image](https://github.com/rkansal47/make4ht-action) to compile the PDF and website.

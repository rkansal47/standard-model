# QFT Notes

Converted from latex to html using tex4ht.

## Notes for compiling

### Math

Using mathml + mathjax for the best equation rendering and referencing (mathml needed for custom macros).

Some notes:

 - The `resizegather` package caused rendering issues [https://github.com/michal-h21/make4ht/issues/158](#158).
 - `mathbbm` is not supported.
 - Equation splitting...
 - `nicefrac` is not well-supported and `cfrac` gives an error.


Mathjax-alone was briefly attempted. Was able to achieve chapter-wise number by followed this answer https://tex.stackexchange.com/a/714216 but changing section $\rightarrow$ chapter.

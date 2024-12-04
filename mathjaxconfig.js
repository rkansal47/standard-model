MathJax ={
loader: {load: ['[tex]/tagFormat']},
  section: 1,
  tex: {
    tags: 'ams',
    packages: {'[+]': ['tagFormat', 'sections']},
    tagformat: {
      number: (n) => MathJax.config.section + '.' + n,
      id: (n) => 'eqn-id-' + n
    }
  },
  startup: {
    ready() {
      const Configuration = MathJax._.input.tex.Configuration.Configuration;
      const CommandMap = MathJax._.input.tex.SymbolMap.CommandMap;
      new CommandMap('sections', {
        nextSection: 'NextSection'
      }, {
        NextSection(parser, name) {
          MathJax.config.section++;
          parser.tags.counter = parser.tags.allCounter = 0;
        }
      });
      Configuration.create(
        'sections', {handler: {macro: ['sections']}}
      );
      MathJax.startup.defaultReady();
      MathJax.startup.input[0].preFilters.add(({math}) => {
        if (math.inputData.recompile) MathJax.config.section = math.inputData.recompile.section;
      });
      MathJax.startup.input[0].postFilters.add(({math}) => {
        if (math.inputData.recompile) math.inputData.recompile.section = MathJax.config.section;
      });
   }
  }
}
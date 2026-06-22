// MathJax v3 + pymdownx.arithmatex(generic) 配置
// 作用：把 $...$ / $$...$$（arithmatex 已转成 \(\)\[\]）交给 MathJax 渲染；
//      并在 Material 的 navigation.instant 无刷新跳转后重新排版公式。
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});

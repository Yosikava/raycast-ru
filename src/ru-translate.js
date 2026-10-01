// Runtime Russian translation for Raycast windows.
// Replaces English UI text with Russian using window.__RU_DICT (exact match)
// and window.__RU_PATTERNS (regex templates). Misses are kept in localStorage.
(function () {
  'use strict';
  var DICT = window.__RU_DICT || {};
  var PATTERNS = (window.__RU_PATTERNS || []).map(function (p) {
    return [new RegExp('^' + p[0] + '$'), p[1]];
  });
  var ATTRS = ['placeholder', 'title', 'aria-label', 'data-tooltip', 'alt'];
  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, INPUT: 1, CODE: 1, PRE: 1, NOSCRIPT: 1 };
  var MISS_KEY = 'ru-translate-misses';
  var misses = {};
  try { misses = JSON.parse(localStorage.getItem(MISS_KEY) || '{}'); } catch (e) {}
  var missDirty = false;

  function exact(s) {
    if (Object.prototype.hasOwnProperty.call(DICT, s)) return DICT[s];
    var alt = s.indexOf('...') >= 0 ? s.replace(/\.\.\./g, '\u2026') : s.replace(/\u2026/g, '...');
    if (alt !== s && Object.prototype.hasOwnProperty.call(DICT, alt)) return DICT[alt];
    return null;
  }

  function lookup(s) {
    var r = exact(s);
    if (r !== null) return r;
    if (/:$/.test(s) && (r = exact(s.slice(0, -1))) !== null) return r + ':';
    for (var i = 0; i < PATTERNS.length; i++) {
      var m = s.match(PATTERNS[i][0]);
      if (m) return PATTERNS[i][1].replace(/\$(\d)/g, function (_, n) { return m[n]; });
    }
    return null;
  }

  function translate(text) {
    var t = text.trim();
    if (!t || !/[A-Za-z]{2}/.test(t)) return null;
    var r = lookup(t);
    if (r === null) {
      if (t.length < 200 && !misses[t]) { misses[t] = 1; missDirty = true; }
      return null;
    }
    return r === t ? null : text.replace(t, r);
  }

  function skipped(el) {
    for (; el; el = el.parentElement) {
      if (SKIP[el.tagName] || el.isContentEditable || el.hasAttribute('data-ru-skip')) return true;
    }
    return false;
  }

  function doText(node) {
    if (skipped(node.parentElement)) return;
    var r = translate(node.nodeValue);
    if (r !== null) node.nodeValue = r;
  }

  function doAttrs(el) {
    for (var i = 0; i < ATTRS.length; i++) {
      var v = el.getAttribute(ATTRS[i]);
      if (v) {
        var r = translate(v);
        if (r !== null) el.setAttribute(ATTRS[i], r);
      }
    }
  }

  function walk(root) {
    if (root.nodeType === 3) return doText(root);
    if (root.nodeType !== 1 || SKIP[root.tagName]) return;
    doAttrs(root);
    var w = document.createTreeWalker(root, 5 /* ELEMENT | TEXT */);
    var n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) doText(n);
      else doAttrs(n);
    }
  }

  var mo = new MutationObserver(function (list) {
    for (var i = 0; i < list.length; i++) {
      var m = list[i];
      if (m.type === 'characterData') doText(m.target);
      else if (m.type === 'attributes') doAttrs(m.target);
      else for (var j = 0; j < m.addedNodes.length; j++) walk(m.addedNodes[j]);
    }
  });

  function start() {
    walk(document.documentElement);
    mo.observe(document.documentElement, {
      childList: true, subtree: true, characterData: true,
      attributes: true, attributeFilter: ATTRS
    });
    if (document.title) {
      var r = translate(document.title);
      if (r !== null) document.title = r;
    }
  }

  setInterval(function () {
    if (!missDirty) return;
    missDirty = false;
    try { localStorage.setItem(MISS_KEY, JSON.stringify(misses)); } catch (e) {}
  }, 5000);

  window.__ruMisses = function () { return Object.keys(misses); };
  if (document.documentElement) start();
  else document.addEventListener('DOMContentLoaded', start);
})();

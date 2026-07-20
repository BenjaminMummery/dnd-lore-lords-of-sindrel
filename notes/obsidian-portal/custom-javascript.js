// Obsidian Portal campaign custom JS - VS Code-style heading folds + footnotes.
// Paste into Settings -> Advanced -> Custom JavaScript (Public).
//
// Footnotes (end of page, never folded):
//   Preferred - HTML comments (Textile inside is parsed normally):
//     <!-- op-footnotes -->
//     h4. Footnotes
//     p(#fn1). [1] Clarification here.
//     <!-- /op-footnotes -->
//   Or Textile div (not a raw HTML <div> - Textile inside raw HTML is not parsed):
//     div(op-footnotes).
//
//     h4. Footnotes
//     p(#fn1). [1] Clarification here.
//   Raw HTML div only if contents are HTML too:
//     <div class="op-footnotes"><h4>Footnotes</h4><p id="fn1">...</p></div>

(function () {
  var FOOTNOTES = ".op-footnotes, [data-op-footnotes]";
  var FOOTNOTES_START = /^\s*op-footnotes\s*$/i;
  var FOOTNOTES_END = /^\s*\/op-footnotes\s*$/i;

  var SKIP =
    "summary, details.op-heading-fold, .op_accordion, .ui-accordion, " +
    ".wiki-edit, #gm-only, .ddb-section, .ddb-header, .stat-block, .ddb-companion-blocks, " +
    ".post-header-container, .wiki-page-name, .character-name, .item-name, " +
    FOOTNOTES;

  var ROOT_SELECTORS = [
    ".wiki-page-content",
    ".adventure-log-show .post-main",
    ".post-section.post-main",
    ".main-content .content",
    ".op-character-prose",
    ".ddb-character-prose",
  ];

  function injectStyles() {
    if (document.getElementById("op-heading-fold-styles")) {
      return;
    }
    var style = document.createElement("style");
    style.id = "op-heading-fold-styles";
    style.textContent =
      ".op-heading-fold { margin: 0 0 0.5rem; }" +
      ".op-fold-summary { cursor: pointer; list-style: none; display: flex; align-items: baseline; gap: 0.35rem; width: 100%; }" +
      ".op-fold-summary::-webkit-details-marker { display: none; }" +
      ".op-fold-summary::before { content: '>'; color: #64748b; font-size: 0.75rem; flex-shrink: 0; }" +
      ".op-heading-fold[open] > .op-fold-summary::before { content: 'v'; }" +
      ".op-fold-summary h1, .op-fold-summary h2, .op-fold-summary h3, " +
      ".op-fold-summary h4, .op-fold-summary h5, .op-fold-summary h6 { margin: 0; display: inline; }" +
      ".op-heading-fold-h2 > .op-fold-summary h2 { display: block; flex: 1; min-width: 0; color: #4b0c0f; font-weight: bold; }" +
      ".op-fold-body { padding: 0.35rem 0 0.5rem; }" +
      ".op-fold-body .op-inline-link-heading { display: inline; font-size: inherit; font-weight: inherit; " +
      "letter-spacing: normal; border: none; margin: 0; padding: 0; }" +
      ".op-fold-body .op-inline-link-heading a { font-weight: inherit; }" +
      ".op-footnotes { margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid #6d6862; " +
      "font-size: 0.92em; color: #475569; clear: both; }" +
      ".op-footnotes > :first-child { margin-top: 0; }" +
      ".op-footnotes h1, .op-footnotes h2, .op-footnotes h3, .op-footnotes h4, " +
      ".op-footnotes h5, .op-footnotes h6 { font-size: 1em; margin: 0 0 0.45rem; color: inherit; }" +
      ".op-footnotes p, .op-footnotes li { line-height: 1.45; }" +
      ".op-footnotes .footnote-backref { font-size: 0.85em; margin-left: 0.25rem; }";
    document.head.appendChild(style);
  }

  function isFootnotesBlock(node) {
    return !!(node && node.nodeType === 1 && node.matches && node.matches(FOOTNOTES));
  }

  function promoteCommentFootnotes(root) {
    if (!root || !root.childNodes) {
      return;
    }
    var child = root.firstChild;
    while (child) {
      var next = child.nextSibling;
      if (child.nodeType === 8 && FOOTNOTES_START.test(child.nodeValue || "")) {
        var wrap = document.createElement("div");
        wrap.className = "op-footnotes";
        wrap.setAttribute("data-op-footnotes", "");
        var sibling = next;
        while (sibling) {
          var after = sibling.nextSibling;
          if (sibling.nodeType === 8 && FOOTNOTES_END.test(sibling.nodeValue || "")) {
            root.removeChild(sibling);
            break;
          }
          wrap.appendChild(sibling);
          sibling = after;
        }
        root.removeChild(child);
        root.appendChild(wrap);
      }
      child = next;
    }
  }

  function relocateFootnotes(root) {
    if (!root) {
      return;
    }
    Array.prototype.slice.call(root.querySelectorAll(FOOTNOTES)).forEach(function (block) {
      if (block.parentNode !== root) {
        root.appendChild(block);
      }
    });
  }

  function extractFootnotesFromFolds(root) {
    if (!root) {
      return;
    }
    Array.prototype.slice.call(root.querySelectorAll(FOOTNOTES)).forEach(function (block) {
      if (block.closest("details.op-heading-fold")) {
        root.appendChild(block);
      }
    });
  }

  function prepareFootnotes(root) {
    promoteCommentFootnotes(root);
    relocateFootnotes(root);
  }

  function foldHeadingKey(heading) {
    var level = headingLevel(heading);
    if (!level) {
      return "";
    }
    return level + "|" + (heading.textContent || "").replace(/\s+/g, " ").trim();
  }

  function captureFoldStates(root) {
    var states = {};
    Array.prototype.slice.call(root.querySelectorAll("details.op-heading-fold")).forEach(function (details) {
      var heading = details.querySelector(".op-fold-summary h1, h2, h3, h4, h5, h6");
      if (!heading) {
        return;
      }
      var key = foldHeadingKey(heading);
      if (key) {
        states[key] = details.hasAttribute("open");
      }
    });
    return states;
  }

  function restoreFoldStates(root, states) {
    if (!states) {
      return;
    }
    Array.prototype.slice.call(root.querySelectorAll("details.op-heading-fold")).forEach(function (details) {
      var heading = details.querySelector(".op-fold-summary h1, h2, h3, h4, h5, h6");
      if (!heading) {
        return;
      }
      var key = foldHeadingKey(heading);
      if (!key || !Object.prototype.hasOwnProperty.call(states, key)) {
        return;
      }
      if (states[key]) {
        details.setAttribute("open", "open");
      } else {
        details.removeAttribute("open");
      }
    });
  }

  function peekSectionHasContent(heading, level) {
    var sibling = heading.nextSibling;
    while (sibling) {
      if (sibling.nodeType === 1) {
        if (isSectionBoundary(sibling, level)) {
          break;
        }
        if (isMidSentenceLinkHeading(sibling)) {
          sibling = sibling.nextSibling;
          continue;
        }
        if ((sibling.textContent || "").replace(/\s+/g, " ").trim()) {
          return true;
        }
        if (sibling.querySelector && sibling.querySelector("img, table, details, ul, ol, blockquote, pre, iframe, svg")) {
          return true;
        }
      } else if (sibling.nodeType === 3 && /\S/.test(sibling.textContent || "")) {
        return true;
      }
      sibling = sibling.nextSibling;
    }
    return false;
  }

  function hasUnfoldedHeadings(root) {
    return Array.prototype.some.call(root.querySelectorAll("h1, h2, h3, h4, h5, h6"), function (heading) {
      if (shouldSkip(heading) || heading.closest("details.op-heading-fold")) {
        return false;
      }
      var level = headingLevel(heading);
      return !!(level && peekSectionHasContent(heading, level));
    });
  }

  function hasUnpromotedFootnotes(root) {
    var child = root.firstChild;
    while (child) {
      if (child.nodeType === 8 && FOOTNOTES_START.test(child.nodeValue || "")) {
        return true;
      }
      child = child.nextSibling;
    }
    return false;
  }

  function needsRefold(root) {
    return hasUnfoldedHeadings(root) || hasUnpromotedFootnotes(root);
  }

  function headingLevel(node) {
    var m = /^H([1-6])$/i.exec(node.tagName || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function shouldSkip(node) {
    if (node.closest("summary")) {
      return true;
    }
    if (node.closest(FOOTNOTES)) {
      return true;
    }
    if (node.closest(".op-character-prose, .ddb-character-prose")) {
      return false;
    }
    return !!node.closest(SKIP);
  }

  function foldLevelFromElement(node) {
    if (!node || !node.classList) {
      return 0;
    }
    for (var lvl = 1; lvl <= 6; lvl++) {
      if (node.classList.contains("op-heading-fold-h" + lvl)) {
        return lvl;
      }
    }
    return 0;
  }

  function foldBodyHasContent(body) {
    if (!body || !body.childNodes.length) {
      return false;
    }
    if ((body.textContent || "").replace(/\s+/g, " ").trim()) {
      return true;
    }
    return !!body.querySelector("img, table, details, ul, ol, blockquote, pre, iframe, svg");
  }

  function unwrapHeadingFolds(root) {
    var folds = Array.prototype.slice.call(root.querySelectorAll("details.op-heading-fold"));
    folds.reverse().forEach(function (details) {
      var summary = details.querySelector(".op-fold-summary");
      var body = details.querySelector(".op-fold-body");
      var heading = summary && summary.querySelector("h1, h2, h3, h4, h5, h6");
      var parent = details.parentNode;
      if (!summary || !body || !heading || !parent) {
        return;
      }
      parent.insertBefore(heading, details);
      while (body.firstChild) {
        parent.insertBefore(body.firstChild, details);
      }
      parent.removeChild(details);
    });
  }

  function isLinkOnlyHeading(heading) {
    if (!heading || !heading.getElementsByTagName) {
      return false;
    }
    var links = heading.getElementsByTagName("a");
    if (links.length !== 1 || heading.children.length !== 1) {
      return false;
    }
    var headingText = (heading.textContent || "").replace(/\s+/g, " ").trim();
    var linkText = (links[0].textContent || "").replace(/\s+/g, " ").trim();
    return headingText === linkText;
  }

  function nearestContentSibling(node, direction) {
    var sibling = node;
    while (sibling) {
      sibling = direction === "prev" ? sibling.previousSibling : sibling.nextSibling;
      if (!sibling) {
        return null;
      }
      if (sibling.nodeType === 3) {
        if (/\S/.test(sibling.textContent || "")) {
          return sibling;
        }
        continue;
      }
      if (sibling.nodeType === 1) {
        return sibling;
      }
    }
    return null;
  }

  // OP sometimes promotes an inline wiki link to h4 mid-sentence; not a real section.
  function isMidSentenceLinkHeading(heading) {
    if (!isLinkOnlyHeading(heading)) {
      return false;
    }
    var prev = nearestContentSibling(heading, "prev");
    if (prev && prev.nodeType === 3) {
      return true;
    }
    var next = nearestContentSibling(heading, "next");
    if (next && next.nodeType === 3) {
      var text = (next.textContent || "").trim();
      if (/^[.,;:!?-]+$/.test(text)) {
        return true;
      }
    }
    return false;
  }

  function collectSectionBody(heading, level, body) {
    var sibling = heading.nextSibling;
    while (sibling) {
      if (sibling.nodeType === 1) {
        if (isSectionBoundary(sibling, level)) {
          break;
        }
      } else if (sibling.nodeType === 3) {
        if (!/\S/.test(sibling.textContent || "")) {
          sibling = sibling.nextSibling;
          continue;
        }
      } else {
        sibling = sibling.nextSibling;
        continue;
      }
      var move = sibling;
      sibling = sibling.nextSibling;
      if (move.nodeType === 1 && isMidSentenceLinkHeading(move)) {
        move.classList.add("op-inline-link-heading");
      }
      body.appendChild(move);
    }
  }

  function isSectionBoundary(sibling, level) {
    if (!sibling) {
      return false;
    }
    if (isFootnotesBlock(sibling)) {
      return true;
    }
    if (sibling.matches("h1, h2, h3, h4, h5, h6")) {
      if (isMidSentenceLinkHeading(sibling)) {
        return false;
      }
      var nextLevel = headingLevel(sibling);
      return !!(nextLevel && nextLevel <= level);
    }
    if (sibling.classList && sibling.classList.contains("op-heading-fold")) {
      var foldLevel = foldLevelFromElement(sibling);
      return !!(foldLevel && foldLevel <= level);
    }
    return false;
  }

  function foldHeadings(root, options) {
    if (!root) {
      return;
    }
    options = options || {};
    var savedStates = null;
    if (options.force) {
      savedStates = captureFoldStates(root);
      root.removeAttribute("data-op-fold-applied");
      unwrapHeadingFolds(root);
    }
    if (root.getAttribute("data-op-fold-applied")) {
      return;
    }
    prepareFootnotes(root);
    var defaultOpenLevel = options.defaultOpenLevel != null ? options.defaultOpenLevel : 6;

    var headings = Array.prototype.slice
      .call(root.querySelectorAll("h1, h2, h3, h4, h5, h6"))
      .filter(function (h) {
        return !shouldSkip(h);
      });

    headings.reverse().forEach(function (heading) {
      if (heading.closest("details.op-heading-fold")) {
        return;
      }
      var level = headingLevel(heading);
      if (!level) {
        return;
      }

      var body = document.createElement("div");
      body.className = "op-fold-body";
      collectSectionBody(heading, level, body);

      if (!foldBodyHasContent(body)) {
        return;
      }

      var parent = heading.parentNode;
      var insertBefore = heading.nextSibling;

      var details = document.createElement("details");
      details.className = "op-heading-fold op-heading-fold-h" + level;
      if (level <= defaultOpenLevel) {
        details.setAttribute("open", "open");
      }

      var summary = document.createElement("summary");
      summary.className = "op-fold-summary";
      details.appendChild(summary);
      details.appendChild(body);
      parent.insertBefore(details, insertBefore);
      summary.appendChild(heading);
    });

    extractFootnotesFromFolds(root);
    relocateFootnotes(root);
    restoreFoldStates(root, savedStates);
    root.setAttribute("data-op-fold-applied", "1");
  }

  function isNestedContentRoot(root) {
    var parent = root.parentElement;
    while (parent) {
      for (var i = 0; i < ROOT_SELECTORS.length; i++) {
        try {
          if (parent.matches(ROOT_SELECTORS[i])) {
            return true;
          }
        } catch (e) {
          /* invalid selector in older browsers */
        }
      }
      parent = parent.parentElement;
    }
    return false;
  }

  function contentRoots() {
    var roots = [];
    ROOT_SELECTORS.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (root) {
        if (selector === ".post-section.post-main" && root.querySelector(".wiki-page-content")) {
          return;
        }
        if (isNestedContentRoot(root)) {
          return;
        }
        if (roots.indexOf(root) === -1) {
          roots.push(root);
        }
      });
    });
    return roots;
  }

  function run(options) {
    injectStyles();
    var opts = options || { defaultOpenLevel: 6 };
    contentRoots().forEach(function (root) {
      foldHeadings(root, opts);
      if (needsRefold(root)) {
        foldHeadings(root, { force: true, defaultOpenLevel: opts.defaultOpenLevel });
      }
    });
  }

  var scheduleTimer = null;
  function scheduleRun() {
    if (scheduleTimer) {
      clearTimeout(scheduleTimer);
    }
    scheduleTimer = setTimeout(function () {
      scheduleTimer = null;
      run();
      [100, 500].forEach(function (delay) {
        setTimeout(function () {
          contentRoots().forEach(function (root) {
            if (needsRefold(root)) {
              foldHeadings(root, { force: true, defaultOpenLevel: 6 });
            }
          });
        }, delay);
      });
    }, 50);
  }

  window.opFoldHeadings = foldHeadings;

  if (window.jQuery) {
    jQuery(document).on("opJsInitializedEvent", scheduleRun);
    jQuery(document).on("ajaxComplete page:load", scheduleRun);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRun);
  } else {
    scheduleRun();
  }
})();

#!/usr/bin/env python3
"""Assemble the draft site: shared head, nav, footer + per-page bodies in pages/."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")
PREFIX = os.environ.get("ASSET_PREFIX", "../")   # '../' while the draft sits in draft/, '' once promoted
NOINDEX = os.environ.get("NOINDEX", "1") == "1"
LIVE = os.environ.get("LIVE", "0") == "1"          # LIVE=1: write to the site root with clean URLs
OUT = os.path.dirname(ROOT) if LIVE else ROOT
LIVE_PAGES = ["index.html", "scale-ready-os.html", "case-studies.html", "case-study-waca.html", "case-study-swoop-baby.html"]
CLEAN = {"index.html": "/", "Privacy.html": "/privacy", "Terms.html": "/terms", "AIDataHandling.html": "/ai-data-handling"}
def clean_links(html):
    import re
    def fix(m):
        href = m.group(1)
        if href.startswith(("http", "mailto", "#")): return m.group(0)
        path, _, frag = href.partition("#")
        path = path.replace("../", "").replace("{PREFIX}", "")
        if path.startswith("assets/"): return 'href="/' + path + '"'
        if path in CLEAN: path = CLEAN[path]
        elif path.endswith(".html"): path = "/" + path[:-5]
        return 'href="' + path + ("#" + frag if frag else "") + '"'
    html = re.sub(r'href="([^"]*)"', fix, html)
    html = html.replace('src="../assets/', 'src="/assets/').replace('src="site.js', 'src="/site.js').replace('href="/site.css', 'href="/site.css')
    return html
SITE = "https://romymofficial.com/"
import hashlib
ASSET_V = hashlib.md5(open(os.path.join(ROOT,"site.css"),"rb").read()+open(os.path.join(ROOT,"site.js"),"rb").read()).hexdigest()[:8]

DISCOVERY = "https://tidycal.com/3zkp0x3/30-minute-discovery"
STRATEGY = "https://tidycal.com/3zkp0x3/strategy-call-30-min"
LOGIN = "https://login.romymofficial.com/"

PAGE_META = {
    "index.html": ("Romy Mueller | Business Strategist & Operations Partner",
                   "Business strategist and operations partner for 6- and 7-figure coaching businesses. I overhaul operations, streamline tech and build the systems for growth."),
    "private-work.html": ("Private Strategy & Implementation | Romy Mueller",
                          "For established coaching and education businesses that want experienced strategic input and someone who can do the work."),
    "strategy-call.html": ("Strategy Call | Romy Mueller",
                           "Got a business decision you'd like another perspective on? A focused strategy session with my recommendation and practical next steps."),
    "scale-ready-os.html": ("Scale Ready OS | Romy Mueller",
                            "A 12-week group programme for coaches and consultants who want to build a better way to run their business. Next intake 1 December 2026."),
    "case-studies.html": ("Case Studies | Romy Mueller",
                          "Selected client work: an online education business and a baby sleep consultancy."),
    "case-study-waca.html": ("Case study: Socially Sands / WACA | Romy Mueller",
                             "Rebuilding the systems behind a growing coaching business: platform migrations, automated recurring work, trustworthy tracking and a better checkout."),
    "case-study-swoop-baby.html": ("Case study: Swoop Baby | Romy Mueller",
                                   "Building the systems to support a growing service business: a rebuilt client journey, client tracking in one place and automated onboarding and follow-ups."),
}

def head(fn):
    title, desc = PAGE_META[fn]
    canon = SITE if fn == "index.html" else SITE + fn.replace(".html", "")
    robots = '<meta name="robots" content="noindex">\n' if NOINDEX else ""
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="{PREFIX}assets/favicon.png">
<link rel="apple-touch-icon" href="{PREFIX}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,500;1,400&family=Raleway:wght@600&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{"/" if LIVE else ""}site.css?v={ASSET_V}">
</head>
<body>
'''

def nav(fn):
    def a(href, label):
        cur = ' aria-current="page"' if href == fn else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f'''
<header class="nav" id="top">
  <div class="wrap">
    <a class="logo" href="index.html">Romy M<span>.</span></a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Open menu"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="navLinks">
      <li><a href="index.html">Home</a></li>
      <li><a href="index.html#ways">Work with me</a></li>
      <li class="has-sub"><a href="case-studies.html"{(' aria-current="page"' if fn.startswith('case-stud') else '')}>Case Studies</a>
        <ul class="sub"><li><a href="case-study-waca.html">Socially Sands / WACA</a></li><li><a href="case-study-swoop-baby.html">Swoop Baby</a></li></ul>
      </li>
      {a("scale-ready-os.html", "Scale Ready OS")}
      <li><a href="index.html#about">About</a></li>
      <li><a class="btn btn-primary" href="{DISCOVERY}" target="_blank" rel="noopener">Book a discovery call</a></li>
    </ul>
  </div>
</header>
'''

FOOTER = f'''
<footer class="footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="index.html">Romy M<span>.</span></a>
        <p class="foot-tag"><span class="nw">Business Strategist &amp;</span> <span class="nw">Operations Partner</span></p>
        <div class="footer-social">
          <a href="https://www.instagram.com/romym_official/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.9 5.9 0 0 0-2.13 1.38A5.9 5.9 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.79.72 1.46 1.38 2.13a5.9 5.9 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.9 5.9 0 0 0 2.13-1.38 5.9 5.9 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0 0-1.38-2.13A5.9 5.9 0 0 0 19.86.63C19.1.33 18.22.13 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 12 18.16 6.16 6.16 0 0 0 12 5.84zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg></a>
          <a href="https://www.linkedin.com/in/romymueller/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a>
          <a href="https://www.tiktok.com/@romymofficial" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a>
        </div>
      </div>
      <nav class="foot-links" aria-label="Footer">
        <a class="foot-link" href="index.html#about">About</a>
        <a class="foot-link" href="index.html#ways">Work with me</a>
        <a class="foot-link" href="case-studies.html">Case Studies</a>
        <a class="foot-link" href="scale-ready-os.html">Scale Ready OS</a>
        <a class="foot-link" href="{LOGIN}" target="_blank" rel="noopener">Log in <span aria-hidden="true">&rarr;</span></a>
        <a class="foot-link" href="mailto:hello@romymofficial.com">Contact</a>
      </nav>
    </div>
    <div class="foot-bottom">
      <span>© 2026 RomyM Official</span>
      <nav aria-label="Policies"><a href="{PREFIX}Privacy.html">Privacy Policy</a><a href="{PREFIX}Terms.html">Terms</a><a href="{PREFIX}AIDataHandling.html">AI &amp; Data Handling</a></nav>
    </div>
  </div>
</footer>
<script src="site.js?v={ASSET_V}"></script>
</body>
</html>
'''

def build():
    for fn in PAGE_META:
        if LIVE and fn not in LIVE_PAGES: continue
        src = os.path.join(PAGES, fn)
        body = open(src).read()
        body = body.replace("{{DISCOVERY}}", DISCOVERY).replace("{{STRATEGY}}", STRATEGY).replace("{{PREFIX}}", PREFIX)
        out = head(fn) + nav(fn) + '<main>' + body + '</main>' + FOOTER
        if LIVE: out = clean_links(out)
        open(os.path.join(OUT, fn), "w").write(out)
        print("built", os.path.join(os.path.basename(OUT), fn))
    if LIVE:
        import shutil
        shutil.copy(os.path.join(ROOT, "site.css"), os.path.join(OUT, "site.css"))
        shutil.copy(os.path.join(ROOT, "site.js"), os.path.join(OUT, "site.js"))

if __name__ == "__main__":
    build()

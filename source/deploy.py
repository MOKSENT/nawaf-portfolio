#!/usr/bin/env python3
"""Wrap the token-resolved builds into the two standalone files the site serves.

    build/artifact-ar.build.html  ->  ../index.html      (Arabic, site root)
    build/artifact-en.build.html  ->  ../en/index.html   (English)

Run build_and_inject.py first; see README.md for the full order.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)          # repo root, where index.html lives
AR_ART = "https://claude.ai/code/artifact/51297c92-5e4d-4350-adf1-a5a5d11a2e20"
EN_ART = "https://claude.ai/code/artifact/30946092-ea26-49a1-8604-75b38b28c00d"


def build(src, prefix_file, out, rewrites):
    html = open(os.path.join(HERE, src), encoding="utf-8").read()
    prefix = open(os.path.join(HERE, prefix_file), encoding="utf-8").read()
    for a, b in rewrites:
        html = html.replace(a, b)
    lines = html.split("\n")
    # the page markup starts at the first <div class="page-..."> line;
    # everything above it is <title> + <style> and belongs in <head>
    i = next(k for k, l in enumerate(lines) if l.lstrip().startswith('<div class="page'))
    doc = (prefix + "\n".join(lines[:i]) + "\n</head>\n<body>\n"
           + "\n".join(lines[i:]) + "\n</body>\n</html>\n")
    path = os.path.join(REPO, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(doc)
    print(out, len(doc), "chars")


build("build/artifact-ar.build.html", "prefix_ar.txt", "index.html", [(EN_ART, "/en/")])
build("build/artifact-en.build.html", "prefix_en.txt", "en/index.html", [(AR_ART, "/")])

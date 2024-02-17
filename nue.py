#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path
from datetime import datetime

def f_meta(post_path):
    meta = {}
    with open(os.path.join(post_path, "raw.md")) as f:
        for line in f:
            if line.strip() == "-->":
                break
            parts = line.strip().split(":", 1)
            if len(parts) == 2:
                meta[parts[0].strip()] = parts[1].strip()
    return meta

def render(content):
    pandoc_args = [
        "pandoc",
        "--from=markdown-smart-fancy_lists+pipe_tables+all_symbols_escapable+raw_html+inline_notes+fenced_divs",
        "--to=html",
    ]
    pandoc_proc = subprocess.Popen(pandoc_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    html_output, _ = pandoc_proc.communicate(input=content)
    return html_output

def t_body(title, content):
    return f"""<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link rel='shortcut icon' href='/static/favicon.png' type='image/x-icon'>
    <link href='/static/style.css' rel='stylesheet' type='text/css'>
    <title>{title}</title>
  </head>
  <body>
    <nav class='feed'>
      <div>
        <a href='/' class='bold'>home</a>
        <a href='/main'>main</a>
        <a href='/side'>side</a>
        <a href='/archive' class='bold'>archive</a>
        <a href='/'>map</a>
        <a href='https://enceris.fandom.com/'>wiki</a>
      </div>
      <div>
        <a href='#' class='toggle'>dark mode</a>
      </div>
    </nav>
    <span style='white-space: nowrap;'>PLACEHOLDER</span>
    {content}
    <script type='module' src='/static/script.js'></script>
  </body>
</html>"""

def t_tags(tags):
    out = ""
    for tag in tags.split():
        out += f"#<a href='/main/?query=%23{tag}' class='bold'>{tag}</a> "
    return out.rstrip()

def t_date(timestamp):
    date_str = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
    return f"<time datetime='{date_str}'>{date_str}</time>"

def t_card(post_name, meta, root_dir, title="chapter"):
    chapter = meta.get("chapter", "")
    if not chapter:
        chapter = meta.get("volume", "")
    name = meta.get("name", "")
    return f"""<section>
        <span class='chapter'>{title} {chapter}:</span>
        <a href='/{root_dir}/{post_name}' class='bold'>{name}</a>
        <!--<div>{meta.get('peek', '')}</div>
        <span>{t_tags(meta.get('tags', ''))}</span>-->
      </section>"""

def t_post(post_id, meta, root_dir):
    name = meta.get("name", "")
    chapter = meta.get("chapter", "")
    peek = meta.get("peek", "")
    raw_content = open(os.path.join(root_dir, post_id, "raw.md")).read()
    formatted_content = render(raw_content)
    date = t_date(meta.get("date", ""))
    tags = t_tags(meta.get("tags", ""))

    body_content = f"""
        <main>
            <article>
                <h1>{name}</h1>
                <h4>KAKUTAI</h4>
                <h4>{peek}</h4>
                <hr>
                {formatted_content}
                <span class='meta'>{date} {tags}</span>
            </article>
        </main>
    """

    title = f"Chapter{chapter}:{name}"
    return t_body(title, body_content)

def build2(root_dir):
    volumes = {}
    for root, _, _ in os.walk(root_dir):
        depth = root.count(os.path.sep)
        if depth == 1:  # Volume level
            volume = os.path.basename(root)
            volumes[volume] = {"chapters": [], "name": f_meta(root).get("name", ""), "volume": f_meta(root).get("volume", "")}
        elif depth == 2:  # Chapter level
            volume = os.path.basename(os.path.dirname(root))
            chapter = os.path.basename(root)
            volumes[volume]["chapters"].append((chapter, f_meta(root).get("name", "")))

    for volume, data in volumes.items():
        volume_index = []
        for entry in data["chapters"]:
            chapter, name = entry
            chapter_path = os.path.join(root_dir, volume, chapter)
            print(f"t_post {volume}/{chapter}")
            with open(os.path.join(chapter_path, "index.html"), "w") as f:
                f.write(t_post(f"{volume}/{chapter}", f_meta(chapter_path), root_dir))
            volume_index.append(t_card(f"{volume}/{chapter}", f_meta(chapter_path), root_dir, "Chapter"))
        with open(os.path.join(root_dir, volume, "index.html"), "w") as f:
            f.write(t_body(data["name"], f"<main>{''.join(volume_index)}</main>"))

    with open(os.path.join(root_dir, "index.html"), "w") as f:
        posts = []
        for p, data in volumes.items():
            posts.append(t_card(p, data, root_dir, "volume"))
        f.write(t_body("index - Kakutai", f"<main>{''.join(posts)}</main>"))

def build3(root_dir):
    volumes = {}
    for root, _, _ in os.walk(root_dir):
        depth = root.count(os.path.sep)
        if depth == 1:  # Volume level
            volume = os.path.basename(root)
            volumes[volume] = {"chapters": [], "name": f_meta(root).get("name", ""), "volume": f_meta(root).get("volume", "")}
        elif 1 < depth < 3:  # Subvolume level
            volume = os.path.basename(os.path.dirname(root))
            subvolume = os.path.basename(root)
            volumes[volume]["chapters"].append((subvolume, f_meta(root).get("name", "")))
        elif depth == 3:  # Chapter level
            volume = os.path.basename(os.path.dirname(os.path.dirname(root)))
            subvolume = os.path.basename(os.path.dirname(root))
            chapter = os.path.basename(root)
            volumes[volume]["chapters"].append((subvolume, chapter, f_meta(root).get("name", "")))

    for volume, data in volumes.items():
        volume_index = []
        for entry in data["chapters"]:
            if len(entry) == 2:  # Subvolume
                subvolume, name = entry
                subvolume_path = os.path.join(root_dir, volume, subvolume)
                subvolume_index = []
                for chapter_entry in os.listdir(subvolume_path):
                    if os.path.isdir(os.path.join(subvolume_path, chapter_entry)):
                        chapter, name = chapter_entry, f_meta(os.path.join(subvolume_path, chapter_entry)).get("name", "")
                        print(f"t_post {volume}/{subvolume}/{chapter}")
                        with open(os.path.join(subvolume_path, chapter, "index.html"), "w") as f:
                            f.write(t_post(f"{volume}/{subvolume}/{chapter}", f_meta(os.path.join(subvolume_path, chapter)), root_dir))
                        subvolume_index.append(t_card(f"{volume}/{subvolume}/{chapter}", f_meta(os.path.join(subvolume_path, chapter)), root_dir))
                with open(os.path.join(subvolume_path, "index.html"), "w") as f:
                    f.write(t_body(subvolume, f"<main>{''.join(subvolume_index)}</main>"))
                volume_index.append(t_card(f"{volume}/{subvolume}", f_meta(subvolume_path), root_dir, "Subvolume"))
            elif len(entry) == 3:  # Chapter
                subvolume, chapter, name = entry
                chapter_path = os.path.join(root_dir, volume, subvolume, chapter)
                print(f"t_post {volume}/{subvolume}/{chapter}")
                with open(os.path.join(chapter_path, "index.html"), "w") as f:
                    f.write(t_post(f"{volume}/{subvolume}/{chapter}", f_meta(chapter_path), root_dir))
        with open(os.path.join(root_dir, volume, "index.html"), "w") as f:
            f.write(t_body(data["name"], f"<main>{''.join(volume_index)}</main>"))

    with open(os.path.join(root_dir, "index.html"), "w") as f:
        posts = []
        for p, data in volumes.items():
            posts.append(t_card(p, data, root_dir, "volume"))
        f.write(t_body("index - Kakutai", f"<main>{''.join(posts)}</main>"))

if __name__ == "__main__":
    build3("archive")
    build2("main")
    build2("side")
    with open("index.html", "w") as f:
        f.write(t_body("index", render(open("raw.md").read())))


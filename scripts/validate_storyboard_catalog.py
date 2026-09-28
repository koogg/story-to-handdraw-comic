#!/usr/bin/env python3
"""Read-only checks of synchronized catalogs, previews, and offline galleries."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "assets/handraw-style"
SKILL = LIB / "skills/handdraw-style-prompter"


class LocalLinks(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("src", "href"):
            value = attrs.get(key, "")
            parsed = urlsplit(value)
            if not parsed.path or parsed.scheme or parsed.netloc:
                continue
            path = (self.page.parent / unquote(parsed.path)).resolve()
            assert path.is_relative_to(LIB.resolve()) and path.is_file(), (self.page, value)
            if tag == "img" and key == "src":
                self.images.append(path)


def main():
    layouts = json.loads((SKILL / "references/layouts.json").read_text(encoding="utf-8"))
    ids = [x["id"] for x in layouts]
    assert len(ids) == len(set(ids)), "Duplicate layout IDs"
    catalogs = {
        "comic-storyboard": (ROOT / "references/storyboard-catalog.md").read_text(encoding="utf-8"),
        "social": (ROOT / "references/social-infographic-catalog.md").read_text(encoding="utf-8"),
    }
    for key, content in catalogs.items():
        expected = [x["id"] for x in layouts if (x["category"] == "comic-storyboard") == (key == "comic-storyboard")]
        assert re.findall(r"^### ((?:SC|IG|SB)-\d{3}) · ", content, re.M) == expected, key
    images = set()
    for item in layouts:
        content = catalogs["comic-storyboard" if item["category"] == "comic-storyboard" else "social"]
        assert f"### {item['id']} · {item['name']}" in content, item["id"]
        prompt = (SKILL / "references" / item["prompt_file"]).read_text(encoding="utf-8")
        zh, en = prompt.split("<!-- zh -->", 1)[1].split("<!-- en -->", 1)
        assert zh.strip() and en.strip() and zh.strip() in content, item["id"]
        image = (SKILL / "gallery" / item["image"]).resolve()
        assert image.is_relative_to((LIB / "images/layouts").resolve()) and image.is_file(), image
        assert "../assets/handraw-style/" + image.relative_to(LIB).as_posix() in content, item["id"]
        images.add(image)
    actual = {p.resolve() for folder in ("social-cards", "infographics", "comic-storyboards") for p in (LIB / "images/layouts" / folder).glob("*.webp")}
    assert images == actual, "Missing or obsolete layout previews"
    for name in ("index.html", "layouts.html"):
        page = SKILL / "gallery" / name
        parser = LocalLinks(page)
        parser.feed(page.read_text(encoding="utf-8"))
        if name == "layouts.html":
            gallery_layout_images = {p for p in parser.images if p.suffix.lower() == ".webp"}
            assert gallery_layout_images == images, "Layout gallery coverage mismatch"
        else:
            singles = {p.resolve() for p in (LIB / "images/individual").glob("*/*.webp") if not p.stem.endswith("_grid")}
            assert singles.issubset(parser.images), "Style gallery missing individual previews"
    print(f"PASS: {len(layouts)} layouts, matching prompts, local previews, and both offline galleries.")


if __name__ == "__main__":
    main()

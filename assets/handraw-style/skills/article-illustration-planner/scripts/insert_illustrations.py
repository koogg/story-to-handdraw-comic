#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_illustrations.py - Deterministic Markdown Article Illustration Inserter
Part of the article-illustration-planner Skill.

Inserts images into Markdown articles at designated anchor points cleanly,
preserving original prose, indentation, and structure.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def insert_illustrations(
    article_text: str,
    manifest: list[dict],
) -> str:
    """
    Inserts image embeds into article_text at anchor points.
    
    Manifest schema:
    [
        {
            "index": 1,
            "anchor": "### 1. 概念起源",
            "position": "after", # "after" or "before"
            "image_path": "images/illus_01.webp",
            "caption": "图1：概念起源与核心意象",
            "alt": "插图1: 概念起源" # optional
        }
    ]
    """
    lines = article_text.splitlines(keepends=True)
    
    # Sort manifest by anchor appearance order in text to avoid offset interference
    # We will search lines top-to-bottom.
    
    # Normalize anchors for line-level matching
    for item in manifest:
        anchor = item.get("anchor", "").strip()
        if not anchor:
            continue
        
        position = item.get("position", "after").lower()
        image_path = item.get("image_path", "")
        caption = item.get("caption", "")
        alt = item.get("alt", caption or f"插图{item.get('index', '')}")
        
        # Build insertion block
        insertion_lines = []
        insertion_lines.append(f"\n![{alt}]({image_path})\n")
        if caption:
            insertion_lines.append(f"*▲ {caption}*\n\n")
        else:
            insertion_lines.append("\n")
        insertion_block = "".join(insertion_lines)
        
        # Find matching line
        matched_idx = -1
        for idx, line in enumerate(lines):
            if anchor in line:
                matched_idx = idx
                break
        
        if matched_idx != -1:
            if position == "before":
                lines.insert(matched_idx, insertion_block)
            else:
                # "after": insert after the matched line (or after the paragraph if it's inline text)
                lines.insert(matched_idx + 1, insertion_block)
        else:
            # Fallback: anchor not found verbatim, search fuzzy or append at end
            sys.stderr.write(f"[WARNING] Anchor not found in article: '{anchor}'. Appending illustration.\n")
            lines.append(insertion_block)
            
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Insert illustrations into Markdown article at anchor points.")
    parser.add_argument("--article", "-a", required=True, help="Path to input Markdown article.")
    parser.add_argument("--manifest", "-m", help="Path to JSON manifest of illustrations.")
    parser.add_argument("--manifest-json", help="Direct JSON string of manifest.")
    parser.add_argument("--output", "-o", help="Path to output Markdown file. Defaults to [stem]_illustrated.md")

    args = parser.parse_args()

    article_path = Path(args.article)
    if not article_path.exists():
        sys.stderr.write(f"Error: Article file '{article_path}' does not exist.\n")
        sys.exit(1)

    article_text = article_path.read_text(encoding="utf-8")

    manifest = []
    if args.manifest:
        manifest_file = Path(args.manifest)
        if not manifest_file.exists():
            sys.stderr.write(f"Error: Manifest file '{manifest_file}' does not exist.\n")
            sys.exit(1)
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    elif args.manifest_json:
        manifest = json.loads(args.manifest_json)
    else:
        sys.stderr.write("Error: Either --manifest or --manifest-json must be provided.\n")
        sys.exit(1)

    illustrated_text = insert_illustrations(article_text, manifest)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = article_path.parent / f"{article_path.stem}_illustrated{article_path.suffix}"

    output_path.write_text(illustrated_text, encoding="utf-8")
    print(f"[SUCCESS] Illustrated article written to: {output_path}")


if __name__ == "__main__":
    main()

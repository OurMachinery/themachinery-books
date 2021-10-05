#!/usr/bin/env python3
# clang-format off

import re
import sys
import os
import json
from pathlib import Path


__book_root_path = ""


def find_terms(content, path):
    regex = r"(\{\{\$include(.*)\}\})"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        original_current_content = match.group(1)
        __current_content = match.group(2)
        __current_content = re.sub(r"(:[\d]+)", "", __current_content)
        abs = __current_content.format(**os.environ).strip()
        destination = Path(abs).resolve()
        origin = Path(
            "{first}/{doc}".format(first=__book_root_path, doc=path)).resolve()
        relative_path = os.path.relpath(destination, start=origin)
        original_current_content = original_current_content.replace(
            __current_content, " {rl}".format(rl=relative_path)).replace("$", "#")
        content = content.replace(match.group(1), original_current_content)
    return content


def process_chapter(chapter, path):
    if len(chapter['sub_items']):
        for item in chapter['sub_items']:
            process_chapter(item['Chapter'], item['Chapter']['path'])
    if "__autogen__doc_include" not in chapter:
        chapter["content"] = find_terms(chapter["content"], path)
        chapter["__autogen__doc_include"] = True
    return chapter


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'supports':
            # sys.argv[2] is the renderer name
            sys.exit(0)
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    inp = sys.stdin
    context, book = json.load(inp)
    __book_root_path = context["root"]
    if 'sections' in book:
        for item in book['sections']:
            item['Chapter'] = process_chapter(
                item['Chapter'], item['Chapter']['path'])
    print(json.dumps(book), end='')

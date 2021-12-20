#!/usr/bin/env python3
# clang-format off

import enum
import re
import sys
import os
import json
from pathlib import Path

__config = {}


def correct_env(content):
    regex = r"(env\.([A-Z_0-9]+))"
    subst = "{\\2}"
    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, content, 0, re.MULTILINE)
    if result:
        return result
    return content


def find_terms(content, path):
    regex = r"(\{\{([a-z_]+)\}\})"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        term = match.group(2)
        if term in __config:
            regex = r"(\{\{"+term+"\}\})"
            result = re.sub(regex, __config[term], content, 0, re.MULTILINE)
            if result:
                content = result
    return content


def process_chapter(chapter, path):
    if len(chapter['sub_items']):
        for item in chapter['sub_items']:
            process_chapter(item['Chapter'], item['Chapter']['path'])
    if "__autogen__replacement_env" not in chapter:
        chapter["content"] = find_terms(chapter["content"], path)
        chapter["__autogen__replacement_env"] = True

    return chapter


def load_config():
    f = open('context.json')
    return json.load(f)


if __name__ == '__main__':
    #sys.stdout = open('log.log', 'w')
    if len(sys.argv) > 1:
        if sys.argv[1] == 'supports':
            # sys.argv[2] is the renderer name
            sys.exit(0)
    __config = load_config()
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    inp = sys.stdin
    context, book = json.load(inp)
    if 'sections' in book:
        for item in book['sections']:
            item['Chapter'] = process_chapter(
                item['Chapter'], item['Chapter']['path'])
    print(json.dumps(book), end='')
    # sys.stdout.close()

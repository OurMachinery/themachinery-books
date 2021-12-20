#!/usr/bin/env python3
# clang-format off

import enum
import re
import sys
import os
import json
from pathlib import Path
import subprocess


__book_root_path = ""

__debug = False


def debug_log(msg):
    if __debug:
        print(msg)


def get_tag(content, token):
    regex = None
    regex = r"#"+token+"\((.+)\)"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        return match.group(1)
    return None


def get_tag_name(content, end=False):
    regex = None
    if end:
        regex = r"#code_snippet_end\((.+)\)"
    else:
        regex = r"#code_snippet_begin\((.+)\)"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        return match.group(1)
    return None


def correct_env(content):
    regex = r"(env\.([A-Z_0-9]+))"
    subst = "{\\2}"
    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, content, 0, re.MULTILINE)
    if result:
        return result
    return content


def extract_exclude(content, tag_exclude, current_tag, requested_tag):
    if "#code_snippet_exclude_begin()" in content:
        return True
    if "#code_snippet_exclude_end()" in content:
        return False
    # alternative processing
    if "#code_snippet_exclude_begin(" in content:
        tag = get_tag(content, "code_snippet_exclude_begin")
        if tag == requested_tag:
            return True
    if "#code_snippet_exclude_end(" in content:
        tag = get_tag(content, "code_snippet_exclude_end")
        if tag == requested_tag:
            return False
    return tag_exclude


def process_code_snipet(file, requested_tag, ignore_exclude):
    ignore_exclude = True if ignore_exclude is not None else False
    debug_log("process: {} #{}".format(file, requested_tag))
    fh = open(file, "r")
    lines = fh.readlines()
    # Strips the newline character
    tag = None
    tag_contents = ""
    tag_exclude = False
    for index, line in enumerate(lines):
        tag_exclude = extract_exclude(line, tag_exclude, tag, requested_tag)
        if ignore_exclude and tag_exclude:
            tag_exclude = False
        if "#code_snippet_exclude_end(" in line or "#code_snippet_exclude_begin(" in line:
            continue
        if "#code_snippet_begin(" in line:
            found_tag = get_tag_name(line)
            if found_tag == requested_tag:
                tag = found_tag
                if len(tag_contents) > 0:
                    tag_contents += "//...\n"
                tag_exclude = False
                debug_log("opened: {}".format(tag))
            continue
        if "#code_snippet_end(" in line and not tag_exclude:
            found_tag = get_tag_name(line, True)
            if found_tag == requested_tag:
                debug_log("closed: {}".format(tag))
                tag = None
                continue
            continue

        if tag != None and tag == requested_tag and not tag_exclude:
            tag_contents += line
            debug_log("added data to: {}".format(tag))

    p = subprocess.Popen(
        ["clang-format", "-style=file"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    tag_formatted = p.communicate(input=str.encode(tag_contents))[0]
    return tag_formatted.decode()


def process_insert_all(file):
    fh = open(file, "r")
    lines = fh.readlines()
    # Strips the newline character
    content = ""
    for index, line in enumerate(lines):
        if "#code_snippet_exclude_end(" in line or "#code_snippet_exclude_begin(" in line or "#code_snippet_begin(" in line or "#code_snippet_end(" in line:
            continue
        content += line
    p = subprocess.Popen(
        ["clang-format", "-style=file"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    tag_formatted = p.communicate(input=str.encode(content))[0]
    return tag_formatted.decode()


def find_terms(content, path):
    regex = r"\{\{insert_code\(([\/aA-zZ_.0-9]+),([aA-zZ_0-9]+)\)\}\}|\{\{insert_code\(([\/aA-zZ_.0-9]+),([aA-zZ_0-9]+),([aA-zZ_0-9]+)\)\}\}"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        original_current_content = match.group(0)
        path = match.group(1) if match.group(
            1) is not None else match.group(3)
        __current_content = correct_env(path)
        __current_content = re.sub(r"(:[\d]+)", "", __current_content)
        abs = __current_content.format(**os.environ).strip()
        destination = Path(abs).resolve()
        tag = match.group(2) if match.group(
            2) is not None else match.group(4)
        data = process_code_snipet(destination, tag, match.group(5))
        if len(data) == 0:
            data = "Could not replace {}".format(original_current_content)
        content = content.replace(original_current_content, data)
    regex = r"(\{\{insert_code\((.*)\)\}\})"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        original_current_content = match.group(1)
        __current_content = correct_env(match.group(2))
        __current_content = re.sub(r"(:[\d]+)", "", __current_content)
        abs = __current_content.format(**os.environ).strip()
        destination = Path(abs).resolve()
        data = process_insert_all(destination)
        if len(data) == 0:
            data = "Could not replace {}".format(original_current_content)
        content = content.replace(original_current_content, data)

    return content


def process_dollar_includes(content, path):
    regex = r"(\{\{\$include(.*)\}\})"
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        original_current_content = match.group(1)
        __current_content = match.group(2)
        __current_content = re.sub(r"(:[\d]+)", "", __current_content)
        abs = correct_env(__current_content)
        abs = abs.format(**os.environ).strip()
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
        chapter["content"] = process_dollar_includes(chapter["content"], path)
        chapter["__autogen__doc_include"] = True

    return chapter


if __name__ == '__main__':
    if __debug:
        sys.stdout = open('log.log', 'w')
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
    if not __debug:
        print(json.dumps(book), end='')
    if __debug:
        sys.stdout.close()

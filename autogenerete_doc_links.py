#!/usr/bin/env python3

import re
import sys
import os
import json


def find_term(jsonObject, term):
    for val in jsonObject:
        fn = "{0}()".format(term)
        inl = "{0}.inl".format(term)
        c = "{0}.c".format(term)
        h = "{0}.h".format(term)
        isTerm = val["term"] == term or fn == val["term"] or h == val["term"] or c == val["term"] or inl == val["term"]
        isFile = val["file"] == term
        isPath = val["path"] == term
        if isTerm or isFile or isPath:
            return (val, isTerm, isFile, isPath)
    return None


def find_terms(content, name):
    regex = r"`([aA-zZ\(\)\.]+)`"
    with open("../terms.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    matches = re.finditer(regex, content, re.MULTILINE)
    for match in matches:
        group = match.group(1)
        term = find_term(jsonObject, group)
        if term != None:
            link = "{{docs}}"
            link = "{0}{1}.html#{2}".format(link, term[0]["path"], term[0]["name"])
            if term[3]:
                subst = "[{0}]({1})".format(term[0]["path"], link)
                regex = "`({0})`".format(term[0]["path"])
                content = re.sub(regex, subst, content, 0, re.MULTILINE)
            elif term[2]:
                subst = "[{0}]({1})".format(term[0]["file"], link)
                regex = "`({0})`".format(term[0]["file"])
                content = re.sub(regex, subst, content, 0, re.MULTILINE)
            elif term[1]:
                subst = "[{0}]({1})".format(group, link)
                regex = "`({0})`".format(term[0]["term"])
                content = re.sub(regex, subst, content, 0, re.MULTILINE)
    return content


def process_chapter(chapter, name):
    if len(chapter['sub_items']):
        for item in chapter['sub_items']:
            process_chapter(item['Chapter'], item['Chapter']['name'])
    if "__autogen__doc_links" not in chapter:
        chapter["content"] = find_terms(chapter["content"], name)
        chapter["__autogen__doc_links"] = True
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
    if 'sections' in book:
        for item in book['sections']:
            item['Chapter'] = process_chapter(item['Chapter'], item['Chapter']['name'])
    print(json.dumps(book), end='')

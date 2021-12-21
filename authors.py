#!/usr/bin/env python3
# clang-format off

import sys
import os
import json
from pathlib import Path
from git import Repo
import hashlib

__debug = False


def debug_log(msg):
    if __debug:
        print(msg)


def process_file(content, path):
    if "SUMMARY.md" in path:
        return content
    path = path.replace("index.md", "README.md")
    path = os.path.join("tutorials", "src", path)
    repo = Repo(search_parent_directories=True)
    names = {}
    for commit in repo.iter_commits("main", Path(path).as_posix()):
        if commit.committer.name not in names:
            names[commit.committer.name] = [commit.committer.email, 1]
        else:
            names[commit.committer.name][1] += 1
    authors = "\n### Contributors\n"
    for name, (email, commit) in sorted(names.items(), key=lambda x: x[1], reverse=True):
        authors += "[![{}](https://www.gravatar.com/avatar/{}?s=32) {}](mailto:{})\n".format(
            name, hashlib.md5(email.lower().encode('utf-8')).hexdigest(), name, email)
    return content + authors


def process_chapter(chapter, path):
    if len(chapter['sub_items']):
        for item in chapter['sub_items']:
            process_chapter(item['Chapter'], item['Chapter']['path'])
    if "__autogen__doc_include" not in chapter:
        chapter["content"] = process_file(chapter["content"], path)
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

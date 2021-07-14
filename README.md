# The Machinery book

> **⚠ WARNING: This project is currently a work in progress.**

This repository contains the source of "The Machinery" book and some other books. 

## How to contribute?

If you want to contribute to this project please read the [CONTRIBUTING.md](CONTRIBUTING.md) first!

## Requirements

Building the book requires 
- [mdBook](https://github.com/rust-lang-nursery/mdBook)
- [mdbook-toc](https://github.com/badboy/mdbook-toc)
- [mdbook-tera](https://github.com/avitex/mdbook-tera)

To get them:

```bash
$ cargo install mdbook
$ cargo install mdbook-toc
$ cargo install mdbook-tera
```

Alternatively you can download the latest executables for:

- [mdbook](https://github.com/rust-lang/mdBook/releases/)
- [mdbook-toc](https://github.com/badboy/mdbook-toc/releases)

## Writing

Edit the markdown files with your editor of choice (we like [Typora](https://typora.io/)). If you want to see the changes live, run:

```bash
# For the_machinery_book
$ cd the_machinery_book && mdbook serve

# For the tutorials
$ cd tutorials && mdbook serve
```

If you want to add new pages to the system just add them to `SUMMARY.md`. As soon as they are in there they will be used for the book.

*About Links*

If you want to link anything within the book please make use of `{{base_url}}` this will be replaced
on build with the correct base URL.

## Building

To build the book, type:

```bash
# For the_machinery_book
$ cd the_machinery_book && mdbook build

# For the tutorials
$ cd tutorials && mdbook build
```

The output will appear in the `book` subdirectory. To check it out, open it in your web browser:

*Firefox:*

```bash
$ firefox book/index.html                       # Linux
$ open -a "Firefox" book/index.html             # OS X
$ Start-Process "firefox.exe" .\book\index.html # Windows (PowerShell)
$ start firefox.exe .\book\index.html           # Windows (Cmd)
```

*Chrome:*

```bash
$ google-chrome book/index.html                 # Linux
$ open -a "Google Chrome" book/index.html       # OS X
$ Start-Process "chrome.exe" .\book\index.html  # Windows (PowerShell)
$ start chrome.exe .\book\index.html            # Windows (Cmd)
```

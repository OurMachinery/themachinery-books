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
- [mdbook-linkcheck](https://github.com/Michael-F-Bryan/mdbook-linkcheck)
- Python 3.9+ (for auto include generation) (needs to be acciceslbe from CMD)

To get them:

```bash
$ cargo install mdbook
$ cargo install mdbook-toc
$ cargo install mdbook-tera
$ cargo install mdbook-linkcheck
```

Alternatively you can download the latest executables for:

- [mdbook](https://github.com/rust-lang/mdBook/releases/)
- [mdbook-toc](https://github.com/badboy/mdbook-toc/releases)
- [mdbook-linkcheck](https://github.com/Michael-F-Bryan/mdbook-linkcheck/releases)

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

If you want to link anything within the book please make use of 

- `{{base_url}}` for the base address of your current book
- `{{the_machinery_book}}` to cross link to this book
- `{{tutorials}}` to cross link to this book
- `{{docs}}` to link to the documentation e.g. `{{docs}}plugins/physx/physx_scene.h.html#structtm_physx_scene_api`

They will be replaced on build with the correct URL's. 

Besides the build process will check all links if they are valid. If not you will not be able to build the game.

*Linking to API types*

If you want to link to functions or API's you can just write in your markdown: 
```
`tm_physx_scene_api`
```
On deploy the book will automaically find those terms and replaces them with proper linking.

### When adding source code snippets:

Please when you intend to add source code snippets please push them first (or make a PR) to the https://github.com/OurMachinery/themachinery-book-code-snippets. After that you can make use of the auto include preprocessor:
```
{{$include {TM_BOOK_CODE_SNIPPETS}/gameplay_code/ecs_component_example.c:17:31}}
```

**NOTE**: `TM_BOOK_CODE_SNIPPETS` needs to be a enviroment variable pointing to the `examples` folder of the `themachinery-book-code-snippets` repo.

#### Naming rules:

Please name your source code file after the tutorial or guide you are working on. For more information: https://github.com/OurMachinery/themachinery-book-code-snippets

### Working in dropbox paper

In case you have written your article in [dropbox paper](https://paper.dropbox.com/) you can export your work as following:

1. Open your document
2. Open the **᠁** Symbol (Menu)
3. Search for the "Export" point
4. Export as `.md` file

Open your markdown editor of choice (e.g. [Typora](https://typora.io/)) and check if the formatting is correct. If yes copy and paste the file into the correct location in the book. After this open the `SUMMARY.md` of the corresponding book and add a entry.

To verify everything run: (choose the correct book)

```bash
# For the_machinery_book
$ cd the_machinery_book && mdbook serve

# For the tutorials
$ cd tutorials && mdbook serve
```
_Open the in the browser using http://localhost:3000_.

If everything works and looks like it supposed to you can commit to master and push.

### Working in paper

In case you have written your article in [dropbox paper](https://paper.dropbox.com/) you can export your work as following:

1. Open your document
2. Open the **᠁** Symbol (Menu)
3. Search for the "Export" point
4. Export as `.md` file

Open your markdown editor of choice (e.g. [Typora](https://typora.io/)) and check if the formatting is correct. If yes copy and paste the file into the correct location in the book. After this open the `SUMMARY.md` of the corresponding book and add a entry.

To verify everything run: (choose the correct book)

```bash
# For the_machinery_book
$ cd the_machinery_book && mdbook serve

# For the tutorials
$ cd tutorials && mdbook serve
```

If everything works commit to master and push.

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

## Deploy

Run The workflow under Actions.

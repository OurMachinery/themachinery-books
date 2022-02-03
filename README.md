# The Machinery book

> **⚠ WARNING: This project is currently a work in progress.**

This repository contains the source of "The Machinery" book and some other books. 

## How to contribute?

If you want to contribute to this project please read the [CONTRIBUTING.md](CONTRIBUTING.md) first!

## Requirements and installation

To edit the book you need:

- [tmbook](#)

### Installation via `tmbook`

Download `tmbook` and create a folder open the folder with the terminal and type:

```
tmbook init
```
This will automatically download everything for you.


### Installation via git

Open your terminal and run:
```
git clone https://github.com/OurMachinery/themachinery-books.git
cd themachinery-books
```

Add `tmbook` in the `themachinery-books` folder and now you can use it. 


## Writing

Edit the markdown files with your editor of choice (we like [Typora](https://typora.io/)). 

If you want to see the changes live, run:
```bash
# For the_machinery_book
$ cd the_machinery_book && ../tmbook serve

# For the tutorials
$ cd tutorials && ../tmbook serve
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
On deploy the book will automaically find those terms and replaces them with proper linking. (if the `terms.json` file has been updated)

### When adding source code snippets:

Please when you intend to add source code snippets please push them first (or make a PR) to the https://github.com/OurMachinery/themachinery-book-code-snippets. After that you can make use of the auto include preprocessor:

```
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/ecs_component_example.c,tag_name)}} // will include what ever is in this context
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/ecs_component_example.c)}} // will include the whole file
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/ecs_component_example.c,tag,off)}} // ignores all exclude statements
```

in code they are defined as following:

**begin context and end context:**
```c
// #code_snippet_begin(tm_load_plugin)
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;

    tm_draw2d_api = tm_get_api(reg, tm_draw2d_api);
    tm_ui_api = tm_get_api(reg, tm_ui_api);
    tm_allocator_api = tm_get_api(reg, tm_allocator_api);

    tm_add_or_remove_implementation(reg, load, tm_tab_vt, custom_tab_vt);
}
// #code_snippet_end(tm_load_plugin)
```
**Contextual exclude:**

> *Note*: If the context (tag) `tab__toolbars` shall include all (also whats excluded) one can call: `{{insert_code(env.TM_BOOK_CODE_SNIPPETS/toolbar/toolbar_example.c,tab__toolbars,off)}}`

```c
// #code_snippet_begin(tab__toolbars)
static struct tm_toolbar_i *tab__toolbars(tm_tab_o *tab, tm_temp_allocator_i *ta)
{
    // #code_snippet_exclude_begin(tab__toolbars)
    struct tm_toolbar_i *toolbars = 0;
    tm_carray_temp_push(toolbars,
                        ((tm_toolbar_i){
                            .id = TM_STRHASH_U64(TM_STATIC_HASH("my_tab", 0x833aa53d363283b5ULL)),
                            .ui = toolbar__ui,
                            .draw_mode_mask = TM_TOOLBAR_DRAW_MODE_HORIZONTAL | TM_TOOLBAR_DRAW_MODE_VERTICAL,
                        }),
                        ta);
    return toolbars;
    // #code_snippet_exclude_end(tab__toolbars)
}
// #code_snippet_end(tab__toolbars)
```

> **Note**: You can also have a none contextual exclude: `// #code_snippet_exclude_end()`.

**Enviroment Variables:**

> **NOTE**: `TM_BOOK_CODE_SNIPPETS` needs to be a environment variable pointing to the `examples` folder of the `themachinery-book-code-snippets` repo.

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


## Building

To build the book, type:

```bash
# For the_machinery_book
$ cd the_machinery_book && ../tmbook build

# For the tutorials
$ cd tutorials && ../tmbook build
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

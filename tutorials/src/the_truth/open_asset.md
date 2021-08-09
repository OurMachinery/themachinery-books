# Open a special tab for an Asset



This walkthrough shows you how to enable an asset to open a specific tab. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/the_plugin_system.html). This walkthrough aims to enable you to double-click an asset and open it in a specific tab.



You will learn:

- Create a basic tab
- Open an asset
- How to use a temporary temporray allocator



This walkthrough will refer to the text asset example as the asset we want to extend! If you have not followed it, here is the link: [Custom Asset]({{tutorials}}/the_truth/custom_asset/index.html).

**Table of Content**

* auto-gen TOC;
{:toc}


## New Tab

The first cause of action is to create the Tab we want to open. 

> **Note:** We can use the basic tab Template from the Engine: **File -> New Plugin -> New Tab.** 

In this walkthrough, we aim to have a simple tab that shows the content of our text file.

The Steps of creating a tab are similar to the ones of a standard plugin:

1. We create a new file. For example: `txt_tab.c`
2. We need to include some files for a tab plugin:

```c
static struct tm_api_registry_api *tm_global_api_registry;

static struct tm_ui_api *tm_ui_api;
static struct tm_temp_allocator_api *tm_temp_allocator_api;

extern struct tm_the_truth_api *tm_the_truth_api;
static struct tm_localizer_api *tm_localizer_api;

#include <foundation/allocator.h>
#include <foundation/api_registry.h>
#include <foundation/string.inl>
#include <foundation/temp_allocator.h>
#include <foundation/the_truth.h>

#include <plugins/ui/docking.h>
#include <plugins/ui/ui.h>

#include <the_machinery/the_machinery_tab.h>

#include "txt.h"
```



> **Note:** With extern we can use the truth api from the `txt.c` file so we do not need to get it from the registry!

- The docking header file provides us the default tab type
- The UI header gives us access to the UI API
- The txt header gives us access to our custom types



1. We create a new load function on the bottom of the file:

```c
void load_txt_tab(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;

    tm_ui_api = reg->get(TM_UI_API_NAME);
    tm_temp_allocator_api = reg->get(TM_TEMP_ALLOCATOR_API_NAME);
}
```

In our main file the `txt.c` we need to add this function and call it:

```c
extern void load_txt_tab(struct tm_api_registry_api* reg, bool load);

// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    // more code
    load_txt_tab(reg,load);
}
```

2. Above this function we initialize a object of the type `tm_the_machinery_tab_vt`

```c
static tm_the_machinery_tab_vt *tab_vt = &(tm_the_machinery_tab_vt){
// ...
};

void load_txt_tab(struct tm_api_registry_api *reg, bool load){
    //...
}
```

3. We add to the `txt.h` the name of our Tab as well as its hash

```c
#define TM_TXT_TAB_VT_NAME "tm_txt_tab"
#define TM_TXT_TAB_VT_NAME_HASH TM_STATIC_HASH("tm_txt_tab", 0x2cd261be98a99bc3ULL)
```

4. To this Virtual Table, we add the name and its hash as well as the following functions:

```c
static const char *tab__create_menu_name(void)
{
    return "Text Tab";
}

static const char *tab__title(tm_tab_o *tab, struct tm_ui_o *ui)
{
    return "Text Tab";
}

static tm_the_machinery_tab_vt *tab_vt = &(tm_the_machinery_tab_vt){
    .name = TM_TXT_TAB_VT_NAME,
    .name_hash = TM_TXT_TAB_VT_NAME_HASH,
    .create_menu_name = tab__create_menu_name,
    .create = tab__create,
    .destroy = tab__destroy,
    .title = tab__title,
    .ui = tab__ui,
    .set_root = tab__set_root,
    .root = tab__root,
};
```

5. On top of our file, we define the opaque type: `tm_tab_o` and provide some fields to it:

```c
struct tm_tab_o
{
    tm_tab_i tm_tab_i;
    tm_allocator_i *allocator;

    tm_tt_id_t asset;
    tm_the_truth_o *tt;
};
```



The most important fields here are the **asset** and **tt** filed. They will store the currently used asset and truth. Those fields allow us to access both in various functions.



### Implementing the functions

Now that we have done all the boilerplate code, let us focus on the three functions that count:

- The create function
- The UI Update
- The Set Root function



#### The Create Function

```c
static tm_tab_i *tab__create(tm_tab_create_context_t *context, tm_ui_o *ui)
{
    tm_allocator_i *allocator = context->allocator;
    uint64_t *id = context->id;

    static tm_the_machinery_tab_vt *vt = 0;
    if (!vt)
        vt = tm_global_api_registry->get(TM_TXT_TAB_VT_NAME);

    tm_tab_o *tab = tm_alloc(allocator, sizeof(tm_tab_o));
    *tab = (tm_tab_o){
        .tm_tab_i = {
            .vt = (tm_tab_vt *)vt,
            .inst = (tm_tab_o *)tab,
            .root_id = *id,
        },
        .allocator = allocator,
    };

    *id += 1000000;
    return &tab->tm_tab_i;
}
```

In this function, we store the allocator first. 

> **Tipp:** if you wanted to create a child allocator, you could do this for your Tab. A child allocator may be very useful when doing many allocations: `tm_allocator_api.create_child()`.

As the next step, we initialize the virtual table of or Tab, but only if the static variable was not initialized. 

```c
    static tm_the_machinery_tab_vt *vt = 0;
    if (!vt)
        vt = tm_global_api_registry->get(TM_TXT_TAB_VT_NAME);
```

We need to initialize the tab interface so other engine parts can communicate with a generic interface to the Tab. We store a pointer to our Tab within this interface so other callers of the standard generic interface can access this instance and pass it along to the functions. After this, we allocate the Tab itself.

```c
    tm_tab_o *tab = tm_alloc(allocator, sizeof(tm_tab_o));
    *tab = (tm_tab_o){
        .tm_tab_i = {
            .vt = (tm_tab_vt *)vt,
            .inst = (tm_tab_o *)tab,
            .root_id = *id,
        },
        .allocator = allocator,
    };
```

In the end, we return the pointer to the interface, so the docking system has it

#### The Update Function

```c
static void tab__ui(tm_tab_o *tab, tm_ui_o *ui, const tm_ui_style_t *uistyle_in, tm_rect_t rect)
{
    tm_ui_style_t *uistyle = (tm_ui_style_t[]){ *uistyle_in };
    if (tab->asset.u64) {
        TM_INIT_TEMP_ALLOCATOR(ta);
        tm_tt_buffer_t buffer = tm_the_truth_api->get_buffer(tab->tt, tm_tt_read(tab->tt, tab->asset), TM_TT_PROP__MY_ASSET__DATA);
        char *content = tm_temp_alloc(ta, buffer.size + 1);
        tm_strncpy_safe(content, buffer.data, buffer.size);

        tm_ui_text_t *text = &(tm_ui_text_t){ .text = content, .rect = rect };
        tm_ui_api->wrapped_text(ui, uistyle, text);
        TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
    } else {
        rect.h = 20;
        tm_ui_text_t *text = &(tm_ui_text_t){ .align = TM_UI_ALIGN_CENTER, .text = "Please open a .txt asset.", .rect = rect };
        tm_ui_api->text(ui, uistyle, text);
    }
}
```

At first, we create a copy of the UI Style. With this copy, we can do what we want since the input style is a const pointer. After this, we check if the asset is present. If not, we print a message on the Tab that the user must select a `txt` asset.

```c
static void tab__ui(tm_tab_o *tab, tm_ui_o *ui, const tm_ui_style_t *uistyle_in, tm_rect_t rect)
{  
tm_ui_style_t *uistyle = (tm_ui_style_t[]){ *uistyle_in };
    if (tab->asset.u64) {
        //...
    } else {
        rect.h = 20;
        tm_ui_text_t *text = &(tm_ui_text_t){ .align = TM_UI_ALIGN_CENTER, .text = "Please open a .txt asset.", .rect = rect };
        tm_ui_api->text(ui, uistyle, text);
    }
}
```

We need an allocator to copy the data of the buffer into a proper string. The allocator is needed since we never added a null terminator to the end of the string when we save it into the buffer.

In this case, we need a temporary allocator. Since we do not want to keep the memory forever, we need to initialize a temp allocator with `TM_INIT_TEMP_ALLOCATOR` and provide a name. Do not forget to free the memory at the end. 

```c
static void tab__ui(tm_tab_o *tab, tm_ui_o *ui, const tm_ui_style_t *uistyle_in, tm_rect_t rect)
{
    tm_ui_style_t *uistyle = (tm_ui_style_t[]){ *uistyle_in };
    if (tab->asset.u64) {
        TM_INIT_TEMP_ALLOCATOR(ta);
            //..
        TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
    } else {
        rect.h = 20;
        tm_ui_text_t *text = &(tm_ui_text_t){ .align = TM_UI_ALIGN_CENTER, .text = "Please open a .txt asset.", .rect = rect };
        tm_ui_api->text(ui, uistyle, text);
    }
}
```

> **Note:** If the memory is smaller than 1024 bytes, the memory is allocated to the stack. Moreover, an alternative is the frame allocator in which the memory is freed every frame.

The next step is it to ask the truth for the buffer and allocate the right amount of memory. Since we want to copy the data into a null-terminated string, we should add 1 to the data size.

```c
 tm_tt_buffer_t buffer = tm_the_truth_api->get_buffer(tab->tt, tm_tt_read(tab->tt, tab->asset), TM_TT_PROP__MY_ASSET__DATA);
char *content = tm_temp_alloc(ta, buffer.size + 1);
```

To ensure our string is clean and filled with nulls, we use the inline string file (hence we add the `foundation/string.inl` to our includes). We have the `tm_strncpy_safe` within this header file, which fills up a string with null terminator.

```c
tm_strncpy_safe(content, buffer.data, buffer.size);
```

The last step before we are done is actually to make the text appear on the screen. We make use of the `tm_ui_api.wrapped_text()` since this function will print the string in multiple lines if need be.

```c
tm_ui_text_t *text = &(tm_ui_text_t){ .text = content, .rect = rect };
tm_ui_api->wrapped_text(ui, uistyle, text);
```



#### The set root / root function

The last function which we need is the set root function. This function allows us to set a root object of the Tab from the outside. Its code is quite straightforward:

```c
void tab__set_root(tm_tab_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t root)
{
    inst->asset = root;
    inst->tt = tt;
}

static tm_tab_vt_root_t tab__root(tm_tab_o *tab)
{
    return (tm_tab_vt_root_t){ tab->tt, tab->asset };
}
```



### Let us test the Tab

Let us open the Tab from the **Tabs** menu!



[image]



### Source Code

```c
static struct tm_api_registry_api *tm_global_api_registry;

static struct tm_ui_api *tm_ui_api;
static struct tm_temp_allocator_api *tm_temp_allocator_api;

extern struct tm_the_truth_api *tm_the_truth_api;
static struct tm_localizer_api *tm_localizer_api;

#include <foundation/allocator.h>
#include <foundation/api_registry.h>
#include <foundation/string.inl>
#include <foundation/temp_allocator.h>
#include <foundation/the_truth.h>

#include <plugins/ui/docking.h>
#include <plugins/ui/ui.h>

#include <the_machinery/the_machinery_tab.h>


#include "txt.h"

struct tm_tab_o
{
    tm_tab_i tm_tab_i;
    tm_allocator_i *allocator;

    tm_tt_id_t asset;
    tm_the_truth_o *tt;
};

static void tab__ui(tm_tab_o *tab, tm_ui_o *ui, const tm_ui_style_t *uistyle_in, tm_rect_t rect)
{
    tm_ui_style_t *uistyle = (tm_ui_style_t[]){ *uistyle_in };
    if (tab->asset.u64) {
        TM_INIT_TEMP_ALLOCATOR(ta);
        tm_tt_buffer_t buffer = tm_the_truth_api->get_buffer(tab->tt, tm_tt_read(tab->tt, tab->asset), TM_TT_PROP__MY_ASSET__DATA);
        char *content = tm_temp_alloc(ta, buffer.size + 1);
        tm_strncpy_safe(content, buffer.data, buffer.size);

        tm_ui_text_t *text = &(tm_ui_text_t){ .text = content, .rect = rect };
        tm_ui_api->wrapped_text(ui, uistyle, text);
        TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
    } else {
        rect.h = 20;
        tm_ui_text_t *text = &(tm_ui_text_t){ .align = TM_UI_ALIGN_CENTER, .text = "Please open a .txt asset.", .rect = rect };
        tm_ui_api->text(ui, uistyle, text);
    }
}

static const char *tab__create_menu_name(void)
{
    return "Text Tab";
}

static const char *tab__title(tm_tab_o *tab, struct tm_ui_o *ui)
{
    return "Text Tab";
}

static tm_tab_i *tab__create(tm_tab_create_context_t *context, tm_ui_o *ui)
{
    tm_allocator_i *allocator = context->allocator;
    uint64_t *id = context->id;

    static tm_the_machinery_tab_vt *vt = 0;
    if (!vt)
        vt = tm_global_api_registry->get(TM_TXT_TAB_VT_NAME);

    tm_tab_o *tab = tm_alloc(allocator, sizeof(tm_tab_o));
    *tab = (tm_tab_o){
        .tm_tab_i = {
            .vt = (tm_tab_vt *)vt,
            .inst = (tm_tab_o *)tab,
            .root_id = *id,
        },
        .allocator = allocator,
    };

    *id += 1000000;
    return &tab->tm_tab_i;
}

static void tab__destroy(tm_tab_o *tab)
{
    tm_free(tab->allocator, tab, sizeof(*tab));
}

void tab__set_root(tm_tab_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t root)
{
    inst->asset = root;
    inst->tt = tt;
}

static tm_tab_vt_root_t tab__root(tm_tab_o *tab)
{
    return (tm_tab_vt_root_t){ tab->tt, tab->asset };
}

static tm_the_machinery_tab_vt *tab_vt = &(tm_the_machinery_tab_vt){
    .name = TM_TXT_TAB_VT_NAME,
    .name_hash = TM_TXT_TAB_VT_NAME_HASH,
    .create_menu_name = tab__create_menu_name,
    .create = tab__create,
    .destroy = tab__destroy,
    .title = tab__title,
    .ui = tab__ui,
    .set_root = tab__set_root,
    .root = tab__root,
};

void load_txt_tab(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;

    tm_ui_api = reg->get(TM_UI_API_NAME);
    tm_temp_allocator_api = reg->get(TM_TEMP_ALLOCATOR_API_NAME);

    tm_set_or_remove_api(reg, load, TM_TXT_TAB_VT_NAME, tab_vt);
    tm_add_or_remove_implementation(reg, load, TM_TAB_VT_INTERFACE_NAME, tab_vt);
}

```



## Open the Tab

After all the previous steps, we can finally make our Text Asset open this Tab!

At first, we need to remove the static of our truth API since we require it in the `txt_tab.c`.

```c
struct tm_the_truth_api *tm_the_truth_api;
```

When that is done, we need to include two more files and get two  more APIs.

```c
// open asset
static struct tm_the_machinery_api* tm_the_machinery_api;
static struct tm_docking_api* tm_docking_api;
//...

#include <plugins/ui/docking.h>
#include <the_machinery/the_machinery_tab.h>
#include <the_machinery/the_machinery.h>
//...
extern void load_txt_tab(struct tm_api_registry_api* reg, bool load);

TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    //...
    // loads the txt tab!
    tm_the_machinery_api = reg->get(TM_THE_MACHINERY_API_NAME);
    tm_docking_api = reg->get(TM_DOCKING_API_NAME);
    load_txt_tab(reg,load);
      //...
}
```

To open an asset, we need to add another aspect to our type. It is the `TM_TT_ASPECT__ASSET_OPEN` aspect! This aspect requires a implementation of the `tm_asset_open_aspect_i`. 

```c
static void create_truth_types(struct tm_the_truth_o *tt)
{
    //...
    tm_the_truth_api->set_aspect(tt,type,TM_TT_ASPECT__ASSET_OPEN,open_i);
    //...
}
```

We add this implementation of the `tm_asset_open_aspect_i` above the `create_truth_types` function.

```c
void open_asset(struct tm_application_o *app, struct tm_ui_o *ui, struct tm_tab_i *from_tab,
        tm_the_truth_o *tt, tm_tt_id_t asset, enum tm_asset_open_mode open_mode){
    
    const tm_docking_find_tab_opt_t opt = {
        .from_tab = from_tab,
        .in_ui = ui,
        .exclude_pinned = true,
    };

    const bool pin = open_mode == TM_ASSET_OPEN_MODE_CREATE_TAB_AND_PIN;
    tm_tab_i *tab = tm_the_machinery_api->create_or_select_tab(app,ui,TM_TXT_TAB_VT_NAME,&opt);

    if (pin)
        tm_docking_api->pin_object(tab, tt, asset);
    else
        tab->vt->set_root(tab->inst, tt, asset);   
    
}

static tm_asset_open_aspect_i* open_i = &(tm_asset_open_aspect_i){
    .open = open_asset,
};

static void create_truth_types(struct tm_the_truth_o *tt)
{
    //...
}
```



The open function gives us all the important information:

1. The App data
2. The UI
3. Which Tab requested this action
4. The current Truth
5. the asset
6. How we will open the Tab.



At first, we define the search criteria for the `create_or_select_tab` of the Machinery API. In this case we want to exclude pinned tabs since the user might have a reason for why they are pinned!

```c
    const tm_docking_find_tab_opt_t opt = {
        .from_tab = from_tab,
        .in_ui = ui,
        .exclude_pinned = true,
    };
```



Now we can create or select a tab by calling the `create_or_select_tab` function.

```c
tm_tab_i *tab = tm_the_machinery_api->create_or_select_tab(app,ui,TM_TXT_TAB_VT_NAME,&opt);
```

The last step is actually to pass some data along! In this case, we need to check if something is pinned or not! Hence we check if the `open_mode` is equal to pinning. If yes, we ask the docking API to pin our Tab.

```c
    const bool pin = open_mode == TM_ASSET_OPEN_MODE_CREATE_TAB_AND_PIN;
    if (pin)
        tm_docking_api->pin_object(tab, tt, asset);
    else
        tab->vt->set_root(tab->inst, tt, asset);   
```
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
2. We make use of the default tab template provided by the engine:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/plugins/my_tab.c}}
```



We modify the following parts of the sample:

- `tab__create_menu_name` & `tab__title` they shall return: `"Text Tab"`
- We remove the `TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)` function since we replace it in the next step.
- To the `tm_tab_o` we add: a pointer to the Truth and a asset entry:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:22:29}}
```

The most important fields here are the **asset** and **tt** filed. They will store the currently used asset and truth. Those fields allow us to access both in various functions.

- We also change the defines to:

  ```c 
  #define TM_TXT_TAB_VT_NAME "tm_txt_tab"
  #define TM_TXT_TAB_VT_NAME_HASH TM_STATIC_HASH("tm_txt_tab", 0x2cd261be98a99bc3ULL)
  ```

After those adjustments we continue with creating a new load function on the bottom of the file:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:114:122}}
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

### Implementing the functions

Now that we have done all the boilerplate code, let us focus on the three functions that count:

- The create function
- The UI Update
- The Set Root function



#### The Create Function

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:63:80}}
```

In this function, we store the allocator first. 

> **Tipp:** if you wanted to create a child allocator, you could do this for your Tab. A child allocator may be very useful when doing many allocations: `tm_allocator_api.create_child()`.

We need to initialize the tab interface so other engine parts can communicate with a generic interface to the Tab. We store a pointer to our Tab within this interface so other callers of the standard generic interface can access this instance and pass it along to the functions. After this, we allocate the Tab itself.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:70:78}}
```

In the end, we return the pointer to the interface, so the docking system has it

#### The Update Function

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:31:51}}
```

At first, we create a copy of the UI Style. With this copy, we can do what we want since the input style is a const pointer. After this, we check if the asset is present. If not, we print a message on the Tab that the user must select a `txt` asset.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:31:34}}
//...
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:44:51}}
```

We need an allocator to copy the data of the buffer into a proper string. The allocator is needed since we never added a null terminator to the end of the string when we save it into the buffer.

In this case, we need a temporary allocator. Since we do not want to keep the memory forever, we need to initialize a temp allocator with `TM_INIT_TEMP_ALLOCATOR` and provide a name. Do not forget to free the memory at the end. 

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:31:36}}
//..
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:43:51}}
```

> **Note:** If the memory is smaller than 1024 bytes, the memory is allocated to the stack. Moreover, an alternative is the frame allocator in which the memory is freed every frame.

The next step is it to ask the truth for the buffer and allocate the right amount of memory. Since we want to copy the data into a null-terminated string, we should add 1 to the data size.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:37:39}}
```

To ensure our string is clean and filled with nulls, we use the inline string file (hence we add the `foundation/string.inl` to our includes). We have the `tm_strncpy_safe` within this header file, which fills up a string with null terminator.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:39}}
```

The last step before we are done is actually to make the text appear on the screen. We make use of the `tm_ui_api.wrapped_text()` since this function will print the string in multiple lines if need be.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:41:42}}
```



#### The set root / root function

The last function which we need is the set root function. This function allows us to set a root object of the Tab from the outside. Its code is quite straightforward:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c:89:98}}
```



### Let us test the Tab

Let us open the Tab from the **Tabs** menu!



[image]



### Source Code

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/tab.c}}
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

{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/txt.c:356:384}}
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
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/txt.c:238:259}}
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
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/txt.c:249}}
```



Now we can create or select a tab by calling the `create_or_select_tab` function.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/txt.c:242:246}}
```

The last step is actually to pass some data along! In this case, we need to check if something is pinned or not! Hence we check if the `open_mode` is equal to pinning. If yes, we ask the docking API to pin our Tab.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/open_asset/txt.c:251:254}}
```
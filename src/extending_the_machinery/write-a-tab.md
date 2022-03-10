# Write a Tab

This walkthrough shows you how to add a custom Tab to the Engine.

During this walkthrough, we will cover the following topics:

- How to create a tab from scratch.
- Where and how do we register the Tab to the Engine.

You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/the_plugin_system.html) and the [Write a plugin guide]({{base_url}}extending_the_machinery/write-a-plugin.html#build-requirements). The goal of this walkthrough is to dissect the Tab plugin provided by the Engine.

**Table of Content**

* {:toc}


## Where do we start?

In this example, we want to create a new plugin, which contains our Tab. We open the Engine go to **file -> New Plugin -> Editor Tab.** The file dialog will pop up and ask us where we want to save our file. Pick a location that suits you.

> **Tip:** Maybe store your plugin in a folder next to your game project.

After this, we see that the Engine created some files for us.

![folder structure new plugin](https://www.dropbox.com/s/jhrqv8t8bbhr20u/tm_tut_new_tab.png?dl=1)

Now we need to ensure that we can build our project. In the root folder (The folder with the premake file), we can run `tmbuild` and see if there is no issue. We will build our projects once and generate the `.sln` file (on windows). 

If there is an issue, we should ensure we have set up the Environment variables correctly and installed all the needed dependencies. For more information, please read this [guide]({{base_url}}build_tools/tmbuild.html).

Now we can open the `.c` file with our favorite IDE. The file will contain the following content:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c)}}
```



## Code structure

Let us dissect the code structure and discuss all the points of interest.



### API and include region

The file begins with all includes and API definitions: 

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,includes)}}
```



The code will fill the API definitions with life in the `tm_load_plugin` function.

The most important aspects here are the two defines on the bottom:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,defines)}}
```

The first one defines the name of our Tab and the second one represents its hash value. The hash value can be used later on to access, search the Tab in the `tm_docking_api`.

> **Note:** If you modify the values, please ensure you ran `hash.exe` again or `tmbuild --gen-hash` so the hash value is updated!

### Define your Data

In the next section, we define the data the Tab can hold. It might be any data you need for the Tab to work and do its job. The tab instance owns the data. It is not shared between Tabs instances. Therefore its lifetime is bound to the current instance.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tm_tab_o)}}
```

A `tm_tab_i` represents a tab object. A tab object is represented as a `vtable` that defines its function interface and an opaque pointer to the Tab's internal data. This design is used so that the application layer can extend the `vtable` with its own interface.

### Define the actual Tab

Every Tab in The Machinery is based on the `tm_tab_vt` and registered to the `tm_tab_vt` in the `tm_load_plugin()` function.

The default `tm_tab_vt` offers multiple options and settings we can set for our Tab. 

| Name                                           | Description                                                  |
| ---------------------------------------------- | ------------------------------------------------------------ |
| `tm_tab_vt.name`                               | Name uniquely identifying this tab type.                     |
| `tm_tab_vt.name_hash`                          | A hash of the `name`.                                        |
| `tm_tab_vt.create_menu_name`()                 | Optional. Returns the (localized) name that should be shown for this tab type in menus that allow you to create new tabs. If this function returns `NULL`, the tab type won't appear in these menus. This can be used for tabs that should only be accessible when certain feature flags are set. |
| `tm_tab_vt.create_menu_category`()             | Optional. Returns the (localized) category that should be shown for this tab type in menus that allow you to create new tabs. If this function returns `NULL` or is not set, the tab type will appear at the root level of the menu, uncategorized. |
| `tm_tab_vt.create`()                           | Creates a new tab of this type and returns a pointer to it. `tm_tab_create_context_t` is an application defined type containing all the data a tab needs in order to be created. `ui` s the UI that the tab will be created in. |
| `tm_tab_vt.destroy`()                          | Destroys the tab                                             |
| **Object methods**                             |                                                              |
| `tm_tab_vt.ui`()                               | Callback for drawing the content of the tab into the specified rect. The `uistyle` is the `tm_ui_api.default_style`() with the clipping rect set to `rect`. |
| `tm_tab_vt.ui_serial`()                        | Optional. If implemented, called from the main UI job once all parallel UI rendering (fork/join) has finished. This can be used for parts of the UI that needs to run serially, for example because they call out to non-thread-safe function. |
| `tm_tab_vt.hidden_update`()                    | This function is o*ptional.* If the Tab wants to do some processing when it is *not* the selected Tab in its tabwell, it can implement this callback. This will be called for all created tabs whose content is currently *not* visible. |
| `tm_tab_vt.title`()                            | Returns the localized title to be displayed for the tab. This typically consists of the name of the tab together with the document that is being edited, such as "Scene: Kitchen*" |
| `tm_tab_vt.set_root`()                         | Optional. Sets the root object of the tab. If a new Truth is loaded, this is called with `set_root(inst, new_tt, 0)`. |
| ` tm_tab_vt.root`()                            | Returns the root object and The Truth that is being edited in the tab. This is used, among other things to determine the undo queue that should be used for Undo/Redo operations when the tab has focus |
| `tm_tab_vt.restore_settings`()                 | Optional. Allow the tab to  restore it's own *state* to the settings. For example the Asset Browser will use this to save the view size of the assets. |
| `  tm_tab_vt.save_settings`()                  | Optional. Allow the tab to save it's own *state* to the settings. For example the Asset Browser will use this to save the view size of the assets. |
| `tm_tab_vt.can_close`()                        | Optional. Returns *true* if the tab can be closed right now and *false* otherwise. A tab might not be able to close if it's in the middle of an important operation. Tabs that do not implement this method can be closed at any time. |
| `tm_tab_vt.focus_event`()                      | [documentation](https://ourmachinery.com//apidoc/plugins/ui/docking.h.html#structtm_tab_vt.focus_event()) |
| `tm_tab_vt.feed_events`()                      | Optional. For feeding events to the tab. Useful for feeding events to UIs that are internal  to a tab. |
| `tm_tab_vt.process_dropped_os_files`()         | Optional. If set, the tab will receive the path to the files that were dropped from the OS since the previous frame. |
| `tm_tab_vt.toolbars`()                         | Optional. Returns a carray of toolbars to be drawn in the tab, allocated using `ta`.  [How to add toolbars](#) |
| `tm_tab_vt.need_update`()                      | Optional. Allow the tab to decide whether it's UI needs an update. Tabs that have animated components like the pong tab will return always true, while other tab may decide to return true only under certain circumstances. If not provided, the assumed default value will be true, so the tab will be updated every frame. If it returns false the UI will be cached. Therefore any call to `.ui` wont be called. |
| `tm_tab_vt.hot_reload`()                       | Optional. Will be called after any code hot reload has happened. |
| `tm_tab_vt.entity_context`()                   | Optional. Should be implemented if tab owns an entity context. |
| `tm_tab_vt.viewer_render_args`()               | Optional. Should be implemented if tab owns an entity context that supports to be rendered outside of it's UI callbacks. |
| **Flags**                                      |                                                              |
| `tm_tab_vt.cant_be_pinned`                     | If set to *true*, the tab can't be pinned even though it has a *root* function. |
| `tm_tab_vt.run_as_job`                         | If set to *true*, the tab's UI will run as a background job, parallel to the rest of the UI  rendering. **Warning:** Setting this to *true* indicates to the docking system that the `ui()` function is thread-safe. If the function is not actually thread-safe you will see threading errors. |
| `tm_tab_vt.dont_restore_at_startup`            | If set to *true*, the tab will be considered _volatile_, and it won't be restored when the last opened project is automatically opened at startup, even if the user had the tab opened when the project was closed. |
| `tm_tab_vt.dont_restore_root_asset_at_startup` | If set to *true*, the tab will be restored at startup, but the root of the tab won't be set to the one that was set during application shutdown. Basically the project will be restored, but it will be always _empty_. |

In this example, we make use of the following options:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tm_tab_vt)}}
```

In the cause of the rest of this walkthrough, we will discuss:`tab__create_menu_name`,  `tab__create`, `tab__destroy` , `tab__title` and `tab__ui`.

### Define the metadata functions

As we can see in our definition of the `custom_tab_vt` object we provide the `tm_tab_vt.create_menu_name()` and the `tm_tab_vt.title()`. The `create_menu_name` is an optional function to allow you to provide a name for the create tab menu. In contrast, the `title()` function is not optional and is needed. It provides the name of the Tab, which the editor shall show in the tab bar.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tab_meta}}
```

### Define create and destroy the Tab

As mentioned before, the data of a tab is bound to its lifetime. Therefore you should create the data on `create` and let go of it on `destroy.`

The create function provides you the `tm_tab_create_context_t` access to many essential things, such as an allocator. This allocator is the one you should use directly or create a child allocator.

> **Note:** for more information check `tm_tab_create_context_t`'s documentation.



```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tab__create)}}
```

We use the provided allocator to allocate the Tab struct, and then we initialize it with the data we deem to be needed. 

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tm_alloc)}}
```

Since we have allocated something, we need to keep track of the used allocator! Hence we have it as a member in our Tab struct.

In the end, we pass a pointer to the Tab interface.

```c
 return &tab->tm_tab_i;
```

When it comes to free the Tab data, we can just call `tm_free()` on our Tab:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tab__destroy)}}
```



## Define the UI update

In the default example, we create a Tab that only updates when the Tab is active and visible. Therefore we do not need the `tm_tab_vt.hidden_update()` function and can just implement the required one: `tm_tab_vt.ui()`.

The Tab itself shall not be jobifed since `run_as_job` is not provided (its default value is false). Therefore we know our function itself may contain none thread safe elements.

If we wanted to make our Tab jobifed, we could make use of the `tm_tab_vt.hidden_update()` function. This function is o*ptional.* If the Tab wants to do some processing when it is *not* the selected Tab in its tabwell, it can implement this callback. This will be called for all created tabs whose content is currently *not* visible.

Let us digest the current code line by line:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tab__ui)}}
```

The `tm_docking_api`, which will call our Tab's update, provides us with the essential information:

- `tm_tab_o* tab` our tab data to access any data we need
- `tm_ui_o* ui` an instance of the UI, needed to call the `tm_ui_api`
- `const tm_ui_style_t* uistyle_in` an instance of the current UI style, can be used to create a local version of it to modify the UI Style for this Tab.
- `tm_rect_t rect` the render surface of the Tab.

In the first line of the function body, we create a new instance of the UI Buffers. You may use them to access the underlying buffers for calls to the`tm_draw2d_api`.Also, this object allows access to the commonly shared metrics and colors.

```c
tm_ui_buffers_t uib = tm_ui_api->buffers(ui);
```

After this, we define our local copy of the UI Style. Then we create an empty `tm_draw2d_style_t` instance. We need to create a Style from the UI Style. You need ` tm_draw2d_style_t* style` later for drawing anything with our draw 2d api.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tm_draw2d_style_t)}}
```

Now we are set, and we can finally color our tab background to red. You can do this with the `tm_draw2d_api.fill_rect()` call. Beforehand we need to change our style's color to red and then call the `tm_draw2d_api.fill_rect()`. We need to pass in the vertex buffer and the index buffer pointer so the function can draw into them.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,draw)}}
```



> **Note:** For more information on the rational behind the UI System please check out this blog post [https://ourmachinery.com/post/one-draw-call-ui/ ](https://ourmachinery.com/post/one-draw-call-ui/ )



## Register the Tab

The last thing before we can compile our project and test it in the Engine is registering the Tab to the Plugin System. As mentioned before, you need to register the Tab to the: `tm_tab_vt` .

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_tab.c,tm_load_plugin)}}
```


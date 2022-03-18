# Toolbars and Overlays

In the Machinery, tabs can provide toolbars. If you wish to use custom toolbars within The Machinery tabs, you do not need to use anything within [tm_toolbar_api]({{docs}}plugins/ui/toolbar.h.html#structtm_toolbar_api). The docking system will ask your tab for a list of toolbars to draw each frame. See [tm_tab_vt->toolbars()]({{docs}}plugins/ui/docking.h.html#structtm_tab_vt.toolbars()).

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428649231_new_order_toolbars.gif)

In this walkthrough, we will learn how to write our little toolbar for our newly added tab! This walkthrough requires you to know how our plugin system works.

**Table of Content**

* {:toc}
## Implement a Toolbar in a Tab

To begin with, we need to create a new tab plugin. We go on **File -> New Plugin -> Tab.** 

A file dialog pops up, and we can decide where to store our plugin.

![](https://www.dropbox.com/s/jhrqv8t8bbhr20u/tm_tut_new_tab.png?dl=1)

We open the `custom_tab.c` (or however we called it) file with our favorite editor.



We search for the line in which we define the tab itself:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/toolbars_overlays.c,vtable)}}
```





To our definition, we add a [`toolbars()`]({{docs}}plugins/ui/docking.h.html#structtm_tab_vt.toolbars()). This function returns a C-Array of toolbar definitions.  The array is allocated with the passed in the temporary allocator.



> **Note:** A temporary allocator ([tm_temp_allocator_api]({{docs}}foundation/temp_allocator.h.html)) Provides a system for temporary memory allocations. I.e., short-lived memory allocations that are automatically freed when the allocator is destroyed. Temp allocators typically use a pointer bump allocator to allocate memory from one or more big memory blocks and then free the entire block when the allocator is destroyed.
>
> **Important:** You need to include  the api first `#include <foundation/temp_allocator.h>` and get the api from the registry!

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/toolbars_overlays.c,new_vtable)}}
```

After we have added this, we need actually to define the function itself:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/toolbars_overlays.c,tab__toolbars)}}
```



Within this function, we define our toolbars. Our toolbar will have an essential job! It will have a button that prints "Hello World".

To make this work, we need to create a C-Array of `tm_toolbar_i` objects and add our toolbar to it. This interface expects the following things:

| Field          | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| id             | An application-wide unique ID for the toolbar. **Cannot be zero.** |
| owner          | A pointer that can be accessed through the `toolbar` argument to the functions of this struct. Often used to store state for the toolbar, for example if you drawing toolbars inside a tab then you might want to store a pointer to that tab here. |
| ui             | Called when [`ui()`]({{docs}}plugins/ui/toolbar.h.html#structtm_toolbar_api.ui()) of [`tm_toolbar_api`]({{docs}}plugins/ui/toolbar.h.html#structtm_toolbar_api) wants to draw the toolbar. Make sure to respect `draw_mode` and return the rect that encompasses all the drawn controls. For toolbars inside horizontal and vertical containers, you can use [`tm_toolbar_rect_split_off()`]({{docs}}plugins/ui/toolbar.h.html#tm_toolbar_rect_split_off()) and [`tm_toolbar_rect_advance()`]({{docs}}plugins/ui/toolbar.h.html#tm_toolbar_rect_advance()) to easily manage the rect sizes while drawing your toolbar.</br>If you need to store state, the make sure to set `owner` when you create the [`tm_toolbar_i`]({{docs}}plugins/ui/toolbar.h.html#structtm_toolbar_i) object and get it from the passed `toolbar` pointer. |
| draw_mode_mask | A combination of supported draw modes, ORed together values of [`enum tm_toolbar_draw_mode`]({{docs}}plugins/ui/toolbar.h.html#enumtm_toolbar_draw_mode). The `ui` function will be passed the currently used draw mode and is expected to handle it. |

> **Note:** For a complete list please check the [documentation]({{docs}}plugins/ui/toolbar.h.html#structtm_toolbar_i)

| Mask                              | Description                         |
| --------------------------------- | ----------------------------------- |
| `TM_TOOLBAR_DRAW_MODE_HORIZONTAL` | You an draw the toolbar horizontal. |
| `TM_TOOLBAR_DRAW_MODE_VERTICAL`   | You an draw the toolbar vertical.   |
| `TM_TOOLBAR_DRAW_MODE_WIDGET`     | The toolbar is an overlay           |

Let us provide the essential things:

1. The id is to be able to identify the toolbar.
2. The UI function is to be able to draw something.
3. The draw_mode_mask to indicate where we want the toolbar to be drawn.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/toolbars_overlays.c,tab__toolbars,off)}}
```



In our UI function, we can add the button via the [`tm_ui_api`]({{docs}}plugins/ui/ui.h.html#structtm_ui_api). Then log the string "Hello World" to the screen with the [logger API]({{docs}}foundation/log.h.html#log.h).

> **Note:** You need include the `plugins/ui/ui.h` and the `foundation/log.h` as well as get the API's first!

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/toolbars_overlays.c,toolbar__ui)}}
```



## Tab Overlays

![An image with visualization modes enabled using the Visualize overlay, as well as a Renderer Statistics overlay. The Visualize overlay is found in Top right toolbar → Render → Lighting Module → Show as overlay. The Statistics overlay is found in Top right toolbar → Statistics.](https://paper-attachments.dropbox.com/s_538DCFE5C2E14B8A7C343B96D5CD2C3E2C191E06DD3EF47F66924FDF7AE2C192_1617105468374_image.png)


As an extension to the dockable toolbars the engine support overlays that hover on top of the tabs. Also, any toolbar can be pulled off and be made into a hovering overlay.

An overlay is just a toolbar that does not belong to any of the four toolbar containers that run along the edge of the tab. Toolbars have three rendering modes — horizontal, vertical, and widget. The widget mode is new, it is the richer, window-like mode seen in the picture above. 

In the scene and simulate tabs, we’ve added:

- A rendering visualization overlay. Found in `Render → Lighting Module → Show as overlay` in the top right toolbar.
- A Statistics button (also top right toolbar) that makes it possible to popup statistics overlays, previously found within the Statistics tab.

The tab should return all toolbars it wishes to draw each frame, see [`tm_tab_vt->toolbars()`]({{docs}}plugins/ui/docking.h.html#structtm_tab_vt.toolbars()). If you wish to support widget mode drawing, then make sure to set the bitmask [`tm_toolbar_i->draw_mode_mask`]({{docs}}plugins/ui/toolbar.h.html#structtm_tab_toolbar_i.draw_mode_mask) a value that contains [`TM_TOOLBAR_DRAW_MODE_WIDGET`]({{docs}}plugins/ui/toolbar.h.html#enumtm_toolbar_draw_mode).

Toolbars are generalized and they are not coupled to the docking system and the tabs, so you could use them within other contexts if you wish. 

## How to use toolbars outside of The Machinery tabs

See the documentation under `How to use toolbars outside of The Machinery tabs` in [toolbar.h]({{docs}}plugins/ui/toolbar.h.html).
# Creating tab layouts through code

The Machinery allows you to fully customize the editor layout. For personal layouts this system can be fully utilized without using code (see [Interface Customizations]({{base_url}}the_editor/customizations.html) for more information), but you might want to create custom default layouts that get defined procedurally, this allows for more control when loading and saving the layout.

Creating layouts in code can be done though the `tm_tab_layout_api`. Here various functions are available for tab management. In this tutorial we’ll go over how the default workspace is created using the `save_layout` function.

In order to create a layout for The Machinery editor we need access to the editor settings. This is done through `tm_the_machinery_api`. This tutorial uses the `tm_the_machinery_create_layout_i` interface in order to gain access to the settings. In these settings we have access to the window layouts, which is the subobject we want to append our layout to. The first things we should do however is check whether our layout already exists so we don’t create a new one every time on startup.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/custom_layouts.c,create_layout)}}
```

After this we can start to define our actual tab layout. This is done through the `tm_tab_layout_t`. In this layout we can recursively define our tab layout with three distinct options per tabwell.

- We can split the tabwell horizontally, creating top and bottom child tabwells.
- We can split the tabwell vertically, creating left and right child tabwells.
- We can define (up to 3) tabs that should be in this tabwell.
![](https://www.dropbox.com/s/ggiq4uv6htgwnpj/tm_tut_default_layout.png?dl=1)

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/custom_layouts.c,tm_tab_layout_t)}}
```

Defining the tabs is relatively straight forward, you define them using their name hash. Splitting a tabwell horizontally or vertically however requires a `bias` parameter. This defines the ratio of both tabs. Zero means both tabs are of equal size, whereas 1 means that the primary tab (left or top) fully encompass the tabwell whilst the secondary tab (right or bottom) is hidden. Negative values allow you to use the secondary tab as if it was the primary tab.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/custom_layouts.c,register)}}
```

Finally we can store our layout in the application settings. The top level object for this is the
window layout. This specified the default position and size of the window if the user decides the
instantiate the layout in a new window rather than as a workspace. 

## Entire Sample

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/ui/custom_layouts.c)}}
```

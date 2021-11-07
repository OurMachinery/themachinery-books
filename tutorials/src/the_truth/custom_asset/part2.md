# Create a Custom Asset Type: Part 2

This part will cover the following topics:

- How to store data in a buffer that is associated with the asset file.
- How to give the asset a custom UI in the Property View.

The [next part]({{base_url}}the_truth/custom_asset/part3.html) shows how to write an importer for the asset.

>  You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* auto-gen TOC;
{:toc}
## Adding More Properties to the The Truth Type

The Truth type we created in Part 1 cannot do much, because it doesn't have any properties:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:15:20}}
```

To actually store some data in the objects, we want to add some properties to the Truth type. Note that we pass in an array of properties when we create the type with `tm_the_truth_api->create_object_type()`.

For our text file objects that are two pieces of data that we want to store:

1. The text data itself.
2. The path on disk (if any) that the text file was imported from.

Storing the *import path* is not strictly necessary, but we'll use it to implement a "reimport" feature. This lets our data type work nicely with text files that are edited in external programs.

Here's how we can define these properties:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:45:48}}
```

>  **Note:** The type [*tm_the_truth_property_definition_t*]({{docs}}foundation/the_truth.h.html#structtm_the_truth_property_definition_t) has a lot more options. For example, is it possible to hide properties from the editor, etc. For more information, read the documentation [*here*]({{docs}}foundation/the_truth.h.html#structtm_the_truth_property_definition_t)*.*

In this case we decided to store the text as a *buffer* instead of a *string*. Buffers can be streamed in and out of memory easily, so if we expect the text files to be large, using a buffer makes more sense than using a string.

We can now create the Truth type with these properties:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:43:55}}
```

Let's also change the asset name to something more meaningful than `my_asset`. We'll call it `txt`. We need to update this new name in four places:

- Asset Name
- Menu Name
- File extension
- The source file: `my_asset.c/h` -> `txt.c/h`

This will change the code as follows:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:43:44}}
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:50}}
}
// .. other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:62:66}}
```

Let's have a look at how it looks in the editor:

![creating a new asset](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609926443262_image.png)

If we create a new *Text* file and select it, this is what we will see in the Properties View:

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609926772154_image.png)

The `Data` property is `nil` because we haven't loaded any data into the file yet. Let's add a UI that let's us import text files from disk.

(Another option would be to add a *Text Editor* UI that would let us edit the text data directly in the editor. However, writing a good text editor is a big task, so for this tutorial, let's use an import workflow instead.)

### Custom UI

To show an **Import** button in the Properties View, we need to customize the Properties View UI of our type. We can do this by adding a `TM_TT_ASPECT__PROPERTIES` to the Truth type.

The `TM_TT_ASPECT__PROPERTIES` is implemented with a `tm_properties_aspect_i` struct. This struct has a lot of field that can be used to customize various parts of the Properties View (for more information on them, check out the [documentation]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_aspect_i)). For our purposes, we are interested in the `custom_ui()` field that lets us use a custom callback for drawing the type in the Properties View.

`custom_ui()` wants a function pointer of the type `float (*custom_ui)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)`.

Let us quickly go over this:

| **Argument** | **Data Type**             | **Description**                                              |
| ------------ | ------------------------- | ------------------------------------------------------------ |
| `args`       | `tm_properties_ui_args_t` | A struct with information from the Properties View that can be used in drawing the UI. For example, this has the `ui` instance as well as the `uistyle` which you will need in any `tm_ui_api` calls. For more information check the [documentation]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t). |
| `item_rect`  | `tm_rect_t`               | The rect in the Properties View UI where the item should be drawn. Note that the height in this struct (`item_rect.h`) is the height of a standard property field. You can use more or less height to draw your type as long as you return the right `y` value (see below). |
| `object`     | `tm_tt_id_t`              | The ID of the Truth object that the Properties View wants to draw. |
| `indent`     | `uint32_t`                | The current indentation level. Usually just passed along to functions in the `tm_properties_view_api` |

| **Return value** | **Description**                                              |
| ---------------- | ------------------------------------------------------------ |
| float            | Returns the `y` coordinate where the next item in the Propertiew View should be drawn. This should be `item_rect.y` + however much vertical space your controls are using. |

To implement the `custom_ui()` function we can make use of the functions for drawing property UIs found in `tm_properties_view_api`, or we can draw UI directly using `tm_ui_api`. Once we've implemented `custom_ui()` we need a instance of `tm_properties_aspect_i` to register. This instance must have global lifetime so it doesn't get destroyed:


```c
//.. other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:21}}
{
// -- code
}
//.. other code    
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:51:53}}
// .. other code
```

Now we can register this aspect with `tm_truth_api`:

```c
//.. other code
static void create_truth_types(struct tm_the_truth_o *tt)
{
//... the other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:54}}
}
//... the other code
```

In the editor, the change is imminently visible. The UI is gone, because it is now using our `custom_ui()` function, but our `custom_ui()` function isn't drawing anything.

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609928409366_image.png)

Let's add the `Imported Path` property back to the UI. We can look at the [properties view API]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_view_api) for a suitable function to draw this property (if we can't find anything we may have to write a custom drawer ourselves).

We could use `tm_properties_view_api->ui_property_default()`. This would use the default editor based on the property type. For a `STRING` property, this is just a text edit field, the same thing that we saw before implementing our `custom_ui()` function. (If we don't have a custom UI, the default UI for each property will be used.)

We chould also use `tm_properties_view_api->ui_string()`. This is just another way of drawing the default `STRING` UI.

But for our purposes, `tm_properties_view_api->ui_open_path()` is better. This is a property UI specifically for file system path. It will draw a button, and if you click the button a system file dialog is shown that let's you pick a path.

Note that in order to use `tm_properties_view_api` we need to load it in our `tm_load_plugin()` function:


```c
// -- api's
static struct tm_properties_view_api *tm_properties_view_api;
//.. other code 
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
//.. other code 
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:71}}
//.. other code 
} 
```

Now we can call `ui_open_path()` . Let's start by looking at its [signature]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_view_api.ui_open_path()):

`float (*ui_open_path)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, const char *name, const char *tooltip, tm_tt_id_t object, uint32_t property, const char *extensions, const char *description, bool *picked)`

| **Argument**  | **Data Type**                                                | **Description**                                              |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `args`        | [tm_properties_ui_args_t]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t) | For this argument, we should pass along the `args` pointer we got in our `custom_ui()` function. |
| `item_rect`   | [tm_rect_t]({{docs}}foundation/api_types.h.html#structtm_rect_t) | The rect where we want the UI of the control to be drawn (including the label). |
| `name`        | `const char*`                                                | The label that the Properties View UI will display in front of the button. |
| `tooltip`     | `const char*`                                                | Tooltip that will be shown if the mouse is hovered over the label. |
| `object`      | [tm_tt_id_t]({{docs}}foundation/api_types.h.html#structtm_tt_id_t) | The Truth object that holds the path `STRING` that should be edited. |
| `property`    | `uint32_t`                                                   | The index of the `STRING` property that should be edited.    |
| `extension`   | `const char*`                                                | List of file extensions that the open file dialog should show (separated by space). |
| `description` | `const char*`                                                | Description of the file to open shown in the open file dialog. |
| `picked`      | `bool*`                                                      | Optional out pointer that is set to `true` if a new file was picked in the file dialog. |



| **Return value** | **Description**                                             |
| ---------------- | ----------------------------------------------------------- |
| float            | The `y` coordinate where the next property should be drawn. |

We can now implement the function:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:45:48}}
```

Note that we are using the property index `TM_TT_PROP__MY_ASSET__FILE` that we defined in the header file hearlier:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.h}}
```

We can now test this in the engine. We see an **Import Path** label with a button and when we click it, we get asked to import a file.

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609931496164_image.png)

Next, we want to make sure that when the user picks a file using this method, we load the file and store it in our `DATA` buffer.

To load files we can use the `tm_os_api` which gives us access to OS functionality. `tm_os_api` has a lot of sub-APIs for different purposes (files, memory, threading, etc). In our case, what we need is `tm_os_api->file_io` which provides access to File I/O functionality:


```c
//other includes
#include <foundation/os.h>
#include <foundation/buffer.h>
//.. other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:21:41}}
```

When a new file is picked in the UI (checked with the `picked` variable) we get the file path from The Truth, read the file data and store it in The Truth.

To manage buffers, we make use of the interface in `buffers.h`. Creating a buffer is a three step process:

* Allocating the memory for the buffer (based on the file size).
* Filling the buffer with content (in this case, from the text file).
* Adding the buffer to the `tm_buffers_i` object.

Once we have created the buffer, we need to set the `BUFFER` `data` item in the Truth object to this buffer. Changing a value in The Truth is another three step process:

* Ask the Truth for a *write pointer* to the object using `write()`.
* Set the buffer for the *write pointer* using `set_buffer()`.
* Commit the changes to the Truth using `commit()`.

We need this somewhat complicated procedure because objects in The Truth are immutable by default. This ensures that The Truth can be used from multiple threads simulatenously. When you change a Truth object using the `write()`/`commit()` protocol, the changes are applied atomically. I.e., other threads will either see the old Truth object or the new one, never a half-old, half-new object.

If you want the change to go into the undo stack so that you can revert it with **Edit → Undo**, you need some additional steps:

* Create an *undo scope* for the action using `create_undo_scope()`.
* Pass that undo scope into `commit()`.
* Register the undo scope with the application's undo stack (found in `args->undo_stack`).

To simplify this example, we've skipped that step and instead we use `TM_TT_NO_UNDO_SCOPE` for the `commit()` action which means the action will not be undoable.

## What Is Next?

In the next part we'll show how to add an *Importer* for our asset type. This will let us drag and drop text files from the explorer into the asset browser.

[Part 3](#)

## Full Example of Basic Asset

`my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.h}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`)

`my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c}}
```






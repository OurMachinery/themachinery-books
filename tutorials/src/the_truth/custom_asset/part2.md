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

To archive our first manual loading, we need to add a custom UI associated with our type. We can do this via the properties aspect `TM_TT_ASPECT__PROPERTIES`. It means we need to go back to the `create_truth_types` function and add a new Aspect and a new object associated with this Aspect.

The Aspect expects a [tm_properties_aspect_i]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_aspect_i) object. When defining the object, we are focused only on is the custom_ui field. 

> Note: This struct has many different fields which are not interesting to us now. (If you want more information on them, check out the [documentation]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_aspect_i).

The `custom_ui` expected s function pointer of the type `float (*custom_ui)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)`.

Let us quickly go over this:

*Function Arguments:*

| **Argument**    | **Data Type**                                                | **Description**                                              |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1 (`args`)      | [tm_properties_ui_args_t]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t) | A bundled type of important information. For example this is the way you would retrieve your ui instance as well as your uistyle instance. For more information check the [documentation]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t). |
| 2 (`item_rect`) | [tm_rect_t]({{docs}}foundation/api_types.h.html#structtm_rect_t) | The ui rectangular of the current item. This can be manipulated in x,y as well as w and h as long as the correct y value is being returned. |
| 3 (`object`)    | [tm_tt_id_t]({{docs}}foundation/api_types.h.html#structtm_tt_id_t) | The truth object id of the current object. Can be used to read information of. |
| 4 (`indent`)    | `uint32_t`                                                   | Used for intention.                                          |

*Return values*

| **Type** | **Description**                                              |
| -------- | ------------------------------------------------------------ |
| float    | This is the being used as the next y value of the following element. |

We need to define a static instance of the [tm_properties_aspect_i*]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_aspect_i) and a custom UI function.


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

Now the properties aspect needs to know about the existence of our custom UI. It follows the same principle as the properties:

```c
//.. other code
static void create_truth_types(struct tm_the_truth_o *tt)
{
//... the other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:54}}
}
//... the other code
```

In the editor, the change is imminently visible. The UI is gone because we have chosen to provide our custom UI.

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609928409366_image.png)


It is time to add the imported file property back to the UI panel. The first step is to think about what our property shall represent:
When we defined it, we described it as type `TM_THE_TRUTH_PROPERTY_TYPE_STRING`. 
It is essential to know because the [properties header file]({{docs}}plugins/editor_views/properties.h.html#properties.h) has the [properties view API]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_view_api), which has many built-in functions for default behavior.

One of the things we can find in there is the [ui_open_path]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_view_api.ui_open_path()) which sounds perfect for the import path. The buffer (data) does not need to be displayed yet. Before using any Properties-View API functions, we need to request the API in our load plugin function.


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

Now we can use and implement the path opening function. Let us look at its [signature]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_view_api.ui_open_path()) first:

`float (*ui_open_path)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, const char *name, const char *tooltip, tm_tt_id_t object, uint32_t property, const char *extensions, const char *description, bool *picked)`

 *Function Arguments:*

| **Argument**      | **Data Type**                                                | **Description**                                              |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1 (`args`)        | [tm_properties_ui_args_t]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t) | A bundled type of important information. For example this is the way you would retrieve your UI instance as well as your `uistyle` instance. For more information check the [documentation]({{docs}}plugins/editor_views/properties.h.html#structtm_properties_ui_args_t). |
| 2 (`item_rect`)   | [tm_rect_t]({{docs}}foundation/api_types.h.html#structtm_rect_t) | The UI rectangular of the current item. This can be manipulated in x,y as well as w and h as long as the correct y value is being returned. |
| 3 (`n`ame)        | `const char*`                                                | This is the name the Properties tab will display as the title in front of the text field. |
| 4 (`t`ooltip)     | `const char*`                                                | Extra information if needed. (Optional)                      |
| 5 (object)        | [tm_tt_id_t]({{docs}}foundation/api_types.h.html#structtm_tt_id_t) | The truth object id of the current object. Can be used to read information of. |
| 6 (property)      | `uint32_t`                                                   | Property index                                               |
| 7 (`extensions`)  | `const char*`                                                | List of potential file extension supported by the open dialog |
| 8 (`description`) | `const char*`                                                | List of descriptions for the potential file extensions       |
| 9 (picked)        | `bool*`                                                      | Out pointer indicating if a file has been picked or not. (optional) |

*Return values*

| **Type** | **Description**                                              |
| -------- | ------------------------------------------------------------ |
| float    | This is the being used as the next y value of the following element. |

To implement the function all that's needed to remember is what index the property had.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:45:48}}
```

The index is 0 there for we are no ready to implement the function:


```c
//custom ui
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:21}}
{
    // -- code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:24:27}}
        // import...
    }
    return item_rect.y;
}
```

Remembering all of those indices is quite cucumbersome! Therefore, it is better to define an enum in our header file. Define an `enum` for each property `TM_TT_PROP__[NAME_OF_TYPE]__[NAME_OF_PROPERTY]`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.h}}
```

(`txt.h`)

When we compiled this we can test it in the engine, just by adding a new text file click on the Import Path:

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609931496164_image.png)


The next step is using the OS API to load a file from the disc and store it in the buffer. This process works after the same principle as adding the properties view API. 

The OS API ([tm_os_api]({{docs}}foundation/os.h.html#structtm_os_api)) lives in the `os.h` and has a member called [file_io]({{docs}}foundation/os.h.html#structtm_os_file_io_api), allowing access to the `tm_os_file_io_api`. With this API, we can read a file. The following example code shows how reading the file and storing it in a buffer could look like in this case. 


```c
//other includes
#include <foundation/os.h>
#include <foundation/buffer.h>
//.. other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c:21:41}}
```

First, we need to read out the file path from our The Truth object. After that, we can create the buffer we want to add to our *data* property (index 1 or `TM_TT_PROP___MY_ASSET__DATA`). 
The buffers live in the `buffer.h`. We create the buffer via The Truth, and it also owns the memory. We are using the [file_system API]({{docs}}foundation/os.h.html#structtm_os_file_system_api) to get the size of the text file. We need to know how big the file is to understand how big the buffer should be. 

> Note: We should also check if the file exists. It has been left out because we just picked the file. 

Then we are reading the file from the disc and store its content in the allocated buffer. The next step is to add the buffer to the Truth buffers via the [buffers->add(buffers->inst, buffer, stat.size, 0);]({{docs}}foundation/buffer.h.html#structtm_buffers_i.add()) call. It adds a buffer containing the specified data of size. It returns an ID identifying the new buffer. For more information, read [here]({{docs}}foundation/buffer.h.html#structtm_buffers_i.add()).

Now we need to ask the Truth to give us a writeable object. Objects from the Truth are immutable in their default state and can only be made mutable by asking explicitly for a writable object.
This happens via the [tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, object);]({{docs}}foundation/the_truth.h.html#structtm_the_truth_api.write()) call.

With the writeable object, we can set the buffer, and then we can commit the changes to the Truth itself.

This iteration is the first, but the issue with it is that we cannot import or drag and drop a .txt file into the Engine. We will tackle this issue in the [next part](#).



## What is next?

The next part will refactor the current code and show you how to make your code and asset more useful by showing you how to program an importer.

[Part 3](#)

## Full example of basic asset

`my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.h}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`)

`my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_2/txt.c}}
```






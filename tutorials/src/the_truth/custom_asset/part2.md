# Create a custom asset part 2

This walkthrough shows you how to add a custom asset to the Engine. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide]({{base_url}}/the_machinery_book/extending_the_machinery/the_plugin_system.html). The goal for this walkthrough is to write a text file asset.

This part will cover the following topics:

- How to store data in a buffer that is associated with the asset file
- How to add a custom UI to be associated with the asset.

When you have finished this part in the [next one]({{base_url}}/tutorials/the_truth/custom_asset/part3.html), we will show you how to write your importer.

>  You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* auto-gen TOC;
{:toc}


## Extending the asset The Truth Type

The asset type we created is nice but it cannot do much. The Machinery can save anything to file that it can store in the Truth. This thought brings us back to the part: **“What kind of asset do we want to create?”.** 

Let us go back to the basic definition of the type `my_asset`. We defined the type without any properties.

The current implementation looks as follows:

```c
// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_ASSET, 0, 0);
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "my_asset");
}
```

To make this more useful, what we can do is add some properties to the type. We can do this via an array of the type [tm_the_truth_property_definition_t](https://ourmachinery.com//apidoc/foundation/the_truth.h.html#structtm_the_truth_property_definition_t). In this array we can define all the properties we want. 


## Text file asset

Now we are changing the `my_asset` to be able to store text in it. 

First, we need to answer the question: *How is a text file defined?* 

Well, a text file has three properties: 

1. It has a file name
2. A file path
3. data - A bunch of characters.

Consequently, we are defining the *import path* property to “reimport” our text asset and the data property to store the imported text.

```c
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER},
    };
```

>  **Note:** The type [*tm_the_truth_property_definition_t*](https://ourmachinery.com//apidoc/foundation/the_truth.h.html#structtm_the_truth_property_definition_t) has a lot more options. For example, is it possible to hide properties from the editor, etc. For more information, read the documentation [*here*](https://ourmachinery.com//apidoc/foundation/the_truth.h.html#structtm_the_truth_property_definition_t)*.*

After we have thought about this, we need to provide the `create_object_type` function with the new information:


```c
static void create_truth_types(struct tm_the_truth_o *tt)
{
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER},
    };
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_ASSET, my_asset_properties, 2);
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "my_asset");
}
```

Now we should change the asset name to something more meaningful than `my_asset`. Lets call it `txt`

The renaming has as a consequence that we need to change three places:

- Asset Name
- Menu Name
- File extension
- The source file: `my_asset.c/h` -> `txt.c/h`

This will change the code as follows:

```c
//.. other code
static void create_truth_types(struct tm_the_truth_o *tt)
{
//... the other code
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "txt");
}
// .. other code
static tm_asset_browser_create_asset_i asset_browser_create_my_asset = {
    .menu_name = TM_LOCALIZE_LATER("New Text File"),
    .asset_name = TM_LOCALIZE_LATER("New Text File"),
    .create = asset_browser_create,
};
```

Let's have a look at how it looks in the editor:

![creating a new asset](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609926443262_image.png)

## Load a text file

After creating a new asset, the asset looks as following in the editor:

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609926772154_image.png)


This asset file is still not quite how we want it because we have not loaded a text file yet. Therefore let us load a file next. At first, we will do it by *hand* via loading a file whenever we are changing the path, and then later on (in the next chapter) we are writing our importer. It will allow us to drag and drop files into the Engine as well or use the *Import Menu.*

### Custom UI

To archive our first manual loading, we need to add a custom UI associated with our type. We can do this via the properties aspect `TM_TT_ASPECT__PROPERTIES`. It means we need to go back to the `create_truth_types` function and add a new Aspect and a new object associated with this Aspect.

The Aspect expects a [`tm_properties_aspect_i`](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_aspect_i) object. When defining the object, we are focused only on is the custom_ui field. 

> Note: This struct has many different fields which are not interesting to us now. (If you want more information on them, check out the [documentation](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_aspect_i).

The `custom_ui` expected s function pointer of the type `float (*custom_ui)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)`.

Let us quickly go over this:

*Function Arguments:*

| **Argument**    | **Data Type**                                                | **Description**                                              |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1 (`args`)      | [tm_properties_ui_args_t](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_ui_args_t) | A bundled type of important information. For example this is the way you would retrieve your ui instance as well as your uistyle instance. For more information check the [documentation](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_ui_args_t). |
| 2 (`item_rect`) | [tm_rect_t](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_rect_t) | The ui rectangular of the current item. This can be manipulated in x,y as well as w and h as long as the correct y value is being returned. |
| 3 (`object`)    | [tm_tt_id_t](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_tt_id_t) | The truth object id of the current object. Can be used to read information of. |
| 4 (`indent`)    | `uint32_t`                                                   | Used for intention.                                          |

*Return values*

| **Type** | **Description**                                              |
| -------- | ------------------------------------------------------------ |
| float    | This is the being used as the next y value of the following element. |

We need to define a static instance of the [tm_properties_aspect_i*](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_aspect_i) and a custom UI function.


```c
//.. other code
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
// -- code
}
//.. other code    
static tm_properties_aspect_i properties_aspect = {
        .custom_ui = properties__custom_ui,
    };
// .. other code
```

Now the properties aspect needs to know about the existence of our custom UI. It follows the same principle as the properties:

```c
//.. other code
static void create_truth_types(struct tm_the_truth_o *tt)
{
//... the other code
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__PROPERTIES, &properties_aspect);
}
//... the other code
```

In the editor, the change is imminently visible. The UI is gone because we have chosen to provide our custom UI.

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609928409366_image.png)


It is time to add the imported file property back to the UI panel. The first step is to think about what our property shall represent:
When we defined it, we described it as type `TM_THE_TRUTH_PROPERTY_TYPE_STRING`. 
It is essential to know because the [properties header file](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#properties.h) has the [properties view API](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_view_api), which has many built-in functions for default behavior.

One of the things we can find in there is the [ui_open_path](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_view_api.ui_open_path()) which sounds perfect for the import path. The buffer (data) does not need to be displayed yet. Before using any Properties-View API functions, we need to request the API in our load plugin function.


```c
// -- api's
static struct tm_properties_view_api *tm_properties_view_api;
//.. other code 
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
//.. other code 
    tm_properties_view_api = reg->get(TM_PROPERTIES_VIEW_API_NAME);
//.. other code 
} 
```

Now we can use and implement the path opening function. Let us look at its [signature](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_view_api.ui_open_path()) first:

`float (*ui_open_path)(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, const char *name, const char *tooltip, tm_tt_id_t object, uint32_t property, const char *extensions, const char *description, bool *picked)`

 *Function Arguments:*

| **Argument**      | **Data Type**                                                | **Description**                                              |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1 (`args`)        | [tm_properties_ui_args_t](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_ui_args_t) | A bundled type of important information. For example this is the way you would retrieve your UI instance as well as your `uistyle` instance. For more information check the [documentation](https://ourmachinery.com//apidoc/plugins/editor_views/properties.h.html#structtm_properties_ui_args_t). |
| 2 (`item_rect`)   | [tm_rect_t](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_rect_t) | The UI rectangular of the current item. This can be manipulated in x,y as well as w and h as long as the correct y value is being returned. |
| 3 (`n`ame)        | `const char*`                                                | This is the name the Properties tab will display as the title in front of the text field. |
| 4 (`t`ooltip)     | `const char*`                                                | Extra information if needed. (Optional)                      |
| 5 (object)        | [tm_tt_id_t](https://ourmachinery.com//apidoc/foundation/api_types.h.html#structtm_tt_id_t) | The truth object id of the current object. Can be used to read information of. |
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
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER},
    };
```

The index is 0 there for we are no ready to implement the function:


```c
//custom ui
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    // -- code
    bool picked = false;
    item_rect.y = tm_properties_view_api->ui_open_path(args, item_rect, "Imported Path", "Path that the text file was imported from.", object, 0, "txt", "text files", &picked);
    if (picked)
    {
        // import...
    }
    return item_rect.y;
}
```

Remembering all of those indices is quite cucumbersome! Therefore, it is better to define an enum in our header file. Define an `enum` for each property `TM_TT_PROP__[NAME_OF_TYPE]__[NAME_OF_PROPERTY]`

```c
#pragma once
#include <foundation/api_types.h>
//... more code
#define TM_TT_TYPE__MY_ASSET "tm_my_asset"
#define TM_TT_TYPE_HASH__MY_ASSET TM_STATIC_HASH("tm_my_asset", 0x1e12ba1f91b99960ULL)

enum {
    TM_TT_PROP__MY_ASSET__FILE,
    TM_TT_PROP__MY_ASSET__DATA,
}
```

(`txt.h`)

When we compiled this we can test it in the engine, just by adding a new text file click on the Import Path:

![](https://paper-attachments.dropbox.com/s_892FB4725BEE1D4E7D7CCEA6A89558987964DFF4B0524E03B4E0F6FFCF6E0FED_1609931496164_image.png)


The next step is using the OS API to load a file from the disc and store it in the buffer. This process works after the same principle as adding the properties view API. 

The OS API ([tm_os_api](https://ourmachinery.com//apidoc/foundation/os.h.html#structtm_os_api)) lives in the `os.h` and has a member called [file_io](https://ourmachinery.com//apidoc/foundation/os.h.html#structtm_os_file_io_api), allowing access to the `tm_os_file_io_api`. With this API, we can read a file. The following example code shows how reading the file and storing it in a buffer could look like in this case. 


```c
//other includes
#include <foundation/os.h>
#include <foundation/buffer.h>
//.. other code
//custom ui
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    tm_the_truth_o *tt = args->tt;
    bool picked = false;
    item_rect.y = tm_properties_view_api->ui_open_path(args, item_rect, TM_LOCALIZE_LATER("Import Path"), TM_LOCALIZE_LATER("Path that the text file was imported from."), object, TM_TT_PROP__MY_ASSET__FILE, "txt", "text files", &picked);
    if (picked)
    {
        const char *file = tm_the_truth_api->get_string(tt, tm_tt_read(tt, object), TM_TT_PROP__MY_ASSET__FILE);

        tm_file_stat_t stat = tm_os_api->file_system->stat(file);

        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);

        tm_file_o f = tm_os_api->file_io->open_input(file);
        tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);

        const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
        tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, object);
        tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id); // 1 = data property index.
        tm_the_truth_api->commit(tt, asset_obj, TM_TT_NO_UNDO_SCOPE);
    }
    return item_rect.y;
}
```

First, we need to read out the file path from our The Truth object. After that, we can create the buffer we want to add to our *data* property (index 1 or `TM_TT_PROP___MY_ASSET__DATA`). 
The buffers live in the `buffer.h`. We create the buffer via The Truth, and it also owns the memory. We are using the [file_system API](https://ourmachinery.com//apidoc/foundation/os.h.html#structtm_os_file_system_api) to get the size of the text file. We need to know how big the file is to understand how big the buffer should be. 

> Note: We should also check if the file exists. It has been left out because we just picked the file. 

Then we are reading the file from the disc and store its content in the allocated buffer. The next step is to add the buffer to the Truth buffers via the [buffers->add(buffers->inst, buffer, stat.size, 0);](https://ourmachinery.com//apidoc/foundation/buffer.h.html#structtm_buffers_i.add()) call. It adds a buffer containing the specified data of size. It returns an ID identifying the new buffer. For more information, read [here](https://ourmachinery.com//apidoc/foundation/buffer.h.html#structtm_buffers_i.add()).

Now we need to ask the Truth to give us a writeable object. Objects from the Truth are immutable in their default state and can only be made mutable by asking explicitly for a writable object.
This happens via the [tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, object);](https://ourmachinery.com//apidoc/foundation/the_truth.h.html#structtm_the_truth_api.write()) call.

With the writeable object, we can set the buffer, and then we can commit the changes to the Truth itself.

This iteration is the first, but the issue with it is that we cannot import or drag and drop a .txt file into the Engine. We will tackle this issue in the [next part](#).



## What is next?

The next part will refactor the current code and show you how to make your code and asset more useful by showing you how to program an importer.

[Part 3](#)

## Full example source code

`txt.h`

```c
#pragma once
#include <foundation/api_types.h>
//... more code
#define TM_TT_TYPE__MY_ASSET "tm_my_asset"
#define TM_TT_TYPE_HASH__MY_ASSET TM_STATIC_HASH("tm_my_asset", 0x1e12ba1f91b99960ULL)

enum {
    TM_TT_PROP__MY_ASSET__FILE,
    TM_TT_PROP__MY_ASSET__DATA,
};
```

`txt.c`

```c
// -- api's
static struct tm_the_truth_api *tm_the_truth_api;
static struct tm_properties_view_api *tm_properties_view_api;
static struct tm_os_api *tm_os_api;
// -- inlcudes
#include <foundation/api_registry.h>
#include <foundation/the_truth.h>
#include <foundation/undo.h>
#include <foundation/the_truth_assets.h>
#include <foundation/localizer.h>
#include <foundation/macros.h>
#include <foundation/os.h>
#include <foundation/buffer.h>

#include <plugins/editor_views/asset_browser.h>
#include <plugins/editor_views/properties.h>

#include "txt.h"

//custom ui
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    tm_the_truth_o *tt = args->tt;
    bool picked = false;
    item_rect.y = tm_properties_view_api->ui_open_path(args, item_rect, TM_LOCALIZE_LATER("Import Path"), TM_LOCALIZE_LATER("Path that the text file was imported from."), object, TM_TT_PROP__MY_ASSET__FILE, "txt", "text files", &picked);
    if (picked)
    {
        const char *file = tm_the_truth_api->get_string(tt, tm_tt_read(tt, object), TM_TT_PROP__MY_ASSET__FILE);
        tm_file_stat_t stat = tm_os_api->file_system->stat(file);
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(file);
        tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
        const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
        tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, object);
        tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id);
        tm_the_truth_api->commit(tt, asset_obj, TM_TT_NO_UNDO_SCOPE);
    }
    return item_rect.y;
}
// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        {"import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING},
        {"data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER},
    };
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_ASSET, my_asset_properties, TM_ARRAY_COUNT(my_asset_properties));
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "txt");
    static tm_properties_aspect_i properties_aspect = {
        .custom_ui = properties__custom_ui,
    };
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__PROPERTIES, &properties_aspect);
}
// -- asset browser regsiter interface
static tm_tt_id_t asset_browser_create(struct tm_asset_browser_create_asset_o *inst, tm_the_truth_o *tt, tm_tt_undo_scope_t undo_scope)
{
    const tm_tt_type_t type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
    return tm_the_truth_api->create_object_of_type(tt, type, undo_scope);
}
static tm_asset_browser_create_asset_i asset_browser_create_my_asset = {
    .menu_name = TM_LOCALIZE_LATER("New Text File"),
    .asset_name = TM_LOCALIZE_LATER("New Text File"),
    .create = asset_browser_create,
};
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
    tm_properties_view_api = reg->get(TM_PROPERTIES_VIEW_API_NAME);
    tm_os_api = reg->get(TM_OS_API_NAME);
    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
    tm_add_or_remove_implementation(reg, load, TM_ASSET_BROWSER_CREATE_ASSET_INTERFACE_NAME, &asset_browser_create_my_asset);
}
```






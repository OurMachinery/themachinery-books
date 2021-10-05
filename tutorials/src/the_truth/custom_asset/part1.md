# Create a custom asset part 1

This walkthrough shows you how to add a custom asset to the Engine. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide]({{the_machinery_book}}extending_the_machinery/the_plugin_system.html). The goal for this walkthrough is to write a text file asset.

In the parts 1 - 3 we will cover the following topics:

- How to create your asset
- How to associate data with your asset
- How to add a custom UI to your asset
- How to create your importer

This part will cover the following topics:

- What to think of in advance?
- Creating an essential asset The Truth type
- Being able to add the asset to the asset browser
  - Via context Menu
  - Via code

The next part will explore how to store more complex data in an asset file and how to get this data back into the Engine.

> You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* auto-gen TOC;
{:toc}

## **First step:** What kind of asset do we want to create?

Sometimes it is needed to add a custom asset to the Engine to support different asset types which are not supported yet. The first step is that we need to decide what our asset shall represent. In this case, it will be a text file. Those decisions have some influence on the details of the implementation. How ever the steps discussed below are the same in any case.


## Creating an asset The Truth Type

The Engine needs to know that there shall be a new asset type. That is why we need to register a new Truth type. Those steps are the same for every truth type, be it an asset or not.

We need to define a globally accessible definition for the name of the type and its hash value. The usual place for this is a header file.

Example Header file: `my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.h}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`, mode information here.)

Now we need to define the layout of our asset type. We should always do this during plugin load. (`tm_load_plugin`) 
During this call we need to register a function to the `tm_the_truth_create_types_i` interface. 
This function is typically called `create_truth_types`, but its name can be arbitrary.


> **Note:** An interface is an abstract structure that maps a struct (the interface) to a hash value/name. It allows for customization points. In The Machinery, the Engine uses this extensively.

Example `tm_load_plugin` function for `my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:35:38}}
}
```

After we did this, let us implement the actual function. First, we need to create a Truth type:
 We use the function `tm_the_truth_api->create_object_type(tm_the_truth_o *tt, const char *name, const tm_the_truth_property_definition_t *properties, uint32_t num_properties);` . This one will register in the Truth a new type with the name and the properties we give the type. 

At this point, we have a normal The Truth type. But we wanted to create an asset! 

#### What is the difference between Truth Type and Asset?

An asset is just a normal truth type. The structure of an asset in the truth is defined in the `foundation/the_truth_assets.h`. An asset itself is, therefore, nothing else than a wrapper around our actual asset. It provides a generic interface to provide some standard information.

The structure of an asset type looks like this:


```c
enum {
    // Name of the asset.
    TM_TT_PROP__ASSET__NAME, // string
    // Directory where the asset resides. For top-level assets, this is `NULL`.
    TM_TT_PROP__ASSET__DIRECTORY, // reference [[TM_TT_TYPE__ASSET_DIRECTORY]]
    // Labels applied to this asset.
    TM_TT_PROP__ASSET__UUID_LABELS, // subobject_set(UINT64_T) storing the UUID of the associated label.
    // Subobject with the actual data of the asset. The type of this subobject depends on the type
    // of data storedin this asset.
    TM_TT_PROP__ASSET__OBJECT, // subobject(*)
    // Thumbnail image associated with asset
    TM_TT_PROP__ASSET__THUMBNAIL, // buffer
};
```

The truth type of the text file we just created will live as a subobject of the Asset Truth Type in the property field: `TM_TT_PROP__ASSET__OBJECT`.

Let us move on and go back and finish the definition of our type. Let us add a file extension to our type. All we need to do is add an aspect of type `TM_TT_ASPECT__FILE_EXTENSION` to our Truth Type. You can find it in the following header file `foundation/the_truth_assets.h`.

> **Note:** The Machinery will automatically prefix your file extension with **tm_**

In code, this looks as follows:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:15:20}}
```

We create a type of name `TM_TT_TYPE__MY_ASSET` with no properties and a file extension my_asset (`.tm_my_asset` in your explorer). 


## Making the Asset Browser able to create it

Now that there is a basic asset type, you might want the asset browser to create it via the `New Asset` context menu. All you need to do is register the asset to the `tm_asset_browser_create_asset_i` interface. This interface requires an implementation of the type `tm_asset_browser_create_asset_i`:


```c
typedef struct tm_asset_browser_create_asset_i
{
    struct tm_asset_browser_create_asset_o *inst;
    // TM_LOCALIZE_LATER() name of menu option to display for creating the asset (e.g. "New
    // Entity").
    const char *menu_name;
    // TM_LOCALIZE_LATER() name of the newly created asset (e.g. "New Entity");
    const char *asset_name;
    // Create callback, should return The Truth ID for the newly created asset.
    tm_tt_id_t (*create)(struct tm_asset_browser_create_asset_o *inst, struct tm_the_truth_o *tt, tm_tt_undo_scope_t undo_scope);
} tm_asset_browser_create_asset_i;
```

Source: `plugins/editor_views/asset_browser.h`

For our basic type, this interface can be defined as follows:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:22:32}}
```

What is happening?

- In this case, the function `asset_browser_create` creates the object of our type. Here we could do more complex things if the asset were more complicated. 
- The *menu name* is for the context menu, while the *asset name* functions as the default asset name. 

Now we register our code to the interface. We do this also in the load plugin function.

Example `tm_load_plugin` function for `my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:35:40}}
```

When we open the Engine, we can open the Asset Browser and create our asset:

![](https://paper-attachments.dropbox.com/s_080D43F0A98EB2BE6BBB6D719C7B3B910F38D78674006103833AED0070469AD4_1609883533160_image.png)

What happens is not existing! But we are getting there! Check out the [next part](#) for more complex and existing actions.

## What is next?

The next part will refactor the current code and show you how to make your code and asset more useful by implementing the action asset.

[Part 2]({{base_url}}/the_truth/custom_asset/part2.html)



## Appendix: Adding an asset via code to the Asset Browser

Sometimes it is necessary to create an asset via code. The Asset Browser plugin provides a solution for this the `tm_asset_browser_add_asset_api`. With this API assets can be created and added to the current project.

To add an asset to the asset browser a few steps are needed. 

1. First, we need to pick the correct type. We need to request it from the truth via the type hash (in this example, `TM_TT_TYPE_HASH__MY_ASSET`). 
2. Secondly, we should create an object of the correct type. 
3. Then we can request the asset browser API if the API not globally accessible.

> If we already requested the API, we do not need to do this step and can use the already defined instance of the API.

4. We need to create a undo scope. (We could also use `TM_TT_NO_UNDO_SCOPE`) but its not recommended!
5. Then, we should decide if we should highlight the new asset in the Asset Browser. (`should_select=true`) If that's needed, an instance of the current UI is required. 
6. Then, the magic can happen and we can call the function `add` of the `tm_asset_browser_add_asset_api` 

The following code example will demonstrate how to add my_asset via code to the current project.

```c
// ... other includes
#include <foundation/the_truth.h>
#include <foundation/undo.h>

#include <plugins/editor_views/asset_browser.h>

#include "my_asset.h"
//... other code

static void add_my_asset_to_project(tm_the_truth_o *tt, struct tm_ui_o *ui, const char *asset_name, tm_tt_id_t target_dir)
{
    const tm_tt_type_t my_asset_type_id = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
    const tm_tt_id_t asset_id = tm_the_truth_api->create_object_of_type(tt, my_asset_type_id, TM_TT_NO_UNDO_SCOPE);
    struct tm_asset_browser_add_asset_api *add_asset = tm_get_api(tm_global_api_registry, tm_asset_browser_add_asset_api);
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Add My Asset to Project"));
    bool should_select = true;
    // we do not have any asset label therefore we do not need to pass them thats why the last
    // 2 arguments are 0 and 0!
    add_asset->add(add_asset->inst, target_dir, asset_id, asset_name, undo_scope, should_select, ui, 0, 0);
}
```



## Full example of basic asset

`my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.h}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`)

`my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c}}
```


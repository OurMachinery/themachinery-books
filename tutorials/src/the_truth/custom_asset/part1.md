# Create a Custom Asset Type: Part 1

This part will cover the following topics:

- What to think of in advance?
- Creating a The Truth type
- Exposing the asset to the asset browser
  - Via the context menu
  - Via code

The next part will explore how to store more complex data in an asset and how to get this data back into the Engine.

> You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* auto-gen TOC;
{:toc}

## **First Step:** What Kind of Asset Do We Want to Create?

The Machinery comes with some predefined asset types, but these types might not cover all types of data you want to represent in the engine. Luckily, you can extend the asset types supported by using plugins.

In this example we will extend the engine with support for text file assets. The steps shown below will be similar regardless of what kind of data representation you are creating.


## Creating a Type in The Truth

In The Machinery, all data is represented in The Truth. To add a new kind of data, we need to register a new Truth Type.

> **Note** that not all Truth types are Asset types. An Asset type is a Truth type that can exist as an independent object in the Asset Browser. For example, Vector3 is a Truth type representing an `(x, y, z)` vector, but it is not an asset type, because we can't create a Vector3 asset in the Asset Browser. A Vector3 is always a subobject of some other asset (such as an Entity).

A Truth type is defined by a name (which must be unique) and a list of properties. Properties are identified by their indices and each property has a specific type.

Typically, we put the type name, the hashed name and the list of properties in the header file, so that they can be accessed by other parts of the code. (Though if you have a Truth type that will only be used internally, in your own code, you could put it in the `.c` file.)

Example header file `my_asset.h`:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.h}}
```

Do not forget to run `hash.exe` whenever you use `TM_STATIC_HASH()` in your code. This will ensure that the correct value for the hash is cached in the macro.

If you are creating a complicated type it may have subobjects that themselves have custom types.

To make The Truth aware of this custom type we must register it with The Truth. This is done with a callback function that is typically called `create_truth_types()` or `truth__create_types()`, but the name doesn't really matter. We register this callback function under the `tm_the_truth_create_types_i` interface. That way, The Truth will now to call this function to register all the types whenever a new Truth object is created (this happens for example when you open a project using **File → Open**).


> **Note:** Interfaces and APIs are the main mechanisms for extending The Machinery. The difference is that an API only has a single implementation (there is only one `tm_the_truth_api` for instance), whereas there can be many implementations of an interface. Each plugin that creates new truth type will implement the `tm_the_truth_create_types_i` interface.

Example `tm_load_plugin` function for `my_asset.c`:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:35:38}}
}
```

Now we can implement the actual `create_truth_types()` function. We use `tm_the_truth_api->create_object_type()` to create a Truth type with a specified name and properties.

At this point, we have a newThe Truth type. But it's not yet an asset! 

#### What Is the Difference between a Truth Type and an Asset?

An *Asset* in The Machinery is just a Truth object of the type `TM_TT_TYPE__ASSET`. 

It looks like this:


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
    TM_TT_PROP__ASSET__THUMBNAIL, // subobject(TM_TT_TYPE__ASSET_THUMBNAIL)
};
```

The most important part here is `TM_TT_PROP__ASSET__OBJECT`. This is the actual object that the asset contains. For an Entity asset, this will be an object of type `TM_TT_TYPE__ENTITY`, etc.

So the *Asset* object is just a wrapper that adds some metadata to the actual data object (found in `TM_TT_PROP__ASSET__OBJECT`). This is where our new ` TM_TT_TYPE__MY_ASSET` will be found.

Truth types that are used as assets need to define an *extension*. This be shown in the Asset Browser. For example, entities have the extension `"entity"`, so an entity named `world` is shown in the Asset Browser as `world.entity`. The extension is also used when the project is saved to disk, but in this case it will automatically be prefixed with `tm_`. So if you look at the project on disk, `world.entity` will be saved as `world.tm_entity`. The reason for this is to be able to easily tell The Machinery files from other disk files.

We set the extension by adding a Truth aspect of type `TM_TT_ASPECT__FILE_EXTENSION` to our type

Here's the full code for creating the type and registering the extension:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:15:20}}
```


## Exposing the Type to the Asset Browser

Even though we now have a Truth Type as well as an Extension, we still don't have any way of creating objects of this type in the Asset Browser. To enable that, there's another interface we have to implement: `tm_asset_browser_create_asset_i`:


```c
// Interface that can be implemented to make it possible to create assets in the Asset Browser,
// using the **New** context menu.
typedef struct tm_asset_browser_create_asset_i
{
    struct tm_asset_browser_create_asset_o *inst;

    // [[TM_LOCALIZE_LATER()]] name of menu option to display for creating the asset (e.g. "New
    // Entity").
    const char *menu_name;

    // [[TM_LOCALIZE_LATER()]] name of the newly created asset (e.g. "New Entity");
    const char *asset_name;

    // Create callback, should return The Truth ID for the newly created asset.
    tm_tt_id_t (*create)(struct tm_asset_browser_create_asset_o *inst, struct tm_the_truth_o *tt,
        tm_tt_undo_scope_t undo_scope);
} tm_asset_browser_create_asset_i;
```

Source: `plugins/editor_views/asset_browser.h`

If you implement this interface, your Truth type will appear in the **New →** context menu of the asset browser and you can create new objects of the type from there.

For our basic type, this interface can be defined as follows:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:22:32}}
```

* The `menu_name` specified in the interface is the name that will appear in the **New  →** menu.
* The `asset_name` is the name that will be given to the newly created asset.
* The `asset_browser_create()` function creates the object of our type. If we wanted to, we could do more advanced things here to set up the asset.

This interface is registered by the `tm_load_plugin()` function, just as all the other interfaces:

Example `tm_load_plugin()` function for `my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c:35:40}}
```

The asset can now be created from the Asset Browser:

![](https://paper-attachments.dropbox.com/s_080D43F0A98EB2BE6BBB6D719C7B3B910F38D78674006103833AED0070469AD4_1609883533160_image.png)

So far things are not that exciting. But we are getting there!

## What is next?

In the next part we will refactor code and show how to make the asset more useful by adding some actual data to it.

[Part 2]({{base_url}}/the_truth/custom_asset/part2.html)



## Appendix: Creating an Asset from Code

The Asset Browser lets you create new assets using the UI, but you may also want to create assets from code. You can do this by using the `tm_asset_browser_add_asset_api` provided by the Asset Browser plugin. It lets you create new assets and adds them to the current project.

To create an asset:

1. Create a Truth object of the desired type and add it to the project using `tm_asset_browser_add_asset_api->add()`. 
2. If you want the action to be undoable, you need to create an undo scope for it and add it to the undo stack.
3. If you want the asset to selected in the asset browser, you need to pass *true* for the `should_select` parameter.

The following code example demonstrate how to add an asset of the `TM_TT_TYPE__MY_ASSET` type to the project.

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



## Full Example of Basic Asset

`my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.h}}
```

(Do not forget to run hash.exe when you create a new `TM_STATIC_HASH()`)

`my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_1/txt.c}}
```


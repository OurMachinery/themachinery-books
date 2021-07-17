# Create a custom Truth Type

This walkthrough shows you how to create a type for the Truth. The Truth is our centralized data model for editing data in the Engine. For more details on the system itself, click here: [The Truth]({{base_url}}/the_machinery_book/the_truth/index.html). 

You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide](https://ourmachinery.github.io/themachinery-books//the_machinery_book/extending_the_machinery/the_plugin_system.html). 



We will cover the following topics:

- How to define a Type.
- Type Properties

After this walkthrough you could checkout the ["Create a custom asset"]({{base_url}}/tutorials/the_truth/custom_asset/index.html) tutorial! 



**Table of Content**

* auto-gen TOC;
{:toc}

## Define a Type

A Truth-Type in The Machinery consists out of a name (its identifier) and properties. 



> **Note:** In theory, you could also define a Type without properties.



To add a Type to the system, you need access to the Truth instance. The Engine may have more than one instance of a Truth. 



> **Example:** There is a Project Truth to keep all the project-related settings and an Engine/Application Truth that holds all the application-wide settings.



Generally speaking, you want to define Truth Types at the beginning of the Engine's life cycle. Therefore the designated place is the `tm_load_plugin` function. The Truth has an *interface* to register a truth type creation function: `TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME`. 

This interface expects a function of the signature: `void create_truth_types(tm_the_truth_o *tt)`. Whenever the Engine creates a Truth, it invokes this interface on all loaded plugins, and their types are registered. You do not need to register your Type to the interface if you want to register your Type to a specific Truth.



> **Note:** Mostly this function is called: `create_truth_types`



Let us define a type. To do that, we need to get the `tm_truth_api` first:

```c
// beginning of the source file
static struct tm_the_truth_api *tm_the_truth_api;
#include <foundation/api_registry.h>
#include <foundation/the_truth.h>
// ... other code
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
 tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
}
```



After this, we define our type name once as a constant char define and one hashed version. There are some conventions to keep in mind:

1. The plain text define should start with: `TM_TT_TYPE__`.
2. The hashed define should start with: `TM_TT_TYPE_HASH__`
3. The name may or may not start with `tm_` but the name plain text and the hashed version need to match!



```c
#define TM_TT_TYPE__MY_TYPE "tm_my_type"
#define TM_TT_TYPE_HASH___MY_TYPE TM_STATIC_HASH("tm_my_type", 0xde0e763ccd72b89aULL)
```



> **Tip:** Do not forget to run `hash.exe.` Otherwise, the `TM_STATIC_HASH` macro will cause an error. You can also run `tmbuild --gen-hash`



It is good practice to place the types into a header file so others can use these types as well!  When that is done we can call the `tm_the_truth_api->create_object_type()` to create the actual type. It will return a `tm_tt_type_t` which is the identifier of our type. The `tm_tt_id_t` will also refer to the type here! 

The function expects:

| Argument                                               | Description                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| `tm_the_truth_o *tt`                                   | The Truth instance. This function will add the type to this instance |
| `const char *name`                                     | The name of the type. It will be hashed internally. Therefore the hash value of `TM_TT_TYPE__`  and `TM_TT_TYPE_HASH___` should match!  *If a type with `name` already exists, that type is returned. Different types with the same are not supported!* |
| `const tm_the_truth_property_definition_t *properties` | The definitions of the properties of the type.               |
| ` uint32_t num_properties`                             | The number of properties. Should match `properties`          |



The home of this function should be our `void create_truth_types(tm_the_truth_o *tt)` . We need to add this one to our source file. After this we add the call to `create_object_type` to it. Remember that we have no properties yet, and our call would look like this:



```c
void create_truth_types(tm_the_truth_o *tt){
	tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_TYPE, 0, 0);
}
```





The last step is to tell the plugin system that we intend to register our `register_truth_type()`.



```c
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
 tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
 tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
}
```



The full source code should look like this:

`my_type.h`

```c
#pragma once
#include <foundation/api_types.h>
#define TM_TT_TYPE__MY_TYPE "tm_my_type"
#define TM_TT_TYPE_HASH___MY_TYPE TM_STATIC_HASH("tm_my_type", 0xde0e763ccd72b89aULL)
```

(Tip: Do not forget to run hash.exe)

`my_type.c`

```c
// beginning of the source file
static struct tm_the_truth_api *tm_the_truth_api;
#include <foundation/api_registry.h>
#include <foundation/the_truth.h>

void create_truth_types(tm_the_truth_o *tt){
	tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_TYPE, 0, 0);
}

TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
 tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
 tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
}
```



After all of this you have registered your type and it could be used. This type is just not really useful without properties.



## About Properties

In The Truth, an Object-Type is made of one or multiple properties. Properties can represent the basic types:

- `bool`, `string`, `float`, `UINT64`, `UNIT32`, `double`, ``buffer`
- `subobject` - An object that lives within this property 
- `reference` - A reference to another object
- `subobject set` - A Set of subobjects
- `reference set` - A Set of references.

*What is the difference between a reference and a subobject?*

To see the difference, consider how [clone_object()]({{docs}}foundation/the_truth.h.html#structtm_the_truth_api.clone_object()) works in both cases:

- When you clone an object with references, the clone will reference the same objects as the original, i.e. they now have multiple references to them.
- When you clone an object with subobjects, all the subobjects will be cloned too. After the clone operation, there is no link between the object's subobjects and the clone's subobjects.

An arbitrary number of objects can reference the same object, but a subobject only has a single owner.

When you destroy an object, any references to that object become NIL references — i.e., they no longer refer to anything.

When you destroy an object that has subobjects, all the subobjects are destroyed with it.



>  **Note:** For more information please check: [The API Documentation]({{docs}}foundation/the_truth.h.html#the_truth.h) 



## Adding properties

Let us add some properties to our Type! As you remember, when we created the Type, the function `create_object_type()` required a pointer to the definition of properties. You can define properties via the `tm_the_truth_property_definition_t` struct.

```c
typedef struct tm_the_truth_property_definition_t
{
    // Name of the property, e.g. "cast_shadows".
    //
    // This name is used both for serialization and for the UI of editing the property. When
    // displayed in the UI, the name will be automatically capitalized (e.g. "Cast Shadows").
    //
    // The name shouldn't be longer than [[TM_THE_TRUTH_PROPERTY_NAME_LENGTH]] characters.
    const char *name;

    // [[enum tm_the_truth_property_type]] type of the property.
    uint32_t type;

    // [[enum tm_the_truth_editor]] enum defining what editor should be used for editing the property.
    uint32_t editor;

    // Editor specific settings.
    union
    {
        tm_the_truth_editor_enum_t enum_editor;
        tm_the_truth_editor_string_open_path_t string_open_path_editor;
        tm_the_truth_editor_string_save_path_t string_save_path_editor;
    };

    // For properties referring to other objects (references & subobjects), specifies the type of
    // objects that they can refer to. A value of [[TM_TT_TYPE__ANYTHING]] is used for an object
    // that can refer to anything.
    //
    // Note: We currently don't have any system for representing "interfaces" or groups of types.
    // I.e. you can't say "I want this to reference any type that inherits from the GRAPH_NODE_TYPE,
    // but no other types." We may add this in the future.
    tm_strhash_t type_hash;

    // Specifies that the property is allowed to refer to other types than the `type_hash`.
    //
    // !!! NOTE: Note
    //     This flag should not be used going forward. Instead, if a property can refer to multiple
    //     types, you should use a `type_hash` of [[TM_TT_TYPE__ANYTHING]]. It is provided for
    //     compatibility purposes, because some object types have a `type_hash` specified but
    //     store subobjects of other types. We cannot simply change the `type_hash` of those objects
    //     to [[TM_TT_TYPE__ANYTHING]], because there may be saved data that has serialized versions
    //     of those objects that omits the object type (if it is `type_hash`). We can't deserialize
    //     those objects if we don't know the `type_hash` of the type.
    bool allow_other_types;
    TM_PAD(7);

    // For buffer properties, the extension (if any) used to represent the buffer type. This can
    // either be hard-coded in `buffer_extension`, or computed by the `buffer_extension_f()`
    // callback (set the unused option to `NULL`).
    const char *buffer_extension;
    const char *(*buffer_extension_f)(const tm_the_truth_o *tt, tm_tt_id_t object, uint32_t property);

    // Tooltip used to describe the property in more detail. The tooltip text will be displayed in
    // the property editor when the property is hovered over.
    //
    // The tooltip should be registered using [[TM_LOCALIZE_LATER()]]. It will be dynamically
    // localized to the current interface language with [[TM_LOCALIZE_DYNAMIC()]] before being
    // displayed in the UI.
    const char *tooltip;

    // If *true*, this property will be skipped during serialization.
    bool not_serialized;
    TM_PAD(7);

    // If specified, this will be used instead of `name` for the UI.
    const char *ui_name;
} tm_the_truth_property_definition_t;
```

([API Documentation]({{docs}}foundation/the_truth.h.html#structtm_the_truth_property_definition_t))



Within our `create_truth_types` we create a array of type `tm_the_truth_property_definition_t`. For this example, we define the properties of type bool and string.

```c
// include `macros.h` to access TM_ARRAY_COUNT for convinace:
#include <foundation/macros.h>
//..code
void create_truth_types(tm_the_truth_o *tt){
    tm_the_truth_property_definition_t properties[] = {
        { "my_bool", TM_THE_TRUTH_PROPERTY_TYPE_BOOL },
        { "my_string", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
    };
	tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_TYPE, properties,TM_ARRAY_COUNT(properties);
}
```



That is all we need to do to define properties for our Type! Also thanks to our automatic "reflection" system you do not have to worry about providing a UI for the type. The Properties View will automatically provide a UI for this type.

## What is next?

You can find more in depth and practical tutorials in the [tutorial book]({{base_url}}tutorials/the_truth/index.html)

# Create a custom Truth Type

This walkthrough shows you how to create a type for the Truth. The Truth is our centralized data model for editing data in the Engine. For more details on the system itself, click here: [The Truth]({{base_url}}the_truth/index.html). 

You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide]({{base_url}}extending_the_machinery/the_plugin_system.html). 



We will cover the following topics:

- How to define a Type.
- Type Properties

After this walkthrough you could check out the ["Create a custom asset"]({{base_url}}tutorials/the_truth/custom_asset/index.html) tutorial! 



**Table of Content**

* auto-gen TOC;
{:toc}

## Define a Type

A Truth-Type in The Machinery consists out of a name (its identifier) and properties. 



> **Note:** In theory, you could also define a Type without properties.



To add a Type to the system, you need access to the Truth instance. The Engine may have more than one instance of a Truth. 



> **Example:** There is a Project Truth to keep all the project-related settings and an Engine/Application Truth that holds all the application-wide settings.



Generally speaking, you want to define Truth Types at the beginning of the Engine's life cycle. Therefore the designated place is the `tm_load_plugin` function. The Truth has an *interface* to register a truth type creation function: `tm_the_truth_create_types_i`. 

This interface expects a function of the signature: `void create_truth_types(tm_the_truth_o *tt)`. Whenever the Engine creates a Truth, it invokes this interface on all loaded plugins, and their types are registered. You do not need to register your Type to the interface if you want to register your Type to a specific Truth.



> **Note:** Mostly this function is called: `create_truth_types`



Let us define a type. To do that, we need to get the `tm_truth_api` first:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_truth_types.c,includes)}}
// ... other code
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_truth_types.c,tm_load_plugin)}}
```

After this, we define our type name once as a constant char define and one hashed version. There are some conventions to keep in mind:

1. The plain text define should start with: `TM_TT_TYPE__`.
2. The hashed define should start with: `TM_TT_TYPE_HASH__`
3. The name may or may not start with `tm_` but the name plain text and the hashed version need to match!



```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/my_type.h)}}
```



> **Tip:** Do not forget to run `hash.exe.` Otherwise, the `TM_STATIC_HASH` macro will cause an error. You can also run `tmbuild --gen-hash`



It is good practice to place the types into a header file so others can use these types as well!  When that is done we can call the `tm_the_truth_api->create_object_type()` to create the actual type. It will return a `tm_tt_type_t` which is the identifier of our type. The `tm_tt_id_t` will also refer to the type here! 

The function expects:

| Argument                                               | Description                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| `tm_the_truth_o *tt`                                   | The Truth instance. This function will add the type to this instance |
| `const char *name`                                     | The name of the type. It will be hashed internally. Therefore the hash value of `TM_TT_TYPE__`  and `TM_TT_TYPE_HASH___` should match!  *If a type with `name` already exists, that type is returned. Different types with the same `name` are not supported!* |
| `const tm_the_truth_property_definition_t *properties` | The definitions of the properties of the type.               |
| ` uint32_t num_properties`                             | The number of properties. Should match `properties`          |



The home of this function should be our `void create_truth_types(tm_the_truth_o *tt)` . We need to add this one to our source file. After this we add the call to `create_object_type` to it. Remember that we have no properties yet, and our call would look like this:



```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_empty_type.c,create_object_type)}}
```



The last step is to tell the plugin system that we intend to register our `register_truth_type()`.



```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_empty_type.c,load_plugin)}}
```



The full source code should look like this:

`my_type.h`

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/my_type.h)}}
```

(Tip: Do not forget to run hash.exe)

`my_type.c`

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_empty_type.c)}}
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
{{$include env.TM_SDK_DIR/foundation/the_truth.h:407:473}}
```

([API Documentation]({{docs}}foundation/the_truth.h.html#structtm_the_truth_property_definition_t))



Within our `create_truth_types` we create an array of type `tm_the_truth_property_definition_t`. For this example, we define the properties of type bool and string.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_truth_types.c)}}
```



That is all we need to do to define properties for our Type! Also thanks to our automatic "reflection" system you do not have to worry about providing a UI for the type. The Properties View will automatically provide a UI for this type.

## What is next?

You can find more in depth and practical tutorials in the [tutorial chapter]({{base_url}}/tutorials/the_truth/index.html)

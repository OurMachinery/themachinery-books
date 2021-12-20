# Provide a Custom Datatype to the Entity Graph

This walkthrough shows you how to extend the Entity Graph with a custom data type

- How to provide a custom compile step for your own data type.



## Data Type Overview of the Entity Graph

The following overview lists all types that are supported by the engine build in with the `Entity Graph Component`.  If you wanted to support your own data type you need to implement the `tm_graph_component_compile_data_i` interface manually.

| Truth Type                                        |
| ------------------------------------------------- |
| `TM_TT_TYPE_HASH__BOOL`                           |
| `TM_TT_TYPE_HASH__UINT32_T`                       |
| `TM_TT_TYPE_HASH__UINT64_T`                       |
| `TM_TT_TYPE_HASH__FLOAT`                          |
| `TM_TT_TYPE_HASH__DOUBLE`                         |
| `TM_TT_TYPE_HASH__VEC2`                           |
| `TM_TT_TYPE_HASH__VEC3`                           |
| `TM_TT_TYPE_HASH__VEC4`                           |
| `TM_TT_TYPE_HASH__POSITION`                       |
| `TM_TT_TYPE_HASH__ROTATION`                       |
| `TM_TT_TYPE_HASH__SCALE`                          |
| `TM_TT_TYPE_HASH__COLOR_RGB`                      |
| `TM_TT_TYPE_HASH__RECT`                           |
| `TM_TT_TYPE_HASH__STRING`                         |
| `TM_TT_TYPE_HASH__STRING_HASH`                    |
| `TM_TT_TYPE_HASH__KEYBOARD_ITEM`                  |
| `TM_TT_TYPE_HASH__MOUSE_BUTTON`                   |
| `TM_TT_TYPE_HASH__ENTITY_ASSET_REFERENCE`         |
| `TM_TT_TYPE_HASH__LOCAL_ENTITY_ASSET_REFERENCE`   |
| `TM_TT_TYPE_HASH__CREATION_GRAPH_ASSET_REFERENCE` |
| `TM_TT_TYPE_HASH__EASING`                         |
| `TM_TT_TYPE_HASH__LOOP_TYPE`                      |
| `TM_TT_TYPE_HASH__COMPONENT_PROPERTY_FLOAT`       |
| `TM_TT_TYPE_HASH__COMPONENT_PROPERTY_VEC2`        |
| `TM_TT_TYPE_HASH__COMPONENT_PROPERTY_VEC3`        |
| `TM_TT_TYPE_HASH__COMPONENT_PROPERTY_VEC4`        |
| `TM_TT_TYPE_HASH__COMPONENT_PROPERTY_ANY`         |

## Implement the `tm_graph_component_compile_data_i`

When you need to implement your own type you need to implement the `tm_graph_component_compile_data_i` interface. This interface lives in the `graph_component.h` header file. This header file is part of the `graph_interpreter` plugin.

The interface is just a function typedef of the following signature:

```c
{{$include {TM_SDK_DIR}/plugins/graph_interpreter/graph_component.h:66}}
```



### How will the graph interpreter use this function?

The Graph Interpreter will call this function when ever it compiles data to a graph before the graph is initialized the first time. The function should return true if it compiled data to a wire otherwise it should return false and the graph interpreter will keep looking for the correct compile function.

The function provided multiple arguments but the following 2 arguments are the most important one:

| Name                         | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| ` tm_tt_id_t data_id`        | The data object the interpreter tries to compile to a wire but does not know how to. |
| ` tm_strhash_t to_type_hash` | The data the wire expects.                                   |

For example in the Animation State Machine `TM_TT_TYPE_HASH__ASM_EVENT_REFERENCE` are objects that contain a string hash (`TM_TT_PROP__ASM_EVENT__NAME`) that the animation state machine needs in order to execute a certain event. The list above shows that there is no translation from a `TM_TT_TYPE_HASH__ASM_EVENT_REFERENCE` to a wire. Therefore we need to provide our own function for this. The animation state machine plugin provides a compilation function for this. 

The plugin knows that a `TM_TT_TYPE_HASH__ASM_EVENT_REFERENCE` is nothing else then a `TM_TT_TYPE_HASH__STRING_HASH` at the end. This means we need to do the following steps:

1. We need to figure out what kind of type is in `data_id`
2. We need to compare the type of `data_id` with the `to_type_hash` being equal to `TM_TT_TYPE_HASH__STRING_HASH`
3. perform our actual translation

Let us begin with figuring out the data type of `data_id`:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c,data_id)}}
```

We also need to get a read object of the `data_id` to read the data from it.

The next step is to compare the given data:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c,compare)}}
```

If this is true we move on with our data compilation. Now that we know our object is of type `TM_TT_TYPE_HASH__ASM_EVENT_REFERENCE` we can use the Truth and extract that actual value we care about the `TM_TT_PROP__ASM_EVENT__NAME`

```` c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c,tt_extract)}}
````

After this its time to compile or better write the data to the provided wire. For this we need to use the `tm_graph_interpreter_api` API and its `tm_graph_interpreter_api.write()` function. The function expects the current interpreter and the wire we write to (we have this one as function parameter of the `tm_graph_component_compile_data_i` interface `uint32_t wire`)  as well as the size and the amount. Passing all these information to the write function enables it to allocate memory internally in the interpreters memory stack.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c,data_extract)}}
```

Keep in mind the function is a bit miss leading since it says `write` but what it actually does it just allocates memory for you (if needed) and give you back a writable pointer. At the end we write to the pointer our data and return true.

All together the translation looks like this:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c,translation)}}
```



## Source Code

The entire sample source code:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/gameplay_code/tm_graph_component_compile_data_i.c)}}
```


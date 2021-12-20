## Create an Object

You can create an object of a Truth Type via two steps:

1. You need to obtain the Type from the type hash. We call the `object_type_from_name_hash` to obtain the `tm_tt_type_t`
2. You need to create an Object from that Type. We call `create_object_of_type` to create an object `tm_tt_id_t` . We pass `TM_TT_NO_UNDO_SCOPE` because we do not need an undo scope for our example.

First, we need to have access to a Truth instance. Otherwise, we could not create an object. In this example, we create a function.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_an_object.c,create_my_type_object)}}
```

Wherever we call this function we can then edit and modify the type and add content to it!

The alternative approach is to use the "Quick Object Creation function".

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/create_an_object.c,quick_create_my_type_object)}}
```



> **Note:**  need to pass `-1` to tell the function that we are at the end of the creation process. More info [here]({{docs}}foundation/the_truth.h.html#structtm_the_truth_api.quick_create_object()).



## What is next?

If you want to learn more about how to create your own custom type, follow the ["Custom Truth Type"]({{base_url}}/the_truth/custom_truth_type.html) walkthrough.

# Modify an object

To manipulate an object, you need to have its ID (`tm_tt_id_t`). When you create an object, you should keep its ID around if you intend to edit it later.

**Table of Content**

* auto-gen TOC;
{:toc}

In this example, we have a function that gets an object and the Truth instance of that object.

```c
void modify_my_object(tm_the_truth_o *tt, tm_tt_id_t my_object){
    //...
}
```

>  **Important:** you can only edit an object that is part of the same instance! Hence your `my_object` must be created within this instance of the Truth (`tt`).  



## 1. Make the object writable

To edit an object, we need to make it writeable first. In the default state, objects from the Truth are immutable. The Truth API has a function that is called `write`. When we call it on an object, we make it writable.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:12}}
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:28}}
//...
}
```

## 2. Write to the object.

We need to know what kind of property we want to edit. That is why we always want to define our properties in a Header-File. A good practice is to comment on what kind of data type property contains.

Let us assume our object is of type ``TM_TT_TYPE__RECT``:

```
enum {
    TM_TT_PROP__RECT__X, // float
    TM_TT_PROP__RECT__Y, // float
    TM_TT_PROP__RECT__W, // float
    TM_TT_PROP__RECT__H, // float
};
```

In our example we want to set the width to `100`. The width is stored in `TM_TT_PROP__RECT__W`.

When we know what we want to edit, we call the correct function and change the value.

The function we need to call:

```c
void (*set_float)(tm_the_truth_o *tt, tm_the_truth_object_o *obj, uint32_t property,float value);
```

Let us bring all of this together:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:12}}
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:28:29}}
//..
}
```



## 3. Save the change

In the end, we need to commit our change to the system. In this example we do not care about the undo scope. That is why we provide the `TM_TT_NO_UNDO_SCOPE` define. This means this action is not undoable.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:11}}
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:36:39}}
```

If we wanted to provide a undo scope we need to create one:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:12}}
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:29:33}}
```

Now this action can be reverted in the Editor.



## 4. Get a value

Instead of changing the value  of width to 100 we can also increment it by 100! All we need to do is get the value first of the Truth Object and add 100 to it. To access a property we need to use the macro `tm_tt_read`. This will give us a immutable (read only) pointer to the underlaying object. This allows us to read the data from it.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:12}}
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:19:25}}
```

> **Note:** If we had a lot of read actions we should only call `tm_tt_read` once and store the result in a  `const tm_the_truth_object_o*` variable and reuse.



## 5. Make the code robust

To ensure we are actually handling the right type we should check this at the beginning of our function. If the type is not correct we should early out.

All we need to do is compare the `tm_tt_type_t`'s of our types. Therefore we need to obtain the type id from the object id and from our expected type. From a `tm_tt_id_t` we can obtain the type by calling `tm_tt_type()` on them. `tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_TYPE);` will give us back the object type from a given hash. After that we can do our comparison.

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/truth/modify_object.c:10:25}}
```


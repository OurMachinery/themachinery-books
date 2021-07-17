# Access values

The truth objects (`tm_tt_id_t`) are immutable objects unless you explicitly make them writable. Therefore we do not be afraid of accidently changing a value when reading from a object property.

To read from a object property we need access to the correct Truth Instance as well as to a object id.  We also need to know what kind of property we want to access. That is why we always want to define our properties in a Header-File. Which allows us and others to find quickly our type definitions. A good practice is to comment on what kind of data type property contains.

Let us assume our object is of type ``TM_TT_TYPE__RECT``:

```
enum {
    TM_TT_PROP__RECT__X, // float
    TM_TT_PROP__RECT__Y, // float
    TM_TT_PROP__RECT__W, // float
    TM_TT_PROP__RECT__H, // float
};
```

When we know what we want to access, we call the correct function and access the value. In our example we want to get the width of a object. The width is stored in `TM_TT_PROP__RECT__W`.

The function we need to call:

```c
void (*get_float)(tm_the_truth_o *tt,const tm_the_truth_object_o *obj, uint32_t property);
```

With this knowledge we can assemble the following function that logs the width of a object:

```c
void log_with(tm_the_truth_o *tt, tm_tt_id_t my_object){   
	const float wdith = tm_the_truth_api->get_float(tt,tm_tt_read(tt,my_object),TM_TT_PROP__RECT__W);
    TM_LOG("the width is %f",width);
}
```



## Make the code robust

To ensure we are actually handling the right type we should check this at the beginning of our function. If the type is not correct we should early out and log a warning.

All we need to do is compare the `tm_tt_type_t`'s of our types. Therefore we need to obtain the type id from the object id and from our expected type. From a `tm_tt_id_t` we can obtain the type by calling `tm_tt_type()` on them. `tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_TYPE);` will give us back the object type from a given hash. After that we can do our comparison.

```c
    void log_with(tm_the_truth_o *tt, tm_tt_id_t my_object){   
    const tm_tt_type_t type = tm_tt_type(my_object);
    const tm_tt_type_t expected_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__RECT);
    
    if(type.u64 != expected_type.u64){
        TM_LOG("The provided type does not mmatch! %p{tm_tt_type_t} != %p{tm_tt_type_t}",&type,&expected_type);
        return;
    }
   
const 	float wdith = tm_the_truth_api->get_float(tt,tm_tt_read(tt,my_object),my_object_w,TM_TT_PROP__RECT__W);
            TM_LOG("the width is %f",width);
}
```

> **Note:** Check out the logger documentation for more information on it. [log.h]({{docs}}foundation/log.h.html#log.h)


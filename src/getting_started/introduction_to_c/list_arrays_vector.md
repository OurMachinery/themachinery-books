# Arrays, Vectors, Lists where is my `std::vector<>` or `List<>`

**Table of Content**

* {:toc}

In the foundation we have a great header file or better inline header file the `foundation/carray.inl` which contains our solution for dynamic growing arrays, lists etc.  When used you are responsible for its memory and have to free the used memory at the end! Do not worry, the API makes it quite easy. 

Let us create an Array of `tm_tt_id_t`. All we need to do is declare our variable as a pointer of `tm_tt_id_t`.

```c
tm_tt_id_t* our_ids = 0;
```

After this we can for example push / add some data to our array:

```c
tm_carray_push(our_ids,my_id,my_allocator);
```

Now the my_id will be stored in the our_ids and allocated with my_allocator! In the end when I do not need my array anymore, I can call: `tm_carray_free(our_ids,my_allocator)`, and my memory is freed!

This doesn't look very pleasant when I am working with a lot of data that only needs to be a temporary list or something. For this case, you can use our temp allocator! Every `tm_carray_` macro has a `tm_carray_temp_` equivalent.

> **Note:** It is also recommended to make use of `tm_carray_resize` or `tm_carray_temp_resize` if you know how many elements your array might have. This will reduce the actual allocations.

Going back to our previous example:

```c
TM_INIT_TEMP_ALLOCATOR(ta);
tm_tt_id_t* all_objects = tm_the_truth_api->all_objects_of_type(tt, type, ta);
// do some magic
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```

`tm_the_truth_api->all_objects_of_type` actually returns a `carray` and you can operate on it with the normal C array methods: e.g. `tm_carray_size()` or `tm_carray_end()`. Since it is allocated with the temp allocator you can forget about the allocation at the end as long as you call `TM_SHUTDOWN_TEMP_ALLOCATOR`.

### How to access an element?

You can access a carray element normally like you would access it in a plain c array:

```c
TM_INIT_TEMP_ALLOCATOR(ta);
tm_tt_id_t* all_objects = tm_the_truth_api->all_objects_of_type(tt, type, ta);
if(all_objects[8].u64 == other_objects[8].u64){
    // what happens now?
}
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```

### Iterate over them

You can iterate over the carray like you would iterate over a normal array:

```c
TM_INIT_TEMP_ALLOCATOR(ta);
tm_tt_id_t* all_objects = tm_the_truth_api->all_objects_of_type(tt, type, ta);
for(uint64_t i = 0;i < tm_carray_size(all_objects);++i){
    TM_LOG("%llu",all_objects[i].u64);// we could also use TM_LOG("%p{tm_tt_id_t}",&all_objects[i]);
}
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```

An alternative approach is a more for each like approach:

```c
TM_INIT_TEMP_ALLOCATOR(ta);
tm_tt_id_t* all_objects = tm_the_truth_api->all_objects_of_type(tt, type, ta);
for(tm_tt_id* id = all_objects;id != tm_carray_end(all_objects);++id){
    TM_LOG("%llu",id->u64);// we could also use TM_LOG("%p{tm_tt_id_t}",id);
}
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```


# Memory Management

**Table of Content**

* {:toc}

While programming plugins for the Machinery, you will encounter the need to allocate things on the heap or generally speaking. In standard C code, you might tend to use `malloc, free or realloc`. Since we try to be as allocator aware as possible, we pass allocators actively down to systems. This means that wherever you need a long-life allocator (such as `malloc`), we give a `tm_allocator_i` object down. This allows you to allocate memory like you would with `malloc`. Like in std C you need to free the memory allocated via a `tm_allocator_i` at the end of its use. Otherwise you may leak. Using our built-in allocators gives you the benefits of automatic leak detection at the end of your program. Since all allocations are registered and analyzed at the end of the application, you will be notified if there is a leak. 

> **Note:** more about leak detection and memory usage check the chapter about the [Memory Usage Tab]({{base_url}}/qa_pipeline/memory.html)



### Child Allocators

In case you check our projects you will find that we are making extensive use of child allocators. This allows us to log the use of their memory in our [Memory Usage Tab]({{base_url}}/qa_pipeline/memory.html).

In case you check our [`Write a custom Tab` example]({{base_url}}extending_the_machinery/write-a-tab.html) you will find in its create function this code:

```c
static tm_tab_i* tab__create(tm_tab_create_context_t* context, tm_ui_o *ui)
{
    tm_allocator_i allocator = tm_allocator_api->create_child(context->allocator, "my tab");
    uint64_t* id = context->id;

    static tm_the_machinery_tab_vt* vt = 0;
    if (!vt)
        vt = tm_global_api_registry->get(TM_CUSTOM_TAB_VT_NAME);

    tm_tab_o* tab = tm_alloc(&allocator, sizeof(tm_tab_o));
    *tab = (tm_tab_o){
        .tm_tab_i = {
            .vt = (tm_tab_vt*)vt,
            .inst = (tm_tab_o*)tab,
            .root_id = *id,
        },
        .allocator = allocator,
    };

    return &tab->tm_tab_i;
}

static void tab__destroy(tm_tab_o* tab)
{
    tm_allocator_i a = tab->allocator;
    tm_free(&a, tab, sizeof(*tab));
    tm_allocator_api->destroy_child(&a);
}
```

The tm_tab_create_context_t context gives you access to the system allocator. This one again allows you to create a child allocator. We can now use the new allocator in our tab. This is why we store it within our `tm_tab_o` object.
In the end, we need to destroy our tab and, therefore free the tab object and destroy the child allocator. `tm_allocator_api->destroy_child(&a);`
If we now shut down the engine and we forgot to free any of the allocations done between create and destroy, we will get a nice log:

```bash
D:\git\themachinery\plugins\my_tab\my_tab.c(100): error leaked 1 allocations 4112 bytes
D:\git\themachinery\foundation\memory_tracker.c(120): error: Allocation scope `application` has allocations
```

### Rule of the thumb

Like in std C any allocation done with `tm_alloc` or `tm_alloc_at` and `tm_realloc` should be followed by a `tm_free`!

### Temporary Allocator

Sometimes we need to allocate data within a function. Sadly we do have access to the default allocator or do not want to give access to an allocator. Do not worry. The temp allocator comes to the rescue and the frame allocator. These are two concepts for quick allocations that you can forget about because the memory will free them at the end of the function or the frame!

**How to use the temp allocator?**

The temp allocator is part of the foundation and lives in its header file: `foundation/temp_allocator.h` Some APIs require temp allocators as the input. They will use them to allocate data that is needed for processing. At first, we need to create an object by using the following macro: `TM_INIT_TEMP_ALLOCATOR(ta)`

A temp allocator is created and can be used now! Importantly do not forget to call `TM_SHUTDOWN_TEMP_ALLOCATOR(ta)` at the end; otherwise, you have a memory leak! Do not worry. You won't be able to compile without calling this function!
Back to our example. Let's ask the Truth for all objects of a specific type:

```c
TM_INIT_TEMP_ALLOCATOR(ta);
tm_tt_id_t* all_objects = tm_the_truth_api->all_objects_of_type(tt, type, ta);
// do some magic
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```

The truth API will now use the temp allocator to create the list. We do not need to call tm_free anywhere, this is all done at the end by `TM_SHUTDOWN_TEMP_ALLOCATOR`!

Sometimes APIs require a normal `tm_allocator_i`, but you are not interested in creating an actual allocator or have access to a memory allocator! No worries, we have your back! The Temp Allocator gives you the following macro: `TM_INIT_TEMP_ALLOCATOR_WITH_ADAPTER(ta, a)`; It generates a normal `tm_allocator_i` uses the temp allocator as its backing allocator. Hence all allocations done with the allocator will be actually done via the `ta` allocator! Again at the end, all your memory is freed by `TM_SHUTDOWN_TEMP_ALLOCATOR(ta);`

>  **Note**: You also have `tm_temp_alloc()` they expect a `tm_temp_allocator_i` instead of the `tm_allocator_i`.

**What is the Frame Allocator?**

The [tm_temp_allocator_api](https://ourmachinery.com//apidoc/foundation/temp_allocator.h.html#structtm_temp_allocator_api) has a frame allocator. A frame allocator allocates memory for one frame and then at the end of the frame the memory is wiped out. This means any allocation done with it will stay in memory until the end of the frame! The way of using it is: `tm_temp_allocator_api.frame_alloc()` or `tm_frame_alloc()`

### Great use case: Formatted Strings

Both the frame as well as the temp allocator are great for using when you need to have a string with formatting! Infact the `tm_temp_allocator_api` provided an extra function for this: `tm_temp_allocator_api.printf()` /`tm_temp_allocator_api.frame_printf()`

> **Note:** About formatting checkout the `tm_sprintf_api`  or [the logging chapter]({{base_url}}/qa_pipeline/logging.html)

# Create a Custom Asset Type: Part 3

This part will cover the following topics:

- How to write an importer

>  You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* {:toc}


## Custom importer for text files

In this part, we will add the ability to import a text file into the Engine. To implement an importer, we need the following APIs:

| **Name**                | **header file**               | **Description**                                              |
| ----------------------- | ----------------------------- | ------------------------------------------------------------ |
| `tm_asset_io_api`       | `foundation/asset_io.h`       | This API has the importer interface.                         |
| `tm_temp_allocator_api` | `foundation/temp_allocator.h` | We will use this to allocate temporary memory.               |
| `tm_allocator_api`      | `foundation/allocator.h`      | We will use this for permanent memory allocations. `tm_allocator_api` supports a number of different allocators, for example the `system` allocator. We need this one later when we rewrite our reimport. |
| `tm_path_api`           | `foundation/path.h`           | Used for splitting and joining file system paths.            |
| `tm_api_registry_api`   | `foundation/api_registry.h`   | We use this to get access to APIs from the API registry.     |
| `tm_task_system_api`    | `foundation/task_system.h`    | Allows us to spawm tasks                                     |

We include these header files and retrieve the APis from the API registry.


> Note: `tm_api_registry_api` can be retrived from the reg parameter in the `tm_load_plugin` function. `tm_global_api_registry = reg;`

The Machinery has a generic interface for asset importers. It requires a bunch of functions to be able to work as intended. The struct we need to implement is called [tm_asset_io_i]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import). It requires us to set the following members:

| Member                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| `enabled()`                     | Should return `true` if the importer is active.              |
| `can_import()`                  | Optional. Should return `true` for the file extensions that can be imported by this interface. |
| `can_reimport()`                | Optional. Should return `true` for Truth assets that can be reimported. |
| `importer_extensions_string()`  | Optional. Extensions that can be imported by this interface. |
| `importer_description_string()` | Optional. Descriptions for the extensions in `importer_extensions_string()`. |
| `import_asset()`                | Implements the import. Since imports can be slow, they are typically implemented as background tasks and this function should return the ID of the background task from `tm_task_system_api`. |

All these members expect a function pointer. Therefore, we need to provide the functionality.

To implement the first functions, we need to do the following steps:

```c
//... other includes
#include <foundation/carray_print.inl>
#include <foundation/string.inl>
#include <foundation/localizer.h>
//... other code
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,asset_io_meta)}}
```

Let us go through them:

- `enabled()` returns *true* because we want the importer to work. 
- `asset_io__can_import()` compares the extension with the one we want to support.


> **Note**: `string.inl ` which we need to include for `tm_strcmp_ignore_case()` uses the `tm_localizer_api` for some of its functionality, that's why we need it.


- `asset_io__can_reimport()` checks if the object type matches our type. 


>  `TM_TT_PROP__ASSET__OBJECT` is the property of the [TM_TT_TYPE__ASSET]({{docs}}foundation/the_truth_assets.h.html#tm_tt_type__asset) type which holds the object associated with the asset.

The last two functions append `.txt` to the file extensions and descriptions. Note that the argument `output` is a [carray]({{docs}}foundation/carray.inl.html#carray.inl). We can use `tm_carray_temp_printf()` to append to that array.


>  **Note**: `carray_print.h` requires tm_sprintf_api`. Therefore, we need to include the right header here.

## Import Task Setup

To run the import as a background task we need to queue a task using the `tm_task_manager_api` from our `asset_io__import_asset()` function. Task functions take a single `void *userdata` argument. Since we typically want to pass more than one thing to the task, we put everything the task needs in a struct and pass a pointer to that struct as the `userdata`. The task function casts this `void *` to the desired type and can then make use of the data.

The task needs to know the location of the file that is to be imported. It also needs access to some semi-global objects, such as the Truth that the file should be imported to, and an allocator to use for memory allocations. The struct could look like this:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_decl)}}
```

The `tm_asset_io_import` field will used be copied from the parameter passed to `asset_io__import_asset()` to the struct.

The function itself looks like this:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,import_asset)}}
```


>  **Important**: The task is the memory owner and needs to clean it up at the end of the execution!

The line `task_system->run_task(task__import_txt, task, "Import Text File");` queues the task task `import_txt()` , with the data `task`, and returns its id. The id can be used to query for when the background task has completed. 


> Info: For more information on the task system check the [documentation]({{docs}}foundation/task_system.h.html#structtm_task_system_api.run_task()).


## Import Task Implementation

The import task should import the data and clean up afterwards.

The function signature is:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn)}}
```

We need to cast `ptr` to our previously defined data type `task__import_txt`. The task `id` can be used by the task callback function to provide task progress updates. In this example, we do not use it.


>  For more information on how to update the status of a task so that it is shown in the editor, see the [documentation]({{docs}}foundation/progress_report.h.html#structtm_progress_report_api).

To implement the import we retrieve the data passed in the struct and then implement the import as in the previous chapter. The reimport works the same as the import, except we add the buffer to an existing object instead of creating a new one:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn_begin)}}
```

Another thing we should consider is error checking: 

- Does the file exist? 
- Can we read the expected number of bytes from the file?

Since we are running as a background task, we will report any errors through the logging API: `tm_logger_api`. Errors reported that way will appear in the Console tab of the UI:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn_check)}}
```

Now we combine all the knowledge from this chapter and the previous chapter. We need to create a new asset via code for the import, and for the reimport, we need to update an existing file. 
Before we do all of this, let us first read the file and create the buffer.


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn_new_asset)}}
```

After this, we should ensure that the file size matches the size of the read data.


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn_read)}}
```

With this out of the way, we can use our knowledge from the last part.

- How to add an asset via code.

The first step was to create the new object and add the data to it.


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_new_buffer)}}
```

After that, we can use the `tm_asset_browser_add_asset_api` to add the asset to the asset browser. 

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,tm_asset_browser_add_asset_api)}}
```

We are getting the API first, because we do not need it anywhere else than in this case. Then we need to extract the file name of the imported file. You can do this with the *path API*'s ` tm_path_api->base()` function. Be aware this function requires a `tm_str_t` which you an create from a normal C string (`const char*`) via `tm_str()`. To access the underlaying C string again just call `.data` on the `tm_str_t`.

> `tm_str_t` represents strings with a `char *` and a size, instead of just a `char *`. 
>
> This lets you reason about parts of a string, which you are not able to do with standard NULL-terminated strings.
>
> [documentation]({{docs}}foundation/api_types.h.html#structtm_str_t)

We want to add the asset to the folder that currently open in the asset browser. We can ask the `tm_asset_browser_add_asset_api` what the current folder is. Then we decide if want to select the file. At the end we call `tm_asset_browser_add_asset_api->add()`. 

> **Note:** If we wanted to, we could add asset labels to the asset and pass them as the last two arguments of the `add()` function instead of `0, 0`.


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,tm_asset_browser_add_asset_api,off)}}
```

That's it for the import.  Before we move on, we need to clean up! No allocation without deallocation!


```c
    tm_free(args->allocator, task, task->bytes);
```


> Info:  If you forget to do this, the Engine will inform you that there is a memory leak in the Console log

Now let's bring it all together:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,import_asset_task)}}
```



## Enabling Reimport

Our implementation does not yet support reimports. Let us fix this quickly!

`tm_asset_io_import` has a field called `reimport_into` of type `tm_tt_id_t`. When doing a regular import, the value of this field will be `(tm_tt_id_t){0}`. When reimporting, it will be the ID of the Truth object that we should import into.

To change an existing object instead of creating a new one, we can use the function `tm_the_truth_api->retarget_write()`. It will make the `commit()` operation write the changes to an existing object instead of two the new one we just created. After comitting, we can destroy the new (temporary) object:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,reimport_asset_task)}}
```

With these changes, the source code now looks as like this:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,task_fn,off)}}
```


## Refactor the Custom UI Import Functionality

The last step before in this part of the tutorial is to update what happens when the user picks a new file in the Properties View of the asset. We want this workflow to make use of the asynchronous import functionality we just added to make the user experience smoother. Besides, this will also remove some code duplication.

Let's reuse our import task. We just need to make sure it has all the data it needs.
We can check the documentation of [tm_asset_io_import]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import) to ensure we do not forget anything important. 

Besides the name of the file we're importing, we also need:

- an allocator
- the Truth to import into
- the object to reimport into

Now we can write our reimport task code:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,custom_ui_inner)}}
```

We'll use the `system` allocator (a global allocator with the same lifetime as the program) to allocate our task, including the bytes needed for the file name string. Remember the layout of our struct:

```c
// -- struct definitions
struct task__import_txt
{
    uint64_t bytes;
    struct tm_asset_io_import args;
    char file[8];
};
// .. other code
```

We fill out the struct with the needed data, copy the file name, and then ask the task system to run the task:


```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c,custom_ui)}}
```

*(For more information on the structure of these functions, please check the previous part)*


- [Part 1](#)
- [Part 2](#)

## The End

This is the final part of this walkthrough. By now, you should have a better idea of:

- How to work with The Truth
- How to create an asset
- How to import assets into the Engine
- How to create a custom UI. 

If you want to see a more complex example of an importer, look at the assimp importer example: `samples\plugins\assimp`.

### Full Example of Basic Asset

`my_asset.h`

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.h)}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`)

`my_asset.c`

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/part_3/txt.c)}}
```


# Create a custom asset part 3

This walkthrough shows you how to add a custom asset to the Engine. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide]({{the_machinery_book}}extending_the_machinery/the_plugin_system.html). The goal for this walkthrough is to write a text file asset.

This part will cover the following topics:

- How to write an importer

>  You can find the whole source code in its git repo: [example-text-file-asset](https://github.com/simon-ourmachinery/example-text-file-asset)

**Table of Content**

* auto-gen TOC;
{:toc}


## Custom importer for text files

In this part, we are adding the ability to import a text file into the Engine. To implement an importer, we need the following APIs:

| **Name**              | **header file**             | **Description**                                              |
| --------------------- | --------------------------- | ------------------------------------------------------------ |
| tm_asset_io_api       | foundation/asset_io.h       | This api provides us with the interface for the actual importer. |
| tm_temp_allocator_api | foundation/temp_allocator.h | Provides a easy way to allocate temporary memory.            |
| tm_allocator_api      | foundation/allocator.h      | Allows us access to different kind of allocators. For example to the system allocator. We need this one later when we rewrite our reimport. |
| tm_path_api           | foundation/path.h           | Allows us to split a path.                                   |
| tm_api_registry_api   | foundation/api_registry.h   | Allows us to retrive a API from the registry.                |
| tm_task_system_api    | foundation/task_system.h    | Allowes us to spawm tasks                                    |

After we have included all the needed header files and retrieved all the APIs from the registry, we can start to write an importer.


> Note: `tm_api_registry_api` can be retrived from the reg parameter in the `tm_load_plugin` function. `tm_global_api_registry = reg;`

The Machinery has a generic interface for asset importers. It requires a bunch of functions to be able to work as intended. The struct we need to implement is called [tm_asset_io_i]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import). It requires us to set the following members:

| Member                      | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| enabled                     | A function ptr that returns a bool. If the return value is true the importer is active. |
| can_import                  | A function ptr that returns `true` if this asset IO interface can import archives with the file extension `extension`. This can be achieved by comparing the file extesions.<br><br>Optional, if not implemented, nothing can be imported. |
| can_reimport                | A function ptr that returns `true` if this asset IO interface can re-import the specified truth asset (of type `TM_TT_TYPE_ASSET`). Optional, if not implemented, nothing can be re-importe |
| importer_extensions_string  | A function ptr that shall append the correct file extention string to the list of possible file extenstions |
| importer_description_string | A function ptr that shall append the correct file extention descriptions string to the list of possible file extenstions descriptions. |
| import_asset                | The actual function that starts a import task. If non-zero, the return value is the ID of the background task from `tm_task_system_api` that does the import. |

All these members expect a function pointer. Therefore, we need to provide the functionality.

To implement the first functions, we need to do the following steps:

```c
//... other includes
#include <foundation/carray_print.inl>
#include <foundation/string.inl>
#include <foundation/localizer.h>
//... other code
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:99:119}}
```

Let us go through them:

- The `enabled` function returns true because we want the importer to work. 
- The `asset_io__can_import` will compare the given extension with the one we want to support.


> Note: `tm_strcmp_ignore_case` requires a localizer. That is why we need the localizer API and the localizer header file. It is not needed if the importer shall be case-sensitive.


- The `asset_io__can_reimport` compares the object type of the given object with the object of our type. 


>  `TM_TT_PROP__ASSET__OBJECT` is the property of the [TM_TT_TYPE__ASSET]({{docs}}foundation/the_truth_assets.h.html#tm_tt_type__asset) type which holds the object associated with the asset.

The last two functions will append the file extension `.txt` to the file extensions and description. Note that the argument output is a [carray]({{docs}}foundation/carray.inl.html#carray.inl). That is why we can use the `tm_carray_temp_printf` function.


>  Note: The `carray_print.h` requires the `tm_sprintf_api`. Therefore, we need to include the right header here.

## Import Task set up

The importer function `asset_io__import_asset` can spawn a task with the task system and pass through the needed information. We need to create a data structure to hold all our data.

*What data does our task need?* 

This task needs to know where to find the file. Moreover it needs to access some essential types such as the Truth and allocator. The struct could look like this:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:39:44}}
```

The `asset_io` header has a nice utility struct predefined the [tm_asset_io_import]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import). When an asset is being imported the caller of the  `asset_io__import_asset()` will hand through all the needed details: 


- The right Truth object
- the correct allocator. 

The function itself looks like this:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:120:130}}
```


>  **Important**: The task is the memory owner and needs to clean it up at the end of the execution!

This line `task_system->run_task(task__import_txt, task, "Import Text File");` will run a task and return its id. The actual task is the function `task__import_txt()`. 


> Info: For more information on the task system check the [documentation]({{docs}}foundation/task_system.h.html#structtm_task_system_api.run_task()).


## Import task implementation

The import task has the function to import data and clean up afterward.

It may look like this:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49}}
{
// all our work
}
```

The data `ptr` needs to be cast into our defined data type: `task__import_txt`. You could use the task id to update its progress. We do not need to do it in this example.


>  For more information on how to update the status of a task. It will be shown in the editor check out the [documentation]({{docs}}foundation/progress_report.h.html#structtm_progress_report_api).

We are left with the following steps:

- Implement the actual importing (similar to the previous chapter).
- Implement the reimport.

First, we need to retrieve the basic information from the task data:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:54}}
//.. more
}
```

After that, we implement the same code as in the previous chapter. We need to open the file, allocate a buffer and add the buffer to the object, either a new one (import) or an existing one (reimport).

**An important note is to do this time error checking**: 

- Does the file exist? 
- Does the file size match with the read file? 

To ask those questions is vital because we are in the async territory. In case of an error, we want to inform the user. Therefore, we need to get the logging API (`tm_logger_api = reg->get(TM_LOGGER_API_NAME);`) as well. You can find it in the `foundation/log.h` file.

The subsequent step is to check if the file exists. You can do this through the filesystem API:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:57}}
    // .. code
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
}
```

Now we combine all the knowledge from this chapter and the previous chapter. We need to create a new asset via code for the import, and for the reimport, we need to update an existing file. 
Before we do all of this, let us first read the file and create the buffer.


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:62}}
// ..code
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
}
```

After this, we should ensure that the file size matches the size of the read data.


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:63}}
//..
        }
        else
        {
            tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not read %s\n", txt_file);
        }
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
}
```

With this out of the way, we can use our knowledge from the last part.

- How to add an asset via code.

The first step was to create the new object and add the data to it.


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:65:70}}
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:79}}
```

After that, we are using the `tm_asset_browser_add_asset_api` to add the asset to the asset browser. 

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:81}}
```

We are getting the API first, because we do not need it anywhere else than in this case. Then we need to extract the file name of the imported file. You can do this with the *path API*'s ` tm_path_api->base()` function. Be aware this function requires a `tm_str_t` which you an create from a normal c string (`const char*`) via `tm_str()`. To access the underlaying c string again just call `.data` on the `tm_str_t`.

> Used to represent a string slice with pointer and length.
>
> This lets you reason about parts of a string, which you are not able to do with standard NULL-terminated strings.
>
> [documentation]({{docs}}foundation/api_types.h.html#structtm_str_t)

After this step we need to get the current folder. Therefore we are asking the `tm_asset_browser_add_asset_api` what the current folder is. Then we decide if want to select the file. At the end we are calling add function of the `tm_asset_browser_add_asset_api->add()`. 

> **Note:** We do not have any asset labels for our current asset therefore we do not pass them to the add function, otherwise the last 2 arguments would be different than `0` and `0`.


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:80:84}}
```

That's it for the import.  Before we move on, we need to clean up! No Allocation without deallocation!


```c
    tm_free(args->allocator, task, task->bytes);
```


> Info:  If you don't do this, the Engine will inform you that there is a memory leak in the logs/terminal.

Now bringing it all together:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:63}}
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:65:70}}
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:79}}
        }
        else
        {
            tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not read %s\n", txt_file);
        }
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
}
```



## Enabling reimport

The previous import task would never be able to reimport an asset. Let us fix this quickly!
The `tm_asset_io_import` has a field called `reimport_into` of type `tm_tt_id_t`, which we did not set. If the current context is an import, otherwise a valid the truth id. It enables us to check if the current context is an import or reimport. To achieve this, we need to update the `reimport_into` object with the newly created object asset_obj, and you can do this via The Truth API function `retarget_write.` It takes an object and updates it with the new content. Commit the change and destroy the temporary object (asset_obj).


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:71:76}}
```

This changes the source code as following:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:49:97}}
```


## Refactor the Custom UI import functionality

The last step before this part is over is to refactor the initial import of the file when we change the property in its custom UI. The current code does everything async. Besides, if we would leave this, we would have code duplication, which we want to avoid, for better-maintained reasons.

You might argue that it is the same process as just reimporting an asset when we change the path. That's correct!

We can reuse our Import-Task. Before we can launch a task, we need to ensure we have the right setup!
We can check the documentation of [tm_asset_io_import]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import) to ensure we do not forget anything important. 

After we have done that, we will find that the reimport task needs besides the file name:

- the allocator
- the current Truth
- the object to import reimport into

Now we can write our reimport task code. The code itself looks like this:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:151:161}}
```

First, we ask for the system allocator (This one has the same lifetime as the program is running). Then, we allocate our task, including bytes for the string. Remember the struct structure:

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

After that, we initialize our struct and its members with the needed data. Moreover, we copy the chars of the file name into our struct + extra bytes, and then we ask the task system to run the task.

This, combined with the custom UI functions, should look similar to this:


```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c:142:165}}
```

*(For more information on the structure of these functions, please check the previous part)*


- [Part 1](#)
- [Part 2](#)

## The end

It is the end of this walkthrough. You might have gained a better understanding:

- Of the Truth 
- How to create an asset
- How to import assets into the Engine
- How to provide a custom UI. 

If you wanted to see a more complex example of an importer, you could check the assimp importer example `samples\plugins\assimp`.

### Full example of basic asset

`my_asset.h`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.h}}
```

(Do not forget to run hash.exe when you create a `TM_STATIC_HASH`)

`my_asset.c`

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/custom_assets/part_3/txt.c}}
```


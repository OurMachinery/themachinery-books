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
static bool asset_io__enabled(struct tm_asset_io_o *inst)
{
    return true;
}
static bool asset_io__can_import(struct tm_asset_io_o *inst, const char *extension)
{
    return tm_strcmp_ignore_case(extension, "txt") == 0;
}
static bool asset_io__can_reimport(struct tm_asset_io_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t asset)
{
    const tm_tt_id_t object = tm_the_truth_api->get_subobject(tt, tm_tt_read(tt, asset), TM_TT_PROP__ASSET__OBJECT);
    return tm_tt_type(object).u64 == tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET).u64;
}
static void asset_io__importer_extensions_string(struct tm_asset_io_o *inst, char **output, struct tm_temp_allocator_i *ta, const char *separator)
{
    tm_carray_temp_printf(output, ta, "txt");
}
static void asset_io__importer_description_string(struct tm_asset_io_o *inst, char **output, struct tm_temp_allocator_i *ta, const char *separator)
{
    tm_carray_temp_printf(output, ta, ".txt");
}
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
struct task__import_txt
{
    uint64_t bytes;
    struct tm_asset_io_import args;
    char file[8];
};
```

The `asset_io` header has a nice utility struct predefined the [tm_asset_io_import]({{docs}}foundation/asset_io.h.html#structtm_asset_io_import). When an asset is being imported the caller of the  `asset_io__import_asset()` will hand through all the needed details: 


- The right Truth object
- the correct allocator. 

The function itself looks like this:


```c
// .. other code
static uint64_t asset_io__import_asset(struct tm_asset_io_o *inst, const char *file, const struct tm_asset_io_import *args)
{
    const uint64_t bytes = sizeof(struct task__import_txt) + strlen(file);
    struct task__import_txt *task = tm_alloc(args->allocator, bytes);
    *task = (struct task__import_txt){
        .bytes = bytes,
        .args = *args,
    };
    strcpy(task->file, file);
    return task_system->run_task(task__import_txt, task, "Import Text File");
}
```


>  **Important**: The task is the memory owner and needs to clean it up at the end of the execution!

This line `task_system->run_task(task__import_txt, task, "Import Text File");` will run a task and return its id. The actual task is the function `task__import_txt()`. 


> Info: For more information on the task system check the [documentation]({{docs}}foundation/task_system.h.html#structtm_task_system_api.run_task()).


## Import task implementation

The import task has the function to import data and clean up afterward.

It may look like this:

```c
static void task__import_txt(void *data, uint64_t task_id)
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
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
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
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists)
    {
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
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists)
    {
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(txt_file);
        const int64_t read = tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
// ..code
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
}
```

After this, we should ensure that the file size matches the size of the read data.


```c
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists)
    {
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(txt_file);
        const int64_t read = tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
        if (read == (int64_t)stat.size)
        {
        // ..code
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

With this out of the way, we can use our knowledge from the \[last part\](#): 

- How to add an asset via code.

The first step was to create the new object and add the data to it.


```c
const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
const tm_tt_type_t plugin_asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
const tm_tt_id_t asset_id = tm_the_truth_api->create_object_of_type(tt, plugin_asset_type, TM_TT_NO_UNDO_SCOPE);
tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, asset_id);
tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id);
tm_the_truth_api->set_string(tt, asset_obj, TM_TT_PROP__MY_ASSET__FILE, txt_file);
 tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
```

After that, we are using the `tm_asset_browser_add_asset_api` to add the asset to the asset browser. 

```c
tm_asset_browser_add_asset_api *add_asset = tm_global_api_registry->get(TM_ASSET_BROWSER_ADD_ASSET_API_NAME);
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
                const char *asset_name = tm_path_api->base(tm_str(txt_file)).data;
                tm_asset_browser_add_asset_api *add_asset = tm_global_api_registry->get(TM_ASSET_BROWSER_ADD_ASSET_API_NAME);
                const tm_tt_id_t current_dir = add_asset->current_directory(add_asset->inst, args->ui);
                const bool should_select = args->asset_browser.u64 && tm_the_truth_api->version(tt, args->asset_browser) == args->asset_browser_version_at_start;
                // we do not have any asset label therefore we do not need to pass them thats why the last
                // 2 arguments are 0 and 0!
                add_asset->add(add_asset->inst, current_dir, asset_id, asset_name, args->undo_scope, should_select, args->ui,0,0);
```

That's it for the import.  Before we move on, we need to clean up! No Allocation without deallocation!


```c
    tm_free(args->allocator, task, task->bytes);
```


> Info:  If you don't do this, the Engine will inform you that there is a memory leak in the logs/terminal.

Now bringing it all together:


```c
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists)
    {
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(txt_file);
        const int64_t read = tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
        if (read == (int64_t)stat.size)
        {
const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
const tm_tt_type_t plugin_asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
const tm_tt_id_t asset_id = tm_the_truth_api->create_object_of_type(tt, plugin_asset_type, TM_TT_NO_UNDO_SCOPE);
tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, asset_id);
tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id);
tm_the_truth_api->set_string(tt, asset_obj, TM_TT_PROP__MY_ASSET__FILE, txt_file);
 tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                const char *asset_name = tm_path_api->base(tm_str(txt_file)).data;
                tm_asset_browser_add_asset_api *add_asset = tm_global_api_registry->get(TM_ASSET_BROWSER_ADD_ASSET_API_NAME);
                const tm_tt_id_t current_dir = add_asset->current_directory(add_asset->inst, args->ui);
                const bool should_select = args->asset_browser.u64 && tm_the_truth_api->version(tt, args->asset_browser) == args->asset_browser_version_at_start;
                // we do not have any asset label therefore we do not need to pass them thats why the last
                // 2 arguments are 0 and 0!
                add_asset->add(add_asset->inst, current_dir, asset_id, asset_name, args->undo_scope, should_select, args->ui,0,0);
        }
        else
        {
            tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not read %s\n", txt_file);
        }
    }
    else
    {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
    tm_free(args->allocator, task, task->bytes);
}
```



## Enabling reimport

The previous import task would never be able to reimport an asset. Let us fix this quickly!
The `tm_asset_io_import` has a field called `reimport_into` of type `tm_tt_id_t`, which we did not set. If the current context is an import, otherwise a valid the truth id. It enables us to check if the current context is an import or reimport. To achieve this, we need to update the `reimport_into` object with the newly created object asset_obj, and you can do this via The Truth API function `retarget_write.` It takes an object and updates it with the new content. Commit the change and destroy the temporary object (asset_obj).


```c
            if (args->reimport_into.u64)
            {
                tm_the_truth_api->retarget_write(tt, asset_obj, args->reimport_into);
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                tm_the_truth_api->destroy_object(tt, asset_id, args->undo_scope);
            }
```

This changes the source code as following:


```c
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists) {
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(txt_file);
        const int64_t read = tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
        if (read == (int64_t)stat.size) {
            const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
            const tm_tt_type_t plugin_asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
            const tm_tt_id_t asset_id = tm_the_truth_api->create_object_of_type(tt, plugin_asset_type, TM_TT_NO_UNDO_SCOPE);
            tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, asset_id);
            tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id);
            tm_the_truth_api->set_string(tt, asset_obj, TM_TT_PROP__MY_ASSET__FILE, txt_file);
            if (args->reimport_into.u64) {
                tm_the_truth_api->retarget_write(tt, asset_obj, args->reimport_into);
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                tm_the_truth_api->destroy_object(tt, asset_id, args->undo_scope);
            } else {
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                const char *asset_name = tm_path_api->base(tm_str(txt_file)).data;
                struct tm_asset_browser_add_asset_api *add_asset = tm_global_api_registry->get(TM_ASSET_BROWSER_ADD_ASSET_API_NAME);
                const tm_tt_id_t current_dir = add_asset->current_directory(add_asset->inst, args->ui);
                const bool should_select = args->asset_browser.u64 && tm_the_truth_api->version(tt, args->asset_browser) == args->asset_browser_version_at_start;
                add_asset->add(add_asset->inst, current_dir, asset_id, asset_name, args->undo_scope, should_select, args->ui, 0, 0);
            }
        } else {
            tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not read %s\n", txt_file);
        }
    } else {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
    tm_free(args->allocator, task, task->bytes);
}
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
            tm_allocator_i *allocator = tm_allocator_api->system;
            const uint64_t bytes = sizeof(struct task__import_txt) + strlen(file);
            struct task__import_txt *task = tm_alloc(allocator, bytes);
            *task = (struct task__import_txt){
                .bytes = bytes,
                .args = {
                    .allocator = allocator,
                    .tt = tt,
                    .reimport_into = object}};
            strcpy(task->file, file);
            task_system->run_task(task__import_txt, task, "Import Text File");
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
//custom ui
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    tm_the_truth_o *tt = args->tt;
    bool picked = false;
    item_rect.y = tm_properties_view_api->ui_open_path(args, item_rect, TM_LOCALIZE_LATER("Import Path"), TM_LOCALIZE_LATER("Path that the text file was imported from."), object, TM_TT_PROP__MY_ASSET__FILE, "txt", "text files", &picked);
    if (picked)
    {
        const char *file = tm_the_truth_api->get_string(tt, tm_tt_read(tt, object), TM_TT_PROP__MY_ASSET__FILE);
        {
            tm_allocator_i *allocator = tm_allocator_api->system;
            const uint64_t bytes = sizeof(struct task__import_txt) + strlen(file);
            struct task__import_txt *task = tm_alloc(allocator, bytes);
            *task = (struct task__import_txt){
                .bytes = bytes,
                .args = {
                    .allocator = allocator,
                    .tt = tt,
                    .reimport_into = object}};
            strcpy(task->file, file);
            task_system->run_task(task__import_txt, task, "Import Text File");
        }
    }
    return item_rect.y;
}
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

All the source code is available on GitHub in the [**example-text-file-asset**](https://github.com/simon-ourmachinery/example-text-file-asset) repo.

**Full Source Code**

`txt.h`

```c
#pragma once
#include <foundation/api_types.h>
//... more code
#define TM_TT_TYPE__MY_ASSET "tm_my_asset"
#define TM_TT_TYPE_HASH__MY_ASSET TM_STATIC_HASH("tm_my_asset", 0x1e12ba1f91b99960ULL)

enum {
    TM_TT_PROP__MY_ASSET__FILE,
    TM_TT_PROP__MY_ASSET__DATA,
};
```



`txt.c`

```c
// -- api's
static struct tm_api_registry_api *tm_global_api_registry;
static struct tm_the_truth_api *tm_the_truth_api;
static struct tm_properties_view_api *tm_properties_view_api;
static struct tm_os_api *tm_os_api;
static struct tm_path_api *tm_path_api;
static struct tm_temp_allocator_api *tm_temp_allocator_api;
static struct tm_logger_api *tm_logger_api;
static struct tm_localizer_api *tm_localizer_api;
static struct tm_asset_io_api *tm_asset_io_api;
static struct tm_task_system_api *task_system;
static struct tm_allocator_api *tm_allocator_api;
static struct tm_sprintf_api *tm_sprintf_api;

// -- inlcudes

#include <foundation/api_registry.h>
#include <foundation/asset_io.h>
#include <foundation/buffer.h>
#include <foundation/carray_print.inl>
#include <foundation/localizer.h>
#include <foundation/log.h>
#include <foundation/macros.h>
#include <foundation/os.h>
#include <foundation/path.h>
#include <foundation/sprintf.h>
#include <foundation/string.inl>
#include <foundation/task_system.h>
#include <foundation/temp_allocator.h>
#include <foundation/the_truth.h>
#include <foundation/the_truth_assets.h>
#include <foundation/undo.h>

#include <plugins/editor_views/asset_browser.h>
#include <plugins/editor_views/properties.h>

#include "txt.h"
// -- struct definitions
struct task__import_txt
{
    uint64_t bytes;
    struct tm_asset_io_import args;
    char file[8];
};
/////
// -- functions:
////
// --- importer
static void task__import_txt(void *data, uint64_t task_id)
{
    struct task__import_txt *task = (struct task__import_txt *)data;
    const struct tm_asset_io_import *args = &task->args;
    const char *txt_file = task->file;
    tm_the_truth_o *tt = args->tt;
    tm_file_stat_t stat = tm_os_api->file_system->stat(txt_file);
    if (stat.exists) {
        tm_buffers_i *buffers = tm_the_truth_api->buffers(tt);
        void *buffer = buffers->allocate(buffers->inst, stat.size, false);
        tm_file_o f = tm_os_api->file_io->open_input(txt_file);
        const int64_t read = tm_os_api->file_io->read(f, buffer, stat.size);
        tm_os_api->file_io->close(f);
        if (read == (int64_t)stat.size) {
            const uint32_t buffer_id = buffers->add(buffers->inst, buffer, stat.size, 0);
            const tm_tt_type_t plugin_asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
            const tm_tt_id_t asset_id = tm_the_truth_api->create_object_of_type(tt, plugin_asset_type, TM_TT_NO_UNDO_SCOPE);
            tm_the_truth_object_o *asset_obj = tm_the_truth_api->write(tt, asset_id);
            tm_the_truth_api->set_buffer(tt, asset_obj, TM_TT_PROP__MY_ASSET__DATA, buffer_id);
            tm_the_truth_api->set_string(tt, asset_obj, TM_TT_PROP__MY_ASSET__FILE, txt_file);
            if (args->reimport_into.u64) {
                tm_the_truth_api->retarget_write(tt, asset_obj, args->reimport_into);
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                tm_the_truth_api->destroy_object(tt, asset_id, args->undo_scope);
            } else {
                tm_the_truth_api->commit(tt, asset_obj, args->undo_scope);
                const char *asset_name = tm_path_api->base(tm_str(txt_file)).data;
                struct tm_asset_browser_add_asset_api *add_asset = tm_global_api_registry->get(TM_ASSET_BROWSER_ADD_ASSET_API_NAME);
                const tm_tt_id_t current_dir = add_asset->current_directory(add_asset->inst, args->ui);
                const bool should_select = args->asset_browser.u64 && tm_the_truth_api->version(tt, args->asset_browser) == args->asset_browser_version_at_start;
                add_asset->add(add_asset->inst, current_dir, asset_id, asset_name, args->undo_scope, should_select, args->ui, 0, 0);
            }
        } else {
            tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not read %s\n", txt_file);
        }
    } else {
        tm_logger_api->printf(TM_LOG_TYPE_INFO, "import txt:cound not find %s \n", txt_file);
    }
    tm_free(args->allocator, task, task->bytes);
}

static bool asset_io__enabled(struct tm_asset_io_o *inst)
{
    return true;
}
static bool asset_io__can_import(struct tm_asset_io_o *inst, const char *extension)
{
    return tm_strcmp_ignore_case(extension, "txt") == 0;
}
static bool asset_io__can_reimport(struct tm_asset_io_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t asset)
{
    const tm_tt_id_t object = tm_the_truth_api->get_subobject(tt, tm_tt_read(tt, asset), TM_TT_PROP__ASSET__OBJECT);
    return object.type == tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET).u64;
}
static void asset_io__importer_extensions_string(struct tm_asset_io_o *inst, char **output, struct tm_temp_allocator_i *ta, const char *separator)
{
    tm_carray_temp_printf(output, ta, "txt");
}
static void asset_io__importer_description_string(struct tm_asset_io_o *inst, char **output, struct tm_temp_allocator_i *ta, const char *separator)
{
    tm_carray_temp_printf(output, ta, ".txt");
}
static uint64_t asset_io__import_asset(struct tm_asset_io_o *inst, const char *file, const struct tm_asset_io_import *args)
{
    const uint64_t bytes = sizeof(struct task__import_txt) + strlen(file);
    struct task__import_txt *task = tm_alloc(args->allocator, bytes);
    *task = (struct task__import_txt){
        .bytes = bytes,
        .args = *args,
    };
    strcpy(task->file, file);
    return task_system->run_task(task__import_txt, task, "Import Text File");
}
static struct tm_asset_io_i txt_asset_io = {
    .enabled = asset_io__enabled,
    .can_import = asset_io__can_import,
    .can_reimport = asset_io__can_reimport,
    .importer_extensions_string = asset_io__importer_extensions_string,
    .importer_description_string = asset_io__importer_description_string,
    .import_asset = asset_io__import_asset
};

// -- asset on its own

//custom ui
static float properties__custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    tm_the_truth_o *tt = args->tt;
    bool picked = false;
    item_rect.y = tm_properties_view_api->ui_open_path(args, item_rect, TM_LOCALIZE_LATER("Import Path"), TM_LOCALIZE_LATER("Path that the text file was imported from."), object, TM_TT_PROP__MY_ASSET__FILE, "txt", "text files", &picked);
    if (picked) {
        const char *file = tm_the_truth_api->get_string(tt, tm_tt_read(tt, object), TM_TT_PROP__MY_ASSET__FILE);
        {
            tm_allocator_i *allocator = tm_allocator_api->system;
            const uint64_t bytes = sizeof(struct task__import_txt) + strlen(file);
            struct task__import_txt *task = tm_alloc(allocator, bytes);
            *task = (struct task__import_txt){
                .bytes = bytes,
                .args = {
                    .allocator = allocator,
                    .tt = tt,
                    .reimport_into = object }
            };
            strcpy(task->file, file);
            task_system->run_task(task__import_txt, task, "Import Text File");
        }
    }
    return item_rect.y;
}

// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER },
    };
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_ASSET, my_asset_properties, TM_ARRAY_COUNT(my_asset_properties));
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "txt");
    static tm_properties_aspect_i properties_aspect = {
        .custom_ui = properties__custom_ui,
    };
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__PROPERTIES, &properties_aspect);
}

// -- asset browser regsiter interface
static tm_tt_id_t asset_browser_create(struct tm_asset_browser_create_asset_o *inst, tm_the_truth_o *tt, tm_tt_undo_scope_t undo_scope)
{
    const tm_tt_type_t type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__MY_ASSET);
    return tm_the_truth_api->create_object_of_type(tt, type, undo_scope);
}
static tm_asset_browser_create_asset_i asset_browser_create_my_asset = {
    .menu_name = TM_LOCALIZE_LATER("New Text File"),
    .asset_name = TM_LOCALIZE_LATER("New Text File"),
    .create = asset_browser_create,
};

// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
    tm_properties_view_api = reg->get(TM_PROPERTIES_VIEW_API_NAME);
    tm_os_api = reg->get(TM_OS_API_NAME);
    tm_path_api = reg->get(TM_PATH_API_NAME);
    tm_temp_allocator_api = reg->get(TM_TEMP_ALLOCATOR_API_NAME);
    tm_allocator_api = reg->get(TM_ALLOCATOR_API_NAME);
    tm_logger_api = reg->get(TM_LOGGER_API_NAME);
    tm_localizer_api = reg->get(TM_LOCALIZER_API_NAME);
    tm_asset_io_api = reg->get(TM_ASSET_IO_API_NAME);
    task_system = reg->get(TM_TASK_SYSTEM_API_NAME);
    tm_sprintf_api = reg->get(TM_SPRINTF_API_NAME);
    tm_global_api_registry = reg;
    if (load)
        tm_asset_io_api->add_asset_io(&txt_asset_io);
    else
        tm_asset_io_api->remove_asset_io(&txt_asset_io);
    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
    tm_add_or_remove_implementation(reg, load, TM_ASSET_BROWSER_CREATE_ASSET_INTERFACE_NAME, &asset_browser_create_my_asset);
}
```


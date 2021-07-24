# Logging

The Machinery comes with a build in Logger system. The Logger System lives in the `foundation/log.h` and contains the `tm_logger_api`. This API provides a few connivance macros. We can use them to log our code from anywhere. Besides this it is super easy to create your own logger and add it to the logger API.



## Logging cheat sheet

You can log custom types. This is enabled via the `tm_sprintf_api`. You can log all primitive types like you are used to from C but as well as the engines API types. Just keep in mind the following syntax: `%p{<MY_TYPE>}` and the **fact** that you **need** to provide a pointer to the correct type:

| type                 | call                                          |
| -------------------- | --------------------------------------------- |
| `bool`               | `TM_LOG("%p{bool}",&my_value);`               |
| `tm_vec2_t`          | `TM_LOG("%p{tm_vec2_t}",&my_value);`          |
| `tm_vec3_t`          | `TM_LOG("%p{tm_vec2_t}",&my_value);`          |
| `tm_vec4_t`          | `TM_LOG("%p{tm_vec4_t}",&my_value);`          |
| `tm_mat44_t`         | `TM_LOG("%p{tm_mat44_t}",&my_value);`         |
| `tm_transform_t`     | `TM_LOG("%p{tm_transform_t}",&my_value);`     |
| `tm_rect_t`          | `TM_LOG("%p{tm_rect_t}",&my_value);`          |
| `tm_str_t`           | `TM_LOG("%p{tm_str_t}",&my_value);`           |
| `tm_uuid_t`          | `TM_LOG("%p{tm_uuid_t}",&my_value);`          |
| `tm_color_srgb_t`    | `TM_LOG("%p{tm_color_srgb_t}",&my_value);`    |
| `tm_tt_type_t`       | `TM_LOG("%p{tm_tt_type_t}",&my_value);`       |
| `tm_tt_id_t`         | `TM_LOG("%p{tm_tt_id_t}",&my_value);`         |
| `tm_tt_undo_scope_t` | `TM_LOG("%p{tm_tt_undo_scope_t}",&my_value);` |
| `tm_strhash_t`       | `TM_LOG("%p{tm_strhash_t}",&my_value);`       |

You can register a support for your own custom type via the `tm_sprintf_api.add_printer()`.



## Write a custom logger

If you desire to add your own logger sink to the eco system there are a few steps you need to take:

1. You need to include the `foundation/log.h` header
2. You need to define a `tm_logger_i` in your file
3. You need add a `log` function to this interface
   1. If you need some local data (such as a allocator)  it might be good to define a `.inst` as well.
4. After all of this you can call the `tm_logger_api.add_logger()`  function to register your logger

*Example:*

```
#include <foundation/log.h>
// some more code

static void my_log_function(struct tm_logger_o *inst, enum tm_log_type log_type, const char *msg)
{
// do what you feel like doing!
}

tm_logger_i *logger = &(tm_logger_i){
    .log = my_log_function,
};
//.. more code
// This functions gets called at some point and this is the point I would like to register my logger
static void my_custom_api_function(void){
    tm_logger_api->add_logger(logger);
}
```

> **Note:** This can be a use case for plugin [callbacks](https://ourmachinery.com//apidoc/foundation/plugin_callbacks.h.html#plugin_callbacks.h). More about this see [Write a plugin]({{base_url}}/extending_the_machinery/write-a-plugin.html#plugin-callbacks-init-sutdown-tick)

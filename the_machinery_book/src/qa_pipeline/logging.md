# Logging

The Machinery comes with a built-in Logger system. The Logger System lives in the `foundation/log.h` and contains the `tm_logger_api`. This API provides a few connivance macros. We can use them to log our code from anywhere. Besides this it is super easy to create your own logger and add it to the logger API.



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

*example:*

First you define a function with a signature of the type `tm_sprintf_printer`. `int tm_sprintf_printer(char *buf, int count, tm_str_t type, tm_str_t args, const void *data);`

```c
static int printer__custom_color_srgb_t(char *buf, int count, tm_str_t type, tm_str_t args, const void *data)
{
    const custom_color_srgb_t *v = data;
    return print(buf, count, "{ .r = %d, .g = %d, .b = %d, .a = %d , .hash = %llu }", v->r, v->g, v->b, v->a, v->hash);
}
```

After that you register it via the `tm_sprintf_api` to the `add_printer()` function.

```c
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_sprintf_api = reg->get(TM_SPRINTF_API_NAME);
    if(tm_sprintf_api->add_printer){
        tm_sprintf_api->add_printer("custom_color_srgb_t", printer__custom_color_srgb_t);
    }
}
```



### More `tm_sprintf_api` formatting cheats

| Fmt                      | Value                                | Result                                      |
| -----------------------  | -----------------------------------  | ------------------------------------------  |
| `%I64d`                  | `(uint64_t)100`                      | `100`                                       |
| `%'d`                    | `12345`                              | `12,345`                                    |
| `%$d`                    | `12345`                              | `12.3 k`                                    |
| `%$d`                    | `1000`                               | `1.0 k`                                     |
| `%$.2d`                  | `2536000`                            | `2.53 M`                                    |
| `%$$d`                   | `2536000`                            | `2.42 Mi`                                   |
| `%$$$d`                  | `2536000`                            | `2.42 M`                                    |
| `%_$d`                   | `2536000`                            | `2.53M`                                     |
| `%b`                     | `36`                                 | `100100`                                    |
| `%p{bool}`               | `&(bool){true}`                      | `true`                                      |
| `%p{tm_vec3_t}`          | `&(tm_vec3_t){ 1, 2, 3 }`            | `{ 1, 2, 3 }`                               |
| `%p{tm_vec3_t}`          | `0`                                  | `(null)`                                    |
| `%p{unknown_type}`       | `&(tm_vec3_t){ 1, 2, 3 }`            | `%p{unknown_type}`                          |
| `%p{unknown_type:args}`  | `&(tm_vec3_t){ 1, 2, 3 }`            | `%p{unknown_type:args}`                     |
| `%p{tm_vec3_t`           | `&(tm_vec3_t){ 1, 2, 3 }`            | `(error)`                                   |
| `%p{tm_rect_t}`          | `&(tm_rect_t){ 10, 20, 100, 200 })`  | `{ 10, 20, 100, 200 }`                      |
| `%p{tm_color_srgb_t}`    | `&TM_RGB(0xff7f00)`                  | `{ .r = 255, .g = 127, .b = 0, .a = 255 }`  |



## Write a custom logger

If you desire to add your own logger sink to the ecosystem there are a few steps you need to take:

1. You need to include the `foundation/log.h` header
2. You need to define a `tm_logger_i` in your file
3. You need add a `log` function to this interface
   1. If you need some local data (such as an allocator)  it might be good to define a `.inst` as well.
4. After all of this you can call the `tm_logger_api.add_logger()`  function to register your logger

*Example:*

```c
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

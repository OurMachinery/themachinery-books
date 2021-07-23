# Aspects

An “aspect” is an interface (struct of function pointers) identified by a unique identifier. The Truth allows you to associate aspects with object types. This lets you extend The Truth with new functionality. For example, you could add an interface for debug printing an object:

```c
 #define TM_TT_ASPECT__DEBUG_PRINT TM_STATIC_HASH("tm_debug_print_aspect_i", 0x39821c78639e0773ULL)

 typedef struct tm_debug_print_aspect_i {
    void (*debug_print)(tm_the_truth_o *tt, uint64_t o);
} tm_debug_print_aspect_i;
```

You could then use this code to debug print an object `o` with:

```c
tm_debug_print_aspect_i *dp = tm_the_truth_api->get_aspect(tt, tm_tt_type(o), TM_DEBUG_PRINT_ASPECT);
if (dp)
    dp->debug_print(tt, o);
```

>  **Note**: that plugins can extend the system with completely new aspects.



The best example of how the Engine is using the aspect system is the `TM_TT_ASPECT__PROPERTIES` which helps us to defines custom UIs for Truth objects.
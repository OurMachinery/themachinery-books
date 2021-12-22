# Aspects

An “aspect” is an interface (struct of function pointers) identified by a unique identifier. The Truth allows you to associate aspects with object types. This lets you extend The Truth with new functionality. For example, you could add an interface for debug printing an object:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/truth_mixed.c,debug_aspect)}}
```

> **Note:** to genereate the `TM_STATIC_HASH` you need to run `hash.exe` or `tmbuild.exe --gen-hash` for more info open the [hash.exe guide]({{the_machinery_book}}/helper_tools/hash.html)

You could then use this code to debug print an object `o` with:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/truth/truth_mixed.c,example_use_case)}}
```

>  **Note**: that plugins can extend the system with completely new aspects.



The best example of how the Engine is using the aspect system is the `tm_properties_aspect_i` which helps us to defines custom UIs for Truth objects.
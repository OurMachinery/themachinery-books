# Extending The Machinery

In The Machinery, **everything is a [plugin]({{base_url}}extending_the_machinery/the_plugin_system.html)**. You can **extend**, **modify** or **replace** existing engine functionality with your plugins. 

The Engine explicitly aims to be simple, minimalistic, and easy to understand. All our code is written in plain C, a significantly more straightforward language than modern C++. The entire codebase compiles in less than 30 seconds, and we support hot-reloading of DLLs, allowing for fast iteration cycles. You can modify your plugin code while the editor or the game runs since the plugin system supports [hot-reloading]({{base_url}}extending_the_machinery/hot-reloading.html). In short, we want to be "hackable." Our APIs are exposed as C interfaces, which means you can easily use them from C, C++, D, or any other language with an FFI for calling into C code.



**Guides to follow:**

- Basic understanding on how to [write a plugin]({{base_url}}extending_the_machinery/write-a-plugin.html).
- Basic understanding about [gameplay coding]({{base_url}}gameplay_coding/index.html).
- More complex tutorials about custom plugins check out the [Tutorials Book]({{base_url}})


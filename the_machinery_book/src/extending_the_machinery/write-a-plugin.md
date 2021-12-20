## Write a plugin

This walkthrough shows you how to extend the engine with a custom plugin.

You will learn about:

- What is needed to write a plugin
- How to write a plugin

This walk through expects you to have the basic understanding about the plugin system. Otherwise you can read more [here]({{base_url}}extending_the_machinery/the_plugin_system.html).

**Table of Content**

* auto-gen TOC;
{:toc}

## Where does the engine search for plugins

The Machinery is built around a plugin model. All features, even the built-in ones, are provided
through plugins. You can extend The Machinery by writing your own plugins. When The Machinery
launches, it loads all the plugins named `tm_*.dll` in its `plugins/` folder. If you write your own
plugins, name them so that they start with `tm_` and put them in this folder, they will be loaded
together with the built-in plugins.

> **Note:** When you create a new plugin via the Engine, the `premake` file will **not** copy the plugin into your global plugin folder. The reason behind this is that we do not know if you want to create a plugin asset. *This workflow is currently under review.*
>
> **Important:** The plugins created via the Engine expect a binary build version if you are using the source access version you might have to modify the `premake` file to make it point to the correct version. This workflow is currently under review.

## Inspect an existing example to get inspiration

The easiest way to build a plugin is to start with an existing example. There are three places where
you can find plugin samples:

1. The `samples` folder in the SDK has a number of plugin samples.

2. The *All Sample Projects* package in the *Download* tab has a `plugins` folder with some small
   samples.

3. You can create a new plugin with the menu command **File > New Plugin**. This will create a
   new `.c` file for the plugin together with some helper files for compiling it. ([Follow this guide](#write-your-own-plugin))

The distribution already comes with pre-built .dlls for the sample plugins, such as
`bin/plugins/tm_pong_tab.dll`. You can see this plugin in action by selecting **Tab > Pong** in the
editor to open up its tab:

![Pong tab.](https://www.dropbox.com/s/hats2jgr3wroahz/pong-tab.png?dl=1)

### What are the build Requirements

To build plugins you need three things:

1. You need to have Visual Studio 2019 installed including the MS C++ Build Tools on your computer.
   Note that the Community Edition works fine. (Or clang and the build essentials on Linux)
2. You need to set the `TM_SDK_DIR` environment variable to the path of the SDK package that you
   installed on your computer. When you compile a plugin, it looks for The Machinery headers in the
   `%TM_SDK_DIR%/headers` folder. 
3. You need the `tmbuild.exe` from the SDK package. `tmbuild.exe` does all the steps needed to
   compile the plugin. Put it in your `PATH` or copy it to your plugin folder so that you can run it
   easily from the command line.

### Build the sample plugin

To compile a plugin, simply open a command prompt in the plugin folder and run the `tmbuild.exe`
executable:

~~~ cmd input
sample-projects/plugins/custom_tab> %TM_SDK_DIR%/bin/tmbuild.exe
​~~~ cmd output
Installing 7za.exe...
Installing premake-5.0.0-alpha14-windows...
Building configurations...
Running action 'vs2019'...
Generated custom_tab.sln...
Generated build/custom_tab/custom_tab.vcxproj...
Done (133ms).
Microsoft (R) Build Engine version 16.4.0+e901037fe for .NET Framework
Copyright (C) Microsoft Corporation. All rights reserved.

  custom_tab.c
  custom_tab.vcxproj -> C:\work\themachinery\build\bin\plugins\tm_custom_tab.dll

-----------------------------
tmbuild completed in: 23.471 s
~~~

`tmbuild.exe` will perform the following steps to build your executable:

1. Create a `libs` folder and download `premake5` into it. (You can set the `TM_LIB_DIR` environment
   variable to use a shared `libs` directory for all your projects.)
2. Run `premake5` to create a Visual Studio project from the `premake5.lua` script.
3. Build the Visual Studio project to build the plugin.

> **Note:** You can learn more about [tmbuild]({{base_url}}helper_tools/tmbuild.html) in its own section.

## Programming in C

*The Machinery* uses C99 as its interface language. I.e., all the header files that you use to
communicate with *The Machinery* are C99 header files, and when you write a plugin you should expose
C99 headers for your APIs. The *implementation* of a plugin can be written in whichever language you
like, as long as it exposes and communicates through a C99 header. In particular, you can write the
implementation in C++ if you want to. (At Our Machinery, we write the implementations in C99.)

### Write your own plugin

To write a plugin you need to implement a `tm_load_plugin()` function that is called whenever the
plugin DLL is loaded/unloaded. In this function, you can interact with various engine interfaces. For
example, you can implement `tm_unit_test_i` to implement unit tests that get run
together with the engine unit tests, you can implement `tm_the_truth_create_types_i` to
extend our data model, The Truth, with your own data types or implement
`tm_entity_create_component_i` to extend our entity model with your own component
types.



The following guides might help you:

- [How to add a new component type]({{base_url}}/gameplay_coding/ecs/write_a_custom_component.html)
- [How to create a new Truth Type]({{base_url}}/the_truth/custom_truth_type.html)
- [How to write a tab]({{tutorials}})
- [How to write unit tests]({{base_url}}qa_pipeline/how_to_write_unit_tests.html)
- [How to write integration tests]({{base_url}}qa_pipeline/how_to_write_integration_tests.html)



The Engine provides an easy way to create plugins for you via the **File -> New Plugins** menu. There you can choose default plugin templates. They come with default files:

![custom tab folder view](https://www.dropbox.com/s/jhrqv8t8bbhr20u/tm_tut_new_tab.png?dl=1)

*The folder structure for a custom tab called `custom_tab`.*



- `premake5.lua` - Your build configuration, on Windows it will generate a `.sln` file for you.
- `libs.json` - Defines the binary dependencies of your projects. `tmbuild` will automatically download them for you.
- `*.c` - Your source file. It contains the sample template code to give you some guidance on what is needed.
- `build.bat` / `build.sh` - quick build files to make building simpler for you.

> **Note:** By default the plugin will not be copied into your Engine's `plugins` folder. You can modify the `premake` file or copy it manually in the folder. You can also make use of a Plugin Asset.

### Structure of a plugin

Every plugin has `tm_load_plugin()` as its entry point, in there we register everything we need to register to the Engines Plugin System. It is important that you do not execute heavy code in this function or rely on other plugins, since they might not be loaded yet! This function is just there to perform load and register operations.

#### Where does my gameplay code live?

Your gameplay lives within the [Systems / Engines]({{base_url}}/gameplay_coding/ecs/index.html) of the ECS or in the [Simulation Entry]({{base_url}}gameplay_coding/simulation_entry.html) and they have their own entry points.

#### How do I update my tool / tab content?

- The `tm_tab_vt` defines three functions for your tab to be updated:
  - `tm_tab_vt.ui()` - Callback for drawing the content of the tab into the specified rect.
  - `tm_tab_vt.ui_serial()` - *Optional.* If implemented, called from the main UI job once all parallel UI rendering (fork/join) has finished. This can be used for parts of the UI that needs to run serially, for example because they call out to a non-thread-safe function.
  - `tm_tab_vt.hidden_update()` - *Optional*. If the tab wants to do some processing when it is *not* the selected tab in its tabwell, it can implement this callback. This will be called for all created tabs whose content is currently *not* visible.

For more information follow the ["Write a tab"]({{tutorials}}) walkthrough.

#### Plugin callbacks (Init, Shutdown, Tick)

The plugin system provides also for plugin callbacks. **It is recommended to rely on these calls as little as possible.** You should not rely on those for your gameplay code!

- `tm_plugin_init_i` - Is typically called as early as possible after all plugins have been loaded.

> **Note:** It is not called when a plugin is reloaded.

- `tm_plugin_shutdown_i` - Is typically be called as early as possible during the application shutdown sequence

> **Note:** Is not called when a plugin is reloaded.

- `tm_plugin_tick_i` - Is typically called as early as possible in the application main loop “tick”.

They are stored in the `foundation/plugin_callbacks.h`.   

#### How do I deal with static variables?

The use of static variables in DLLs can be problematic, because when the DLL is reloaded, the new instance of the DLL will get a new freshly initialized static variable, losing whatever content the variable had before reload. The `tm_api_registry_api` provides a way to solve this issue:  `tm_api_registry_api.static_variable()`

By using this function instead of defining it globally, the variable data is saved in permanent memory.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/static_variable.c)}}
```



### Write your own API

You can also create your own APIs that other plugins can query for. If you create your own APIs, you
want to define them in your header file, so that other plugins can `#include` it and know how to
call your APIs. 

> Note that if you are not defining your own APIs, but just implementing some of the engine's ones, your plugin typically doesn't need a header file.

**my_plugin.h:**

~~~c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_api.h)}}
~~~

**my_plugin.c:**

~~~c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/my_plugin.c)}}
~~~

When The Machinery loads a plugin DLL, it looks for the `tm_load_plugin()` function and calls it. If it can't find the function, it prints an error message. We store the API registry pointer in a static variable so that we can use it everywhere in our DLL.
We also `tm_get_api()` some of the API pointers that we will use frequently and store them in static variables so that we don’t have to use the registry to query for them every time we want to use them. Finally, we add our own API to the registry, so others can query for and use it.

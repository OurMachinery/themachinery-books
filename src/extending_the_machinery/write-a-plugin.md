# My first plugin

This walkthrough shows you how to create your first plugin.

- How to create a plugin from scratch?
- What are the parts a plugin contains?
- Writing a basic API.
- Writing a basic Interface.
- Making use of Plugin Callbacks.
- How to build a plugin?
- What is the difference between an Engine Plugin and a Plugin Asset?

**Table of Content**

* {:toc}


## Programming in C

*The Machinery* uses C99 as its interface language. I.e., all the header files that you use to communicate with *The Machinery* are C99 header files, and when you write a plugin, you should expose C99 headers for your APIs. The *implementation* of a plugin can be written in whichever language you like, as long as it exposes and communicates through a C99 header. In particular, you can write the implementation in C++ if you want to. (At Our Machinery, we write the implementations in C99.)

>  **Note:** Not used to C? No problem we have a collection of extra resources to work with C. [Introduction to C]({{base_url}}/getting_started/introduction_to_c.html)



## Basic Plugin Template

The Engine provides an easy way to create plugins for you via the **file -> New Plugins** menu. There you can choose default plugin templates. Let us choose the minimal plugin. They come with default files:

![](https://www.dropbox.com/s/jhrqv8t8bbhr20u/tm_tut_new_tab.png?dl=1)

*In this case, we choose the Tab template. The only difference is that the `custom_tab` would be `minimal`.*

*The folder structure for a minimal is called minimal.*

- premake5.lua - Your build configuration, on Windows it will generate a .sln file for you.
- libs.json - Defines the binary dependencies of your projects. tmbuild will automatically download them for you.
- *.c - Your source file. It contains the sample template code to guide you on what is needed.
- build.bat / build.sh - quick build files to make building simpler for you.

### What do we have?



#### Premake5

We are using [Premake](https://premake.github.io/) for our meta-build system generator at Our Machinery. This file defines our plugin binary dependencies and builds options for all the Machinery platforms. Premake generates the actual build scripts that we then build with tmbuild, our one-click build tool. More on tmbuild [here]({{base_url}}build_tools/tmbuild.html).

We recommend you to use one single premake file that manages all your plugins. Having a main premake file avoids going into each project folder to build your project. As recommended in the chapter [Project Setup: Possible folder structure for a project]({{base_url}}getting_started/project_setup.html#possible-folder-structure-for-a-project), we also recommend separating your plugins into subfolders. 

> **Note:** The current plugin templates always create all metafiles directly for you, but you can just adjust the main premake file and delete the other ones. This workflow is in review.

In the Book Chapter [Premake]({{base_url}}build_tools/premake.html) you can find more in-depth information about the premake file. 



#### Libs.json 

This file tells tmbuild what kind of binary dependencies you have and what versions you need. tmbuild will automatically download them for you. For more information on the libs.json file, read its [chapter]({{base_url}}/build_tools/libs_json_reference.html).



#### The Build Scripts

Every plugin that is generated with the engines comes with a `build.bat` or `build.sh` at the moment. They are here to help you with your workflow. Whenever you execute them for the first time (double click on them) the script will ask you if you want your plugin to be copied into the plugins folder or if you want a plugin asset. If you decide to create a plugin asset, you need to import the Shared Lib once into your project and then use the Import Change option. More infos on Plugin Asset [here]({{base_url}}extending_the_machinery/plugin-assets.html).

*What is the difference between a Plugin Asset and an Engine Plugin?*

The significant difference is that a plugin asset is an imported Shared Library that lives within your project as a binary data blob. A plugin asset means it is only available within this project and not within other projects. On the other hand, an Engine plugin lives in the engines plugin folder and is available within all projects. More on the difference [here]({{base_url}}/extending_the_machinery/the_plugin_system.html).

#### Source Code

Your actual plugin code lives within the source files within Source Files and header files that help the outside world to make use of the plugin. Every plugin has one entry point. This is the source file that contains the `tm_load_plugin` function.

#### Entry Point

The `tm_load_plugin()` function is our entry point.  In this function, we get access to the API Registry. All our APIs or Interfaces are living within this API.

>  The difference is that APIs only have a single implementation, whereas interfaces can have many implementations. For more information: Check the [Plugin System Chapter]({{base_url}}extending_the_machinery/the_plugin_system.html).

We can register everything we need to register to the Engines Plugin System. You mustn't execute heavy code in this function or rely on other plugins since they might not be loaded yet! This function is just there to perform load and register operations.

 It is not recommended to use this function to initialize and deinitialize data. For such things, we recommend using the `init` or `shutdown` call-back, especially since they are guaranteed to be only called when an initialization or a shutdown happens. This is in contrast to the `tm_load_plugin()` since this function is also called on reload.

> More about hot reload here: [Hot-Reloading]({{base_url}}/extending_the_machinery/hot-reloading.html)



### Plugin callbacks (Init, Shutdown, Tick)

The plugin system also provides for plugin call-backs. **It is recommended to rely on these calls as little as possible.** You should not rely on those for your gameplay code!

`tm_plugin_init_i` - This is typically called as early as possible after all plugins have been loaded.

> **Note:** It is not called when a plugin is reloaded.

`tm_plugin_shutdown_i` - Is typically be called as early as possible during the application shutdown sequence

> **Note:** It is not called when a plugin is reloaded.

`tm_plugin_tick_i` - This is typically called as early as possible in the application main loop “tick”.

>  They are stored in the `foundation/plugin_callbacks.h`. 



## Our very first API - The Command API

This API shall allow us to register commands in any plugin and execute them later if needed.

In our first API, we want to have a function that creates an API context that we need to initialize and deinitialize at the end. Moreover, we want to create an interface that we can use to register commands that you can execute via the Command API. Since requesting all commands every time might be slow, we want to cache them at the beginning of the plugin and at the end. Also, on reload.

> Note: This might not be the best design choice, e.g., thread safety, but this works for demonstration purposes. *PS: Treat this like you would treat slide code.*



### Write your own API

Let us extend the current minimal plugin and add API. API's are only useful if they can be used from the outside. Therefore a header file is needed.

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

### Basic Steps towards the Command API

To be added...

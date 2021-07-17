## Writing a plugin

This walkthrough show you how to extend the engine with a custom plugin.

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



## Use a example "Pong Tab"

The easiest way to build a plugin is to start with an existing example. There are three places where
you can find plugin samples:

1. The `samples` folder in the SDK has a number of plugin samples.

2. The *All Sample Projects* package in the *Download* tab has a `plugins` folder with some small
   samples.

3. You can create a new plugin with the menu command **File > New Plugin**. This will create a
   new `.c` file for the plugin together with some helper files for compiling it.

The distribution already comes with pre-built .dlls for the sample plugins, such as
`bin/plugins/tm_pong_tab.dll`. You can see this plugin in action by selecting **Tab > Pong** in the
editor to open up its tab:

![Pong tab.](https://www.dropbox.com/s/hats2jgr3wroahz/pong-tab.png?dl=1)

### Build Requirements

To build the sample plugins (and your own) you need three things:

1. You need to have Visual Studio 2019 installed including the MS C++ Build Tools on your computer.
   Note that the Community Edition works fine.
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
   variable to use a shared `libs` dir for all your projects.)
2. Run `premake5` to create a Visual Studio project from the `premake5.lua` script.
3. Build the Visual Studio project to build the plugin.

> **Note:** You can learn more about [tmbuild]({{base_url}}helper_tools/tmbuild.html) in its own section.

In order to write a plugin, it is useful to understand a little bit about how the plugin system in *The
Machinery* works.

## Programming in C

*The Machinery* uses C99 as its interface language. I.e., all the header files that you use to
communicate with *The Machinery* are C99 header files, and when you write a plugin you should expose
C99 headers for your APIs. The *implementation* of a plugin can be written in whichever language you
like, as long as it exposes and communicates through a C99 header. In particular, you can write the
implementation in C++ if you want to. (At Our Machinery, we write the implementations in C99.)

### Write your own plugin

To write a plugin you need to implement a `tm_load_plugin()` function that is called whenever the
plugin DLL is loaded/unloaded. In this function, you can interact with various engine interfaces. For
example, you can implement `TM_UNIT_TEST_INTERFACE_NAME` to implement unit tests that get run
together with the engine unit tests, you can implement `TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME` to
extend our data model, The Truth, with your own data types or implement
`TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME` to extend our entity model with your own component
types.

### Write your own API

You can also create your own APIs that other plugins can query for. If you create your own APIs, you
want to define them in your header file, so that other plugins can `#include` it and know how to
call your APIs. Note that if you are not defining your own APIs, but just implementing some of the
engine's ones, your plugin typically doesn't need a header file:

**my_plugin.h:**

~~~c
#include "foundation/api_types.h"

#define MY_API_NAME "my_api"

struct my_api
{
    void (*foo)(void);
};
~~~

**my_plugin.c:**

~~~c
static struct tm_api_registry_api *tm_global_api_registry;
static struct tm_error_api *tm_error_api;
static struct tm_logger_api *tm_logger_api;

#include "my_plugin.h"

#include "foundation/api_registry.h"
#include "foundation/error.h"
#include "foundation/log.h"
#include "foundation/unit_test.h"

static void foo(void)
{
    // ...
}

static struct my_api *my_api = &(struct my_api) {
    .foo = foo,
};

static void my_unit_test(tm_unit_test_runner_i *tr, struct tm_allocator_i *a)
{
    // ...
}

static struct tm_unit_test_i *my_unit_test = &(struct tm_unit_test_i) {
    .name = "my_api",
    .test = my_unit_test,
};

TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    tm_global_api_registry = reg;

    tm_error_api = reg->get(TM_ERROR_API_NAME);
    tm_logger_api = reg->get(TM_LOGGER_API_NAME);

    tm_set_or_remove_api(reg, load, MY_API_NAME, my_api);

    tm_add_or_remove_implementation(reg, load, TM_UNIT_TEST_INTERFACE_NAME, my_unit_test);
}
~~~

When The Machinery loads a plugin DLL, it looks for the `tm_load_plugin()` function and calls it.
If it can't find the function, it prints an error message.

We store the API registry pointer in a static variable so that we can use it everywhere in our DLL.
We also `get()` some of the API pointers that we will use frequently and store them in static
variables so that we don’t have to use the registry to query for them every time we want to use
them. Finally, we add our own API to the registry, so others can query for and use it.


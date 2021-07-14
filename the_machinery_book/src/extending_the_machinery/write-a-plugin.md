## Writing a plugin

This walkthrough show you how to extend the engine with a custom plugin.

You will learn about:

- What is needed to write a plugin
- How to write a plugin

This walk through expects you to have the basic understanding about the plugin system. Otherwise you can read more [here]({{base_url}}/the_machinery_book/extending_the_machinery/the_plugin_system.html).

The Machinery is built around a plugin model. All features, even the built-in ones, are provided
through plugins. You can extend The Machinery by writing your own plugins. When The Machinery
launches, it loads all the plugins named `tm_*.dll` in its `plugins/` folder. If you write your own
plugins, name them so that they start with `tm_` and put them in this folder, they will be loaded
together with the built-in plugins.

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

To build the sample plugins (and your own) you need three things:

1. You need to have Visual Studio 2019 installed including the MS C++ Build Tools on your computer.
   Note that the Community Edition works fine.

2. You need to set the `TM_SDK_DIR` environment variable to the path of the SDK package that you
   installed on your computer. When you compile a plugin, it looks for The Machinery headers in the
   `%TM_SDK_DIR%/headers` folder.

3. You need the `tmbuild.exe` from the SDK package. `tmbuild.exe` does all the steps needed to
   compile the plugin. Put it in your `PATH` or copy it to your plugin folder so that you can run it
   easily from the command line.

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

In order to write a plugin, it is useful to understand a little bit about how the plugin system in *The
Machinery* works.

*The Machinery* uses C99 as its interface language. I.e., all the header files that you use to
communicate with *The Machinery* are C99 header files, and when you write a plugin you should expose
C99 headers for your APIs. The *implementation* of a plugin can be written in whichever language you
like, as long as it exposes and communicates through a C99 header. In particular, you can write the
implementation in C++ if you want to. (At Our Machinery, we write the implementations in C99.)

*The Machinery* is organized into individual APIs that can be called to perform specific tasks. A
plugin is a DLL that exposes one or several of these APIs. In order to implement its functionality,
the plugin may in turn rely on APIs exposed by other plugins.

A central object called the *API registry* is used to keep track of all the APIs. When you want to
use an API from another plugin, you ask the API registry for it. Similarly, you expose your APIs to
the world by registering them with the API registry.

This may seem a bit abstract at this point, so let’s look at a concrete example, `unicode.h` which
exposes an API for encoding and decoding Unicode strings:

~~~c
// This header has been abridged and commented from the original to make things
// clearer.

// Include standard header.
#include "api_types.h"

// Forward declarations.
struct tm_temp_allocator_i;

// Name of this API in the registry.
#define TM_UNICODE_API_NAME "tm_unicode_api"

// Unicode helper functions.
struct tm_unicode_api
{
    // Encodes the `codepoint` as UTF-8 into `utf8` and returns a pointer to the
    // position where to insert the next codepoint. `utf8` should have room for at
    // least four bytes (the maximum size of a UTF-8 encoded codepoint).
    char *(*utf8_encode)(char *utf8, uint32_t codepoint);

    // Decodes and returns the first codepoint in the UTF-8 string `utf8`. The string
    // pointer is advanced to point to the next codepoint in the string. Will generate
    // an error message if the string is not a UTF-8 string.
    uint32_t (*utf8_decode)(const char **utf8);

    // ...
};
~~~

Let’s go through this.

First, the code includes `<api_types.h>`. This is a shared header with common type declarations, it
includes things like `<stdbool.h>` and `<stdint.h>` and also defines a few *The Machinery* specific
types, such as `tm_vec3_t`.

In *The Machinery* we have a rule that header files can't include other header files (except
for `<api_types.h>`). This helps keep compile times down, but it also simplifies the structure of the
code. When you read a header file you don’t have to follow a long chain of other header files to understand
what is happening.

Next follows a block of forward struct declarations (in this case only one).

Next, we have the name of this API defined as a constant `TM_UNICODE_API_NAME`, followed by the
`struct tm_unicode_api` that defines the functions in the API.

To use this API, you would first use the API registry to query for the API pointer, then using that
pointer, call the functions of the API:

~~~c
struct tm_unicode_api *tm_unicode_api =
    (struct tm_unicode_api *)tm_global_api_registry->get(TM_UNICODE_API_NAME);

tm_unicode_api->utf8_encode(utf8, codepoint);
~~~

The different APIs that you can query for and use are documented in their respective header files,
and in the `apidoc.md.html` documentation file (which is just extracted from the headers). Consult
these files for information on how to use the various APIs that are available in *The Machinery.*

In addition to APIs defined in header files, *The Machinery* also contains some header files with
inline functions that you can include directly into your implementation files. For example
`<math.inl>` provides common mathematical operations on vectors and matrices, while `<carray.inl>`
provides a “stretchy-buffer” implementation (i.e. a C version of C++’s `std::vector`).

To write a plugin you need to implement a `tm_load_plugin()` function that is called whenever the
plugin DLL is loaded/unloaded. In this function, you can interact with various engine interfaces. For
example, you can implement `TM_UNIT_TEST_INTERFACE_NAME` to implement unit tests that get run
together with the engine unit tests, you can implement `TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME` to
extend our data model, The Truth, with your own data types or implement
`TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME` to extend our entity model with your own component
types.

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

We also add an *implementation* of the unit test *interface* to the registry. The API registry has
support for both APIs and interfaces. The difference is that APIs only have a single implementation,
whereas interfaces can have many implementations. For example, all code that can be unit-tested
implements the unit test interface. Unit test programs can query the API registry to find all these
implementations and run all the unit tests.

To extend the editor you add implementations to the interfaces used by the editor. For example, you
can add implementations of the `TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME`  in order to create new
data types in The Truth, and add implementations of the `TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME`
in order to define new entity components. See the sample plugin examples.

It does not matter in which order the plugins are loaded. If you query for a plugin that hasn’t yet
been registered, you get a pointer to a nulled struct back. When the plugin is loaded, that struct
is filled in with the actual function pointers. As long as you don’t *call* the functions before the
plugin that implements them has been loaded, you are good. (You can test this by checking for NULL
pointers in the struct.)

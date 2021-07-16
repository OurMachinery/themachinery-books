# The plugin system

*The Machinery* is built around a plugin model. All features, even the built-in ones, are provided through plugins. You can extend *The Machinery* by writing your own plugins.

When *The Machinery* launches, it loads all the plugins named `tm_*.dll` in its `plugins/` folder. If you write your own plugins, name them so that they start with `tm_` and put them in this folder, they will be loaded together with the built-in plugins.

**Table of Content**

* auto-gen TOC;
{:toc}

## About API's

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

## About Interfaces

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

## Per project plugins

The Engine supports per project plugins through *Plugin Assets*. A Plugin Asset is an asset in the
Asset Browser that holds a plugin.

To create a plugin asset in a particular project, just drop the `.dll` into the Asset Browser
(or use **Import...**). Every time you open the project, the plugin will be loaded.

> **Note**: For security reasons, if you open a project containing plugins, you will be asked
> whether you want to allow the plugins to run or not. Plugins aren't sandboxed, they have full
> access to your machine. So you should only allow project plugins to run if you trust the author
> of the plugin.

When selecting a plugin asset in the asset browser the properties tab will show the following:

![](https://ourmachinery.com/images/tutorials/plugin__properties.png)

If you check the ☒ **Import when changed** checkbox, The Machinery will re-import and reload the
plugin every time it detects a change. You can use this to hot-reload your project plugins.

> **Note:** since The Machinery APIs change with each release version, a plugin DLL built for one
> specific version is unlikely to work with another version. Thus, to open a project with plugin
> DLLs, you should make sure that your version matches the version the DLL was built for. In the
> future, when The Machinery is out of beta, we will provide more stable APIs that will work across
> multiple releases.
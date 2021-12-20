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
{{$include {TM_SDK_DIR}/foundation/unicode.h:0:97}}
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

Next, we have the name of this API defined as a constant `tm_unicode_api`, followed by the
`struct tm_unicode_api` that defines the functions in the API.

To use this API, you would first use the API registry to query for the API pointer, then using that
pointer, call the functions of the API:

~~~c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/plugins/get_api_demo.c)}}
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
can add implementations of the `tm_the_truth_create_types_i`  in order to create new
data types in The Truth, and add implementations of the `tm_entity_create_component_i`
in order to define new entity components. See the sample plugin examples.

It does not matter in which order the plugins are loaded. If you query for a plugin that hasn’t yet
been registered, you get a pointer to a nulled struct back. When the plugin is loaded, that struct
is filled in with the actual function pointers. As long as you don’t *call* the functions before the
plugin that implements them has been loaded, you are good. (You can test this by checking for NULL
pointers in the struct.)

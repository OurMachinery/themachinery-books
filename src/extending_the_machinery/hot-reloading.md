# Hot-Reloading

We support hot-reloading of plugins while *The Machinery* is running. This allows you to work on a
plugin and see the changes in real-time without having to shut down and restart the application
between each change to your code.

Hot-reloading is enabled by default, but can be disabled with the `--no-hot-reload` parameter.

When a reload happens, the function pointers in the plugin's API struct are replaced with function
pointers to the new code. Since clients hold pointers to this struct, they will use the new function
pointers automatically -- they don't have to re-query the system for the API.

Note that hot-reloading is not magical and can break in a lot of situations. For example, if you
remove functions in the API or change their parameters, any clients of your API will still try to
call them using the old parameter lists, and things will most likely crash. Similarly, if a client
has stashed away a function pointer to one of your API functions somewhere, such as in a list of
callbacks, there is no way for us to patch that copy and it will continue to call the old code.
Also, if you make changes to the layout of live data objects (such as adding or removing struct
fields) things will break because we make no attempts to transfer the data to the new struct
format.

But adding or removing static functions, or changing the code inside functions should work without
problems. We find hot-reloading to be a big time saver even if it doesn't work in all circumstances.

If you want to use global variables in your DLL you should do so using the
`tm_api_registry_api->static_variable()` function in your `tm_load_plugin()` code. If you just
declare a global variable in your .c file, that variable will be allocated in the DLLs memory space
and when the DLL is reloaded you will lose all changes to the variable. When you use
`static_variable()`, the variable is allocated on the heap, and its content is preserved when the
DLL is reloaded.

If you are using hot-reloading together with a debugger on Windows, be aware that the debugger will
lock `.pdb` files which will prevent you from rebuilding your code. The suggested workflow is
something like this:

* Detach the debugger if it's currently attached.
* Rebuild your DLL and fix any compiler bugs.
* When the DLL is built successfully, The Machinery will automatically reload it.
* If you need to continue debugging, re-attach the debugger.

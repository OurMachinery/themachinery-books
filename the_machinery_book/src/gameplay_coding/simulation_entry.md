## Simulation Entry (writing gameplay code in C)

This walkthrough will show you how to create a _simulation entry_ and what a simulation entry is.

If you wish to program gameplay using C code, then you need some way for this code to execute. You can either make lots of entity components that do inter-component communication, but if you want a more classic monolithic approach, then you can use a simulation entry.

In order for your code to execute using a simulation entry you need two things. Firstly you need an implementation of the Simulation Entry interface, `tm_simulation_entry_i` (see `simulation_entry.h`) and secondly you need a Simulation Entry Component attached to an entity.

Define a `tm_simulation_entry_i` in a plugin like this:

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/gameplay_code/simulation_entry.c:52:59}}
```

Where `start`, `stop` and `tick` are functions that are run when the simulation starts, stop and each frame respectively. Make sure that `id` is a unique identifier.

> **Note:** There is also a plugin template available that does this, see `File -> New Plugin -> Simulation Entry` with The Machinery Editor. 

> **Note:** to generate the `TM_STATIC_HASH` you need to run `hash.exe` or `tmbuild.exe --gen-hash` for more info open the [hash.exe guide]({{the_machinery_book}}/helper_tools/hash.html)

When your plugin loads (each plugin has a `tm_load_plugin` function), make sure to register this implementation of `tm_simulation_entry_i` on the `tm_simulation_entry_i` interface name, like so:

```c
tm_add_or_remove_implementation(reg, load, tm_simulation_entry_i, &simulation_entry_i);
```

When this is done and your plugin is loaded, you can add a Simulation Entry Component to any entity and select your registered implementation. Now, whenever you run a simulation (using Simulate Tab or from a Published build) where this entity is present, your code will run.

The same Simulation Entry interface can be used from multiple Simulation Entry Components and their state will _not_ be shared between them.

> **Note:** For more in-depth examples, we refer to the gameplay samples, they all use Simulation Entry.

## What happens under the hood?

When the Simulation Entry Component is loaded within the Simulate Tab or Runner, it will set up an entity system. This system will run your start, stop and tick functions. You may then ask, what is the difference between using a Simulation Entry and just registering a system from your plugin? The answer is the lifetime of the code. If you register a system from your plugin, then that system will run no matter what entity is spawned whereas the Simulation Entry Component will add and remove the system that runs your code when the entity is spawned and despawned.



## Example: Source Code

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/gameplay_code/simulation_entry.c}}
```


## Simulate Entry (writing gameplay code in C)

This walkthrough show you how to write a simulate entry and what a simulate entry is.

If you wish to program gameplay using C code, then you need some place where this code execution
enters. This is provided by the Simulate Entry interface. In order to use it, begin by implementing
the the interface `tm_simulate_entry_i` (see `simulate_entry.h`). Make an object of the
`tm_simulate_entry_i` struct like this (see any of the gameplay samples for examples with more
context):

```c
static tm_simulate_entry_i simulate_entry_i = {
    .id = TM_STATIC_HASH("tm_my_game_simulate_entry", 0xe240e2d67a0aa93ULL),
    .display_name = TM_LOCALIZE_LATER("My Game Simulate Entry"),
    .start = start,
    .stop = stop,
    .tick = tick,
};
```

where `start()`, `stop()` and `tick()` are the functions that you want called when the game starts, ends
and each frame respectively. Make sure that `id` is unique. When your plugin loads, make sure to
register this implementation of `tm_simulate_entry_i` on the `TM_SIMULATE_ENTRY_INTERFACE_NAME`
interface name, like so:

```c
tm_add_or_remove_implementation(reg, load, TM_SIMULATE_ENTRY_INTERFACE_NAME, &simulate_entry_i);
```

After you've done this, create a `Simulate Entry` asset in a directory next to one of your scene
entities:

![Creating a Simulate Entry asset](https://www.dropbox.com/s/qchhejkfbbjfw7h/create-new-simulate-entrry.png?dl=1)

When you inspect the the properties of this new `Simulate Entry` asset, have a look in the
Simulate Entry dropdown menu. Given that you registered your implementation of `tm_simulate_entry_i`
correctly, it should appear in this list.



## How will the Engine determine which one to pick?

Now, whenever you start simulating a certain entity, such as your main game world, the Simulate Tab
will look in the directory next to the entity you're simulating and check if there is a Simulate
Entry asset there. If there is, it will use the referenced `tm_simulate_entry_i` implementation in
order to enter into gameplay code. If the Simulate Tab fails to find a Simulate Entry asset in the
same directory, it will look in each parent directory. This makes it possible to put a "catch-all"
Simulate Entry in the root directory of your project. You can also put entities that need different
Simulate Entry code in separate directories, with a Simulate Entry asset next to each, which can
reference different implementations of the the `tm_simulate_entry_i` interface.
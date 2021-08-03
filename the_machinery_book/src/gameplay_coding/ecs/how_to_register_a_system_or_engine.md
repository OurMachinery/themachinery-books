# Registering a System or an Engine

To register Systems/Engines, you need to provide a register function to the `TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME` interface. This function has the signature:

```c
static void register_or_system_engine(struct tm_entity_context_o *ctx){}
```

For more information check the `tm_entity_register_engines_i` .

Whenever the Machinery creates an Entity Context, it calls this function and registers all your Systems / Engines to this context.

> The Entity context is the world in which all your entities exist.

For Engines, you pass an instance of the `tm_entity_system_i` to the register function.

```c
// example:
static void register_or_system_engine(struct tm_entity_context_o *ctx){
    const tm_engine_i movement_engine = {
        .ui_name = "movement_engine",
        .hash = TM_STATIC_HASH("movement_engine", 0x336880a23d06646dULL),
        .num_components = 4,
        .components = { keyboard_component, movement_component, transform_component, mover_component },
        .writes = { false, false, true, true },
        .excluded = { no_movement },
        .num_excluded = 1,
        .update = movement_update,
        .inst = (tm_engine_o *)ctx,
    };
    tm_entity_api->register_engine(ctx, &movement_engine);
}
```



For Systems, you pass an instance of the `tm_engine_i` to the register function.

```c
static void register_or_system_engine(struct tm_entity_context_o *ctx){
    const tm_entity_system_i winning_system = {
        .ui_name = "winning_system_update",
        .hash = TM_STATIC_HASH("winning_system_update", 0x8f8676e599ca5c7aULL),
        .update = winning_system_update,
        .before_me[0] = TM_STATIC_HASH("maze_generation_system", 0x7f1fcbd9ee85c3cfULL),
        .exclusive = true,
        .inst = (tm_entity_system_o *)tm_entity_api->component_manager(ctx, tag_component),
    };
    tm_entity_api->register_system(ctx, &winning_system);
}
```

In the above example the scheduler will schedule this system after the `maze_generation_system` system! Since we did not provide any further information in `.writes` or in `.components` the scheduler has no other information to work with. In this case its best to not write to anything!

*Example load function:*


```c
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
    // other code ...
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME, register_or_system_engine);
}
```



## Register your system or engine to the Editor

You can use the `TM_ENTITY_EDITOR_REGISTER_ENGINES_INTERFACE_NAME` to register your engine or system to a entity context that runs only in the Editor. This might be good for components that shall only be used in the Editor.

The function signature is the same as the for the other interface!



### Register systems & engines outside of the load function

You also can register your System/Engine outside of the load function where ever you have access to the correct Entity Context.

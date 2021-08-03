# Filtering Entities

The Machinery knows 2 kind of ways to Tag Entities:

1. using the `Tag Component`
2. using a `Tag Component` to filter the Entity Type's



**Table of Content**

* auto-gen TOC;
{:toc}
## Filtering Entities 

In a Engine (`tm_engine_i`) you can define the `.excluded` filed. This tells the scheduler that this engine shall **not** run on any entity type that contains these components.

Let us assume we have the following entities:

```
#1 Entity:
- Component A
- Component B
- Component C
#2 Entity:
- Component A
- Component B
- Component D
```

Now we have a Engine that shall operate on `(Component A,Component B)` but we do not want it to operate on entities with `Component D` we could just check in our update loop:

```c
// Runs on (component a, comnponent b)
static void engine_update__custom_component(tm_engine_o* inst, tm_engine_update_set_t* data)
{
    struct tm_entity_context_o* ctx = (struct tm_entity_context_o*)inst;
// code
    for (tm_engine_update_array_t* a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
//.. code
        for (uint32_t i = 0; i < a->n; ++i) {
            // if the entity has no component it returns a NULL pointer 
            if(!tm_entity_api->get_component_by_hash(ctx,a->entities[i],TM_TYPE_HASH__COMPONENT_D)){
                //..code
            }
        }
    }
//...code
}
```

or we could define a component mask and use this to filter but both methods are slow. This is because `get_component_by_hash` or `get_component` require us to look up internally the entity + the components and search for them. Its aka a random memory access! 

To avoid all of this we can just tell the engine to ignore all entity types which contain the `component_d` via the `.excluded` fied in the `tm_engine_i`.

```` c
    const tm_engine_i my_system = {
        .ui_name = "my_system",
        .hash = TM_STATIC_HASH("movement_engine", 0x336880a23d06646dULL),
        .num_components = 2,
        .components = { component_a, component_b },
        .writes = { false, true},
        .excluded = { component_d },
        .num_excluded = 1,
        .update = movement_update,
        .inst = (tm_engine_o *)ctx,
    };
    tm_entity_api->register_engine(ctx, &movement_engine);
````

## Filtering Entities by using Tag Components

> **Note**: You can define a `Tag` Component which should not be confused with the `Tag Component`. A tag component is a simple typedef of a `unit64_t` (or something else) or an empty struct in C++ to a component without properties. The function of this component is it to modify the Entity Type / Archetype to group entities together with them.For more information see the [Tagging Entities]({{the_machinery_book}}/gameplay_coding/ecs/tagging_entities.html) Chapter.

You have a Movement / Input System which should always work. At some point you do not want a entity to receive any input. 

*Solution 1*

To solve this issue you could remove the Movement Component but that would be annyoing because you would lose it state, which might be important.

*Better Solution*

First you define the component:

```c
#define TM_TT_TYPE__PLAYER_NO_MOVE_TAG_COMPONENT "tm_player_no_move_t"
#define TM_TT_HASH__PLAYER_NO_MOVE_TAG_COMPONENT TM_STATIC_HASH("tm_player_no_move_t", 0xc58cb6ade683ca88ULL)
static void component__create(struct tm_entity_context_o *ctx)
{
       tm_component_i component = (tm_component_i){
        .name = TM_TT_TYPE__PLAYER_NO_MOVE_TAG_COMPONENT,
        .bytes = sizeof(uint64_t), // since we do not care of its content we can just pick any 8 byte type
    };
    tm_entity_api->register_component(ctx, &component);
}
}
```

Then you filter in your update for the Input Engine/ Movement Engine any Entity that has a No Movement Tag:

```c
    const tm_engine_i movement_engine = {
        .ui_name = "movement_engine",
        .hash = TM_STATIC_HASH("movement_engine", 0x336880a23d06646dULL),
        .num_components = 3,
        .components = { movement_component, transform_component, mover_component },
        .writes = { false, true, true },
        .excluded = { no_movement_tag_component },
        .num_excluded = 1,
        .update = movement_update,
        .inst = (tm_engine_o *)ctx,
    };
    tm_entity_api->register_engine(ctx, &movement_engine);
```

When ever another `engine/system` decides that a entity should not move anymore it just adds a `no_movement_tag_component` to the entity.

```c
static void my_other_system(tm_engine_o *inst, tm_engine_update_set_t *data)
{
    // code ..
	for (tm_engine_update_array_t *a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
    // code...
    for (uint32_t x = 0; x < a->n; ++x) {
        // code...
        if(player_should_not_walk_anymore){
             tm_entity_api->add_component(ctx, d->entities[i], no_movement);
        }
    }
    }
}
```

As you an see the Movement Engine will now update all other entities in the game which do not have the No Movement Tag.
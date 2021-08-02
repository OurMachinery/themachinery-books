# Tagging and Filtering Entities

The Machinery knows 2 kind of ways to Tag Entities:

1. using the `Tag Component`
2. using a `Tag Component` to filter the Entity Type's



**Table of Content**

* auto-gen TOC;
{:toc}
## Using the Tag Component

The difference is that the first solution can be used via the `tag_component_api` and you can add Tags via the Editor to any Entity that has a Tag Component. Later on in your System or Engine you can access the Taged Entity.

> **Note:** This is not the most performant solution but a easy way for entities which do not exist many times in the world. Its a nice way to identify one or two specifc entities for some specific logic.

### Adding them via The Editor

You need to select a Entity and **Right Click -> Add Component**

![](https://www.dropbox.com/s/x6pntlc4u0vw9pa/tm_guide_entity_tag_add_component.png?dl=1)

This will add the *Entity Tag* Component. When selected you have the chance to add Tags to the Entity by using a simple auto complete text box. 

**Beaware:** The Engine will create a entity tag folder in your root folder. This is also the place where the Entity Tag API will search for the assets.

![](https://www.dropbox.com/s/ve5lr0e0qcs221e/tm_guide_entity_tag.png?dl=1)

### Adding and Accessing Tags via C

You can also add tags via the `tag_component_api` but you need access to the `Tag Component Manager`. In your System or on Simulate Entry `start()`:

```c
tm_tag_component_manager_o *tag_mgr = (tm_tag_component_manager_o *)tm_entity_api->component_manager(ctx, tag_component);
tm_tag_component_api->add_tag(tag_mgr, my_to_tagged_entity, TM_STATIC_HASH("player", 0xafff68de8a0598dfULL));
```

You can also recive entities like this:

```c
tm_tag_component_manager_o *tag_mgr = (tm_tag_component_manager_o *)tm_entity_api->component_manager(ctx, tag_component);
tm_entity_t upper_bounding_box = tm_tag_component_api->find_first(tag_mgr, TM_STATIC_HASH("upper_bounding_box", 0x1afc9d34ecb740ecULL));
```

And than you can read the data from the entity via `get_component`. This is where you will perform a random look up and this might be slow. Therefore it is mostly recommend to use this for simple interactions where performance is not needed.

> **Note:** Tags do not need to exist in the Asset Browser, therefore you can add any label to the entity. Keep in mind that they will **not** be created in the Asset Browser!



## Tag Components - Entity Type Filter

On the other hand you can define a `Tag` Component which should not be confused with the priviously explained `Tag Component`. A tag component is a simple typedef of a `unit64_t` (or something else) or an empty struct in C++ to a component without properties. The function of this component is it to modify the Entity Type / Archetype to group entities together with them.

*Example:*

You have the following components:

- Component A
- Component B

And 2 systems :

- System A 
- System B

They both shall operate on Component A & B but have different logic based on what the Components represent. To archive this you just add to a Entity a tag component:

```
#1 Entity:
- Component A
- Component B
- My Tag For System A
#2 Entity:
- Component A
- Component B
- My Tag for System A
```

In this example System B would not operate on both Entities if we use the `.excluded` filter to exclude `My Tag For System A` from the System.

### Real World Example:

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
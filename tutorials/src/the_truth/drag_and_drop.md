# Adding Drag and Drop to Assets

This walkthrough shows you how to add a custom asset to the Engine. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/the_plugin_system.html). The goal of this walkthrough is to enable you to drag and drop your asset into the Scene!

You will learn:

- how to use an aspect in practice
- How to extend an already existing asset.
- How to use an entity-component manager.



This walkthrough will refer to the text asset example as the asset we want to extend! If you have not followed it here is the link: [Custom Asset]({{tutorials}}/the_truth/custom_asset/index.html)

**Table of Content**

* auto-gen TOC;
{:toc}


## About aspects

{{#include ../../../the_machinery_book/src/the_truth/aspects.md:2:*}}



## Adding Drag and Drop to our asset

In this example, we are going back to our text asset sample. In that sample, we have the following function to register the asset to the Truth:

```c
// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER },
    };
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__TXT_ASSET, my_asset_properties, TM_ARRAY_COUNT(txt_asset_properties));
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "txt");
    static tm_properties_aspect_i properties_aspect = {
        .custom_ui = properties__custom_ui,
    };
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__PROPERTIES, &properties_aspect);
}
```

We need to make use of the `TM_TT_ASPECT__ASSET_SCENE` aspect. This aspect allows the associated Truth Type to be dragged and dropped to the Scene if wanted! We can find it in the `plugins/the_machinery_shared/asset_aspects.h` header.

### Asset Scene Aspect

This aspect expects an instance of the `tm_asset_scene_api`. When we provide a call-back called

`bool (*droppable)(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t asset);` we tell the scene that we can drag the asset out of the asset browser. We need to return true for this. In this case you need to provide the `create_entity` function. When you drag your asset into the Scene, this function is called by the Engine. In this function, you can create a new entity and attach it to the parent entity ( which might be the world.  If you drag it on top of another entity, you can attach the newly created entity as a child entity to this one. 

Before we can make use of this we need some component to be created for our Text Asset! Lets call it Story Component.

## The story component

Let us create a use case for our text file. Let us assume we wanted to make a very simple story-based game, and all our text files are the basis for our stories. This means we need to create first a story component.

> Note: For more details on how to create a component, follow this [guide]({{the_machinery_book}}/gameplay_coding/ecs/write_a_custom_component.html).

Here we have the whole source code for the story component:

```c
// more apis
static struct tm_entity_api *tm_entity_api;
// more includes
#include <plugins/entity/entity.h>
#include <plugins/the_machinery_shared/component_interfaces/editor_ui_interface.h>
// other types
struct tm_component_manager_o
{
    tm_entity_context_o *ctx;
    tm_allocator_i allocator;
};

// more code

static const char *component__category(void)
{
    return TM_LOCALIZE("Story");
}

static tm_ci_editor_ui_i *editor_aspect = &(tm_ci_editor_ui_i){
    .category = component__category
};

static float properties__component_custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    TM_INIT_TEMP_ALLOCATOR(ta);
    tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(args->tt, TM_TT_TYPE_HASH__ASSET);
    // get all instances of `TM_TT_TYPE_HASH__TXT_ASSET`
    tm_tt_id_t *ids = tm_the_truth_api->all_objects_of_type(args->tt, tm_the_truth_api->object_type_from_name_hash(args->tt, TM_TT_TYPE_HASH__TXT_ASSET), ta);
    tm_tt_id_t *items = 0;
    const char **names = 0;
    tm_carray_temp_push(names, "Select", ta);
    tm_carray_temp_push(items, (tm_tt_id_t){ 0 }, ta);
    for (uint32_t i = 0; i < tm_carray_size(ids); ++i) {
        // we make sure a Asset Type is the owner of the object! This is important since
        // the Asset Truth type has the name field! `TM_TT_PROP__ASSET__NAME`
        tm_tt_id_t owner = tm_the_truth_api->owner(args->tt, ids[i]);
        if (tm_tt_type(owner).u64 == asset_type.u64) {
            // if the owner is a asset we add it's name to our names array and use the id and add it to ower items!
            tm_carray_temp_push(names, tm_the_truth_api->get_string(args->tt, tm_tt_read(args->tt, owner), TM_TT_PROP__ASSET__NAME), ta);
            tm_carray_temp_push(items, ids[i], ta);
        }
    }
    // creates a popup picker and the user can choose what reference they want to put into the property!
    item_rect.y = tm_properties_view_api->ui_reference_popup_picker(args, item_rect, "Asset", NULL, object, TM_TT_PROP__STORY_COMPONENT__ASSET, names, items, (uint32_t)tm_carray_size(items));
    TM_SHUTDOWN_TEMP_ALLOCATOR(ta); // always make sure you call the shutdown function on the temp allocator
    return item_rect.y;
}


// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
// ..other code
    tm_the_truth_property_definition_t story_component_properties[] = {
        [TM_TT_PROP__STORY_COMPONENT__ASSET] = { "story_asset", .type = TM_THE_TRUTH_PROPERTY_TYPE_REFERENCE, .type_hash = TM_TT_TYPE_HASH__TXT_ASSET }
    };
    static tm_properties_aspect_i properties_component_aspect = {
        .custom_ui = properties__component_custom_ui,
    };

    const tm_tt_type_t story_component_type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__STORY_COMPONENT, story_component_properties, TM_ARRAY_COUNT(story_component_properties));
    tm_the_truth_api->set_aspect(tt, story_component_type, TM_CI_EDITOR_UI, editor_aspect);
    tm_the_truth_api->set_aspect(tt, story_component_type, TM_TT_ASPECT__PROPERTIES, &properties_component_aspect);
}
// ..other code
// -- story component
static bool component__load_asset(tm_component_manager_o *man, tm_entity_t e, void *c_vp, const tm_the_truth_o *tt, tm_tt_id_t asset)
{
    struct tm_story_component_t *c = c_vp;
    const tm_the_truth_object_o *asset_r = tm_tt_read(tt, asset);
    tm_tt_id_t id = tm_the_truth_api->get_reference(tt, asset_r, TM_TT_PROP__STORY_COMPONENT__ASSET);
    if (id.u64) {
        tm_tt_buffer_t buffer = tm_the_truth_api->get_buffer(tt, tm_tt_read(tt, id), TM_TT_PROP__MY_ASSET__DATA);
        c->text = tm_alloc(&man->allocator, buffer.size);
        c->size = buffer.size;
        memcpy(c->text, buffer.data, buffer.size);
    }
    return true;
}

static void component__remove(tm_component_manager_o *manager, tm_entity_t e, void *data)
{
    tm_story_component_t *sc = (tm_story_component_t *)data;
    tm_free(&manager->allocator, sc->text, sc->size);
}

static void component__destroy(tm_component_manager_o *manager)
{
    tm_entity_api->call_remove_on_all_entities(manager->ctx, tm_entity_api->lookup_component_type(manager->ctx, TM_TT_TYPE_HASH__STORY_COMPONENT));
    // Free the actual manager struct and the allocator used to allocate it.
    tm_entity_context_o *ctx = manager->ctx;
    tm_allocator_i allocator = manager->allocator;
    tm_free(&allocator, manager, sizeof(tm_component_manager_o));
    tm_entity_api->destroy_child_allocator(ctx, &allocator);
}

static void component__create(struct tm_entity_context_o *ctx)
{
    // Allocate a new manager for this component type (freed in component__destroy).
    tm_allocator_i allocator;
    tm_entity_api->create_child_allocator(ctx, TM_TT_TYPE__STORY_COMPONENT, &allocator);
    tm_component_manager_o *story_manager = tm_alloc(&allocator, sizeof(tm_component_manager_o));

    *story_manager = (tm_component_manager_o){
        .ctx = ctx,
        .allocator = allocator
    };

    tm_component_i component = {
        .name = TM_TT_TYPE__STORY_COMPONENT,
        .bytes = sizeof(struct tm_story_component_t),
        .load_asset = component__load_asset,
        .destroy = component__destroy,
        .remove = component__remove,
        .manager = (tm_component_manager_o *)story_manager
    };
    tm_entity_api->register_component(ctx, &component);
};
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
// other code
    tm_entity_api = reg->get(TM_ENTITY_API_NAME);
// ... other code
    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME, component__create);
}
```



First, we create our component, and we need a way to guarantee that our truth data exists during runtime as well. Therefore, we use the Entity Manager to allocate our Story data and store just a pointer and its size to the allocated data in the Manager.

```c

struct tm_component_manager_o
{
    tm_entity_context_o *ctx;
    tm_allocator_i allocator;
};
static void component__create(struct tm_entity_context_o *ctx)
{
    // Allocate a new manager for this component type (freed in component__destroy).
    tm_allocator_i allocator;
    tm_entity_api->create_child_allocator(ctx, TM_TT_TYPE__STORY_COMPONENT, &allocator);
    tm_component_manager_o *story_manager = tm_alloc(&allocator, sizeof(tm_component_manager_o));

    *story_manager = (tm_component_manager_o){
        .ctx = ctx,
        .allocator = allocator
    };

    tm_component_i component = {
        .name = TM_TT_TYPE__STORY_COMPONENT,
        .bytes = sizeof(struct tm_story_component_t),
        .load_asset = component__load_asset,
        .destroy = component__destroy,
        .remove = component__remove,
        .manager = (tm_component_manager_o *)story_manager
    };
    tm_entity_api->register_component(ctx, &component);
};

```



The most important function here is the `component__load_asset` function, in which we translate the Truth Representation into an ECS representation. We load the text buffer, allocate it with the Manager, and store a pointer in our component. With this, we could create a reference-counted system in which multiple components point to the same story data, and only when the last component goes we deallocate this. Another alternative would be to avoid loading when we create the component, and the story is already allocated.

```c
static bool component__load_asset(tm_component_manager_o *man, tm_entity_t e, void *c_vp, const tm_the_truth_o *tt, tm_tt_id_t asset)
{
    struct tm_story_component_t *c = c_vp;
    const tm_the_truth_object_o *asset_r = tm_tt_read(tt, asset);
    tm_tt_id_t id = tm_the_truth_api->get_reference(tt, asset_r, TM_TT_PROP__STORY_COMPONENT__ASSET);
    if (id.u64) {
        tm_tt_buffer_t buffer = tm_the_truth_api->get_buffer(tt, tm_tt_read(tt, id), TM_TT_PROP__MY_ASSET__DATA);
        c->text = tm_alloc(&man->allocator, buffer.size);
        c->size = buffer.size;
        memcpy(c->text, buffer.data, buffer.size);
    }
    return true;
}
```



When the Entity context gets destroyed, we need to clean up and destroy our Manager. Important that we call `call_remove_on_all_entities` to make sure all instances of the component are gone.

```c
static void component__remove(tm_component_manager_o *manager, tm_entity_t e, void *data)
{
    tm_story_component_t *sc = (tm_story_component_t *)data;
    tm_free(&manager->allocator, sc->text, sc->size);
}

static void component__destroy(tm_component_manager_o *manager)
{
    tm_entity_api->call_remove_on_all_entities(manager->ctx, tm_entity_api->lookup_component_type(manager->ctx, TM_TT_TYPE_HASH__STORY_COMPONENT));
    // Free the actual manager struct and the allocator used to allocate it.
    tm_entity_context_o *ctx = manager->ctx;
    tm_allocator_i allocator = manager->allocator;
    tm_free(&allocator, manager, sizeof(tm_component_manager_o));
    tm_entity_api->destroy_child_allocator(ctx, &allocator);
}
```

#### Custom UI

We also need to provide a custom UI for our reference to the asset! When we define our Truth type we tell the system that it should be a reference **only** of type `TM_TT_TYPE_HASH__TXT_ASSET`.

```c
    tm_the_truth_property_definition_t story_component_properties[] = {
        [TM_TT_PROP__STORY_COMPONENT__ASSET] = { "story_asset", .type = TM_THE_TRUTH_PROPERTY_TYPE_REFERENCE, .type_hash = TM_TT_TYPE_HASH__TXT_ASSET }
    };
```

This makes sure that in the Editor the user cannot store any other Truth type in this property. The Truth will check for it

We need to add the `TM_TT_ASPECT__PROPERTIES` aspect to our type to make sure it has a custom UI.

```c
    static tm_properties_aspect_i properties_component_aspect = {
        .custom_ui = properties__component_custom_ui,
    };

    const tm_tt_type_t story_component_type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__STORY_COMPONENT, story_component_properties, TM_ARRAY_COUNT(story_component_properties));
    tm_the_truth_api->set_aspect(tt, story_component_type, TM_TT_ASPECT__PROPERTIES, &properties_component_aspect);
```

And than we need to define our custom UI:

```c
static float properties__component_custom_ui(struct tm_properties_ui_args_t *args, tm_rect_t item_rect, tm_tt_id_t object, uint32_t indent)
{
    TM_INIT_TEMP_ALLOCATOR(ta);
    tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(args->tt, TM_TT_TYPE_HASH__ASSET);
    // get all instances of `TM_TT_TYPE_HASH__TXT_ASSET`
    tm_tt_id_t *ids = tm_the_truth_api->all_objects_of_type(args->tt, tm_the_truth_api->object_type_from_name_hash(args->tt, TM_TT_TYPE_HASH__TXT_ASSET), ta);
    tm_tt_id_t *items = 0;
    const char **names = 0;
    tm_carray_temp_push(names, "Select", ta);
    tm_carray_temp_push(items, (tm_tt_id_t){ 0 }, ta);
    for (uint32_t i = 0; i < tm_carray_size(ids); ++i) {
        // we make sure a Asset Type is the owner of the object! This is important since
        // the Asset Truth type has the name field! `TM_TT_PROP__ASSET__NAME`
        tm_tt_id_t owner = tm_the_truth_api->owner(args->tt, ids[i]);
        if (tm_tt_type(owner).u64 == asset_type.u64) {
            // if the owner is a asset we add it's name to our names array and use the id and add it to ower items!
            tm_carray_temp_push(names, tm_the_truth_api->get_string(args->tt, tm_tt_read(args->tt, owner), TM_TT_PROP__ASSET__NAME), ta);
            tm_carray_temp_push(items, ids[i], ta);
        }
    }
    // creates a popup picker and the user can choose what reference they want to put into the property!
    item_rect.y = tm_properties_view_api->ui_reference_popup_picker(args, item_rect, "Asset", NULL, object, TM_TT_PROP__STORY_COMPONENT__ASSET, names, items, (uint32_t)tm_carray_size(items));
    TM_SHUTDOWN_TEMP_ALLOCATOR(ta); // always make sure you call the shutdown function on the temp allocator
    return item_rect.y;
}
```

In there we get all objects of type `TM_TT_TYPE_HASH__TXT_ASSET` we know that this type can only exist as a sub object of the Asset Truth Type.

> The type can only be created a part of the asset at this point!

This information is important because we need a name for our asset and therefore we just iterate over all our TXT Assets and check if they are owned by a Truth Asset type. If yes we get the name from it and store it in a names array. At the end we add all the IDs of the objects in a array so the user can select them in the drop down menu of the `tm_properties_view_api.ui_reference_popup_picker()`.



## Drag and drop a Text Asset into the Scene and create an entity

Finally, we can do what we came here to do: Make our Asset drag and droppable! We make use of the `TM_TT_ASPECT__ASSET_SCENE`!

We define the aspect as described above:

```c
#include <plugins/the_machinery_shared/asset_aspects.h>
//.. other code
tm_asset_scene_api scene_api = {
    .droppable = droppable,
    .create_entity = create_entity,
};
```

In the Create Truth Type function you need to add the aspect `TM_TT_ASPECT__ASSET_SCENE`:

```c
static void create_truth_types(struct tm_the_truth_o *tt)
{
    static tm_the_truth_property_definition_t my_asset_properties[] = {
        { "import_path", TM_THE_TRUTH_PROPERTY_TYPE_STRING },
        { "data", TM_THE_TRUTH_PROPERTY_TYPE_BUFFER },
    };
    const tm_tt_type_t type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__MY_ASSET, my_asset_properties, TM_ARRAY_COUNT(my_asset_properties));
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__FILE_EXTENSION, "txt");
    static tm_properties_aspect_i properties_aspect = {
        .custom_ui = properties__custom_ui,
    };
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__PROPERTIES, &properties_aspect);
    tm_the_truth_api->set_aspect(tt, type, TM_TT_ASPECT__ASSET_SCENE, &scene_api); // <<---

    // .. more code
}
```

Than, we provide a `droppable()` function:

```c
bool droppable(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t asset)
{
    return true;
}
```



After this, the more important function comes:

```c
#include <plugins/entity/transform_component.h>
#include <plugins/the_machinery_shared/scene_common.h>
// ... more code
tm_tt_id_t create_entity(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt,
    tm_tt_id_t asset, const char *name, const tm_transform_t *local_transform,
    tm_tt_id_t parent_entity, struct tm_undo_stack_i *undo_stack)
{
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Create Entity From Creation Graph"));
    const tm_tt_type_t entity_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__ENTITY);
    const tm_tt_id_t entity = tm_the_truth_api->create_object_of_type(tt, entity_type, undo_scope);
    tm_the_truth_object_o *entity_w = tm_the_truth_api->write(tt, entity);
    tm_the_truth_api->set_string(tt, entity_w, TM_TT_PROP__ENTITY__NAME, name);
    // add story:
    {
        tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__STORY_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, asset_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->set_reference(tt, component_w, TM_TT_PROP__STORY_COMPONENT__ASSET, asset);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
    // add transform:
    {
        const tm_tt_type_t transform_component_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, transform_component_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }

    tm_the_truth_api->commit(tt, entity_w, undo_scope);

    tm_scene_common_api->place_entity(tt, entity, local_transform, parent_entity, undo_scope);

    undo_stack->add(undo_stack->inst, tt, undo_scope);

    return entity;
}
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
// other code
     tm_scene_common_api = reg->get(TM_SCENE_COMMON_API_NAME);
    tm_entity_api = reg->get(TM_ENTITY_API_NAME);
// ... other code
    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME, component__create);
}
```



First, we create an entity:

```c
tm_tt_id_t create_entity(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt,
    tm_tt_id_t asset, const char *name, const tm_transform_t *local_transform,
    tm_tt_id_t parent_entity, struct tm_undo_stack_i *undo_stack)
{
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Create Entity From Creation Graph"));
    const tm_tt_type_t entity_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__ENTITY);
    const tm_tt_id_t entity = tm_the_truth_api->create_object_of_type(tt, entity_type, undo_scope);
    tm_the_truth_object_o *entity_w = tm_the_truth_api->write(tt, entity);
    tm_the_truth_api->set_string(tt, entity_w, TM_TT_PROP__ENTITY__NAME, name);
//...
}
```

Suppose it needs a transform. If not, we don't! In this case, we add the transform to the entity, just to make a point:

```c
tm_tt_id_t create_entity(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt,
    tm_tt_id_t asset, const char *name, const tm_transform_t *local_transform,
    tm_tt_id_t parent_entity, struct tm_undo_stack_i *undo_stack)
{
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Create Entity From Creation Graph"));
    const tm_tt_type_t entity_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__ENTITY);
    const tm_tt_id_t entity = tm_the_truth_api->create_object_of_type(tt, entity_type, undo_scope);
    tm_the_truth_object_o *entity_w = tm_the_truth_api->write(tt, entity);
    tm_the_truth_api->set_string(tt, entity_w, TM_TT_PROP__ENTITY__NAME, name);
    // add transform:
    {
        const tm_tt_type_t transform_component_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, transform_component_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
    // ...
}
```

Then, we add the story component to the entity we follow the same steps as before.

```c
tm_tt_id_t create_entity(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt,
    tm_tt_id_t asset, const char *name, const tm_transform_t *local_transform,
    tm_tt_id_t parent_entity, struct tm_undo_stack_i *undo_stack)
{
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Create Entity From Creation Graph"));
    const tm_tt_type_t entity_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__ENTITY);
    const tm_tt_id_t entity = tm_the_truth_api->create_object_of_type(tt, entity_type, undo_scope);
    tm_the_truth_object_o *entity_w = tm_the_truth_api->write(tt, entity);
    tm_the_truth_api->set_string(tt, entity_w, TM_TT_PROP__ENTITY__NAME, name);
    // add transform:
    {
        const tm_tt_type_t transform_component_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, transform_component_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
// add story:
    {
        tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__STORY_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, asset_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->set_reference(tt, component_w, TM_TT_PROP__STORY_COMPONENT__ASSET, asset);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
}
```

After all this, we can commit our changes to the Truth. After this we could place it in the scene with the `tm_scene_common_api.place_entity()`. This step is not needed but is nice to do!

Do not forget to add the undo scope to make sure we can undo our action and return the created entity!

```c
tm_tt_id_t create_entity(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt,
    tm_tt_id_t asset, const char *name, const tm_transform_t *local_transform,
    tm_tt_id_t parent_entity, struct tm_undo_stack_i *undo_stack)
{
    const tm_tt_undo_scope_t undo_scope = tm_the_truth_api->create_undo_scope(tt, TM_LOCALIZE("Create Entity From Creation Graph"));
    const tm_tt_type_t entity_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__ENTITY);
    const tm_tt_id_t entity = tm_the_truth_api->create_object_of_type(tt, entity_type, undo_scope);
    tm_the_truth_object_o *entity_w = tm_the_truth_api->write(tt, entity);
    tm_the_truth_api->set_string(tt, entity_w, TM_TT_PROP__ENTITY__NAME, name);
    // add transform:
    {
        const tm_tt_type_t transform_component_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, transform_component_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
// add story:
    {
        tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__STORY_COMPONENT);
        const tm_tt_id_t component = tm_the_truth_api->create_object_of_type(tt, asset_type, undo_scope);
        tm_the_truth_object_o *component_w = tm_the_truth_api->write(tt, component);
        tm_the_truth_api->set_reference(tt, component_w, TM_TT_PROP__STORY_COMPONENT__ASSET, asset);
        tm_the_truth_api->add_to_subobject_set(tt, entity_w, TM_TT_PROP__ENTITY__COMPONENTS, &component_w, 1);
        tm_the_truth_api->commit(tt, component_w, undo_scope);
    }
tm_the_truth_api->commit(tt, entity_w, undo_scope);

    tm_scene_common_api->place_entity(tt, entity, local_transform, parent_entity, undo_scope);

    undo_stack->add(undo_stack->inst, tt, undo_scope);

    return entity;
    }
```

Now we have added the ability to add this to our asset!

> **Note:** This is all not done at run time, since we are dealing with the Truth here and not with the ECS our changes will apply first to the ECS when we simulate the game!



## Modify a already existing asset

It is important to understand that you can add this to any truth type even if you do not define them in your plugin. Lets assume you have created a new plugin which uses the txt file asset. You are not the owner of this plugin and its source code so you cannot modify it like we did above. What you can do on the other hand you can add the aspect to the truth type:

```c
// -- load plugin
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api *reg, bool load)
{
// other code
     tm_scene_common_api = reg->get(TM_SCENE_COMMON_API_NAME);
    tm_entity_api = reg->get(TM_ENTITY_API_NAME);
// ... other code
    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, create_truth_types);
}
```

and then in the `create_truth_types` function you can add the aspect to the truth type:

```c
// -- create truth type
static void create_truth_types(struct tm_the_truth_o *tt)
{
    tm_tt_type_t asset_type = tm_the_truth_api->object_type_from_name_hash(tt, TM_TT_TYPE_HASH__TXT_ASSET);
    if(asset_type.u64){
        if(tm_the_truth_api->get_aspect(tt, asset_type, TM_TT_ASPECT__ASSET_SCENE))
	    	tm_the_truth_api->set_aspect(tt, asset_type, TM_TT_ASPECT__ASSET_SCENE, &scene_api);
    }
}
```

In here we get the `asset_type` from the Truth. Important here is we need to make sure the type exists already! if not it makes no sense to add the aspect to it. More over we need to make sure that the asset has not already this aspect. Since a Object can have only one aspect at the same time!
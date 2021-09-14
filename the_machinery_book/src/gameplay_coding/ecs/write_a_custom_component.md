# Write a custom component

This walkthrough shows you how to add a custom component to the Engine. During this walkthrough, we will cover the following topics:

- How to create a component from scratch.
- Where and how do we register a component.

You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide]({{base_url}}extending_the_machinery/the_plugin_system.html) and the [Write a plugin guide]({{the_machinery_book}}extending_the_machinery/write-a-plugin.html#build-requirements). The goal of this walkthrough is to dissect the component plugin provided by the Engine.



**Table of Content**

* auto-gen TOC;
{:toc}


## Where do we start?

In this example, we want to create a new plugin, which contains our component. We open the Engine go to **file -> New Plugin -> Entity Component.** The file dialog will pop up and ask us where we want to save our file. Pick a location that suits you.

> **Tip:** Maybe store your plugin in a folder next to your game project.

After this, we see that the Engine created some files for us. Now we need to ensure that we can build our project. In the root folder (The folder with the `premake` file), we run `tmbuild,` and if there is no issue, we see that it will build our projects once and generate the `.sln` file (on windows). If there is an issue, we should ensure we have set up the Environment variables correctly and installed all the needed dependencies. For more information, please read this [guide]({{the_machinery_book}}helper_tools/tmbuild.html).

Now we can open the `.c` file with our favourite IDE. The file will contain the following content:

```c
static struct tm_entity_api* tm_entity_api;
static struct tm_transform_component_api* tm_transform_component_api;
static struct tm_temp_allocator_api* tm_temp_allocator_api;
static struct tm_the_truth_api* tm_the_truth_api;
static struct tm_localizer_api* tm_localizer_api;

#include <plugins/entity/entity.h>
#include <plugins/entity/transform_component.h>
#include <plugins/the_machinery_shared/component_interfaces/editor_ui_interface.h>

#include <foundation/api_registry.h>
#include <foundation/carray.inl>
#include <foundation/localizer.h>
#include <foundation/math.inl>
#include <foundation/the_truth.h>

#define TM_TT_TYPE__CUSTOM_COMPONENT "tm_custom_component"
#define TM_TT_TYPE_HASH__CUSTOM_COMPONENT TM_STATIC_HASH("tm_custom_component", 0x355309758b21930cULL)

enum {
    TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY, // float
    TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE, // float
};

struct tm_custom_component_t {
    float y0;
    float frequency;
    float amplitude;
};

static const char* component__category(void)
{
    return TM_LOCALIZE("Samples");
}

static tm_ci_editor_ui_i* editor_aspect = &(tm_ci_editor_ui_i){
    .category = component__category
};

static void truth__create_types(struct tm_the_truth_o* tt)
{
    tm_the_truth_property_definition_t custom_component_properties[] = {
        [TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY] = { "frequency", TM_THE_TRUTH_PROPERTY_TYPE_FLOAT },
        [TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE] = { "amplitude", TM_THE_TRUTH_PROPERTY_TYPE_FLOAT },
    };

    const tm_tt_type_t custom_component_type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__CUSTOM_COMPONENT, custom_component_properties, TM_ARRAY_COUNT(custom_component_properties));
    const tm_tt_id_t default_object = tm_the_truth_api->quick_create_object(tt, TM_TT_NO_UNDO_SCOPE, TM_TT_TYPE_HASH__CUSTOM_COMPONENT, TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY, 1.0f, TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE, 1.0f, -1);
    tm_the_truth_api->set_default_object(tt, custom_component_type, default_object);

    tm_the_truth_api->set_aspect(tt, custom_component_type, TM_CI_EDITOR_UI, editor_aspect);
}

static bool component__load_asset(tm_component_manager_o* man, tm_entity_t e, void* c_vp, const tm_the_truth_o* tt, tm_tt_id_t asset)
{
    struct tm_custom_component_t* c = c_vp;
    const tm_the_truth_object_o* asset_r = tm_tt_read(tt, asset);
    c->y0 = 0;
    c->frequency = tm_the_truth_api->get_float(tt, asset_r, TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY);
    c->amplitude = tm_the_truth_api->get_float(tt, asset_r, TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE);
    return true;
}

static void component__create(struct tm_entity_context_o* ctx)
{
    tm_component_i component = {
        .name = TM_TT_TYPE__CUSTOM_COMPONENT,
        .bytes = sizeof(struct tm_custom_component_t),
        .load_asset = component__load_asset,
    };

    tm_entity_api->register_component(ctx, &component);
}

// Runs on (custom_component, transform_component)
static void engine_update__custom_component(tm_engine_o* inst, tm_engine_update_set_t* data)
{
    TM_INIT_TEMP_ALLOCATOR(ta);

    tm_entity_t* mod_transform = 0;

    struct tm_entity_context_o* ctx = (struct tm_entity_context_o*)inst;

    double t = 0;
    for (const tm_entity_blackboard_value_t* bb = data->blackboard_start; bb != data->blackboard_end; ++bb) {
        if (TM_STRHASH_EQUAL(bb->id, TM_ENTITY_BB__TIME))
            t = bb->double_value;
    }

    for (tm_engine_update_array_t* a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
        struct tm_custom_component_t* custom_component = a->components[0];
        tm_transform_component_t* transform = a->components[1];

        for (uint32_t i = 0; i < a->n; ++i) {
            if (!custom_component[i].y0)
                custom_component[i].y0 = transform[i].world.pos.y;
            const float y = custom_component[i].y0 + custom_component[i].amplitude * sinf((float)t * custom_component[i].frequency);

            transform[i].world.pos.y = y;
            ++transform[i].version;
            tm_carray_temp_push(mod_transform, a->entities[i], ta);
        }
    }

    tm_entity_api->notify(ctx, data->engine->components[1], mod_transform, (uint32_t)tm_carray_size(mod_transform));

    TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
}

static bool engine_filter__custom_component(tm_engine_o* inst, const tm_component_type_t* components, uint32_t num_components, const tm_component_mask_t* mask)
{
    return tm_entity_mask_has_component(mask, components[0]) && tm_entity_mask_has_component(mask, components[1]);
}

static void component__register_engine(struct tm_entity_context_o* ctx)
{
    const tm_component_type_t custom_component = tm_entity_api->lookup_component_type(ctx, TM_TT_TYPE_HASH__CUSTOM_COMPONENT);
    const tm_component_type_t transform_component = tm_entity_api->lookup_component_type(ctx, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);

    const tm_engine_i custom_component_engine = {
        .ui_name = "Custom Component",
        .hash  = TM_STATIC_HASH("CUSTOM_COMPONENT", 0xe093a8316a6c2d29ULL),
        .num_components = 2,
        .components = { custom_component, transform_component },
        .writes = { false, true },
        .update = engine_update__custom_component,
        .filter = engine_filter__custom_component,
        .inst = (tm_engine_o*)ctx,
    };
    tm_entity_api->register_engine(ctx, &custom_component_engine);
}

TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api* reg, bool load)
{
    tm_entity_api = reg->get(TM_ENTITY_API_NAME);
    tm_transform_component_api = reg->get(TM_TRANSFORM_COMPONENT_API_NAME);
    tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
    tm_temp_allocator_api = reg->get(TM_TEMP_ALLOCATOR_API_NAME);
    tm_localizer_api = reg->get(TM_LOCALIZER_API_NAME);

    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, truth__create_types);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME, component__create);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME, component__register_engine);
}

```



## Code structure

Let us dissect the code structure and discuss all the points of interest.

### API and include region

The file begins with all includes and API definitions: 

```c
static struct tm_entity_api* tm_entity_api;
static struct tm_transform_component_api* tm_transform_component_api;
static struct tm_temp_allocator_api* tm_temp_allocator_api;
static struct tm_the_truth_api* tm_the_truth_api;
static struct tm_localizer_api* tm_localizer_api;

#include <plugins/entity/entity.h>
#include <plugins/entity/transform_component.h>
#include <plugins/the_machinery_shared/component_interfaces/editor_ui_interface.h>

#include <foundation/api_registry.h>
#include <foundation/carray.inl>
#include <foundation/localizer.h>
#include <foundation/math.inl>
#include <foundation/the_truth.h>
```

The code will fill the API definitions with life in the `tm_load_plugin` function.

### Define your Data

The next part contains the Truth Definition of the component and the plain old data struct (POD). *In production, we should separate those aspects into a header file!*

> Note: All components should be plain old datatypes.

```c
#define TM_TT_TYPE__CUSTOM_COMPONENT "tm_custom_component"
#define TM_TT_TYPE_HASH__CUSTOM_COMPONENT TM_STATIC_HASH("tm_custom_component", 0x355309758b21930cULL)

enum {
    TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY, // float
    TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE, // float
};

struct tm_custom_component_t {
    float y0;
    float frequency;
    float amplitude;
};
```



### Add your component to the Truth

After this, we have the region in which we define the category of our component. The Editor will call it to categorize the component into the correct section. 

We need to define a `tm_ci_editor_ui_i` object which uses this function.  Later we register this function to the `TM_CI_EDITOR_UI` aspect of our truth type. If you do not add this aspect later to your Truth Type, the Editor will not know that this Component Type exists, and you can not add it via the Editor, but in C.

> **Note:** More about aspects you can read in the [aspects guide](#).

```c 
static const char* component__category(void)
{
    return TM_LOCALIZE("Samples");
}

static tm_ci_editor_ui_i* editor_aspect = &(tm_ci_editor_ui_i){
    .category = component__category
};
```



In this region, we create our component truth type. It is important to remember that the Truth will not reflect the runtime data, just the data you can edit in the Editor. On the other hand, the Entity Context will store your runtime data, the plain old data struct you have defined above. More about how this works later in this section.



Let us take this code apart one more time:

```c
static void truth__create_types(struct tm_the_truth_o* tt)
{
    tm_the_truth_property_definition_t custom_component_properties[] = {
        [TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY] = { "frequency", TM_THE_TRUTH_PROPERTY_TYPE_FLOAT },
        [TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE] = { "amplitude", TM_THE_TRUTH_PROPERTY_TYPE_FLOAT },
    };

    const tm_tt_type_t custom_component_type = tm_the_truth_api->create_object_type(tt, TM_TT_TYPE__CUSTOM_COMPONENT, custom_component_properties, TM_ARRAY_COUNT(custom_component_properties));
    const tm_tt_id_t default_object = tm_the_truth_api->quick_create_object(tt, TM_TT_NO_UNDO_SCOPE, TM_TT_TYPE_HASH__CUSTOM_COMPONENT, TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY, 1.0f, TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE, 1.0f, -1);
    tm_the_truth_api->set_default_object(tt, custom_component_type, default_object);

    tm_the_truth_api->set_aspect(tt, custom_component_type, TM_CI_EDITOR_UI, editor_aspect);
}
```

1. We define the component's properties.
2. We create the actual type in the Truth.
3. We create an object of our type with `quick_create_object` and provide a default object to our component. It makes sure that when you add the component to an Entity, you have the expected default values. It is not needed, just a nice thing to have.
4. Add our `TM_CI_EDITOR_UI` aspect to the type. It tells the Editor that you can add the component via the Editor. If you do not provide it, the Editor will not suggest this component to you and cannot store it in the Truth. It does not mean you cannot add this component via C.



### Define your component

You an register a component to the `TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME` in your plugin load function. This interface expects a function pointer to a create component function of the signature: `void tm_entity_create_component_i(struct tm_entity_context_o *ctx)`.

The Engine will call this function whenever it creates a new Entity Context to populate the context with all the known components. It usually happens at the beginning of the Simulation.

Within this function, you can define your component and register it to the context. The `tm_entity_api` provides a function `tm_entity_api.register_component()` which expects the current context and a instance of the `tm_component_i`. We define one in our function and give it the needed information:

- A name should be the same as the Truth Type
- The size of the component struct
- A load asset function

```c
static void component__create(struct tm_entity_context_o* ctx)
{
    tm_component_i component = {
        .name = TM_TT_TYPE__CUSTOM_COMPONENT,
        .bytes = sizeof(struct tm_custom_component_t),
        .load_asset = component__load_asset,
    };

    tm_entity_api->register_component(ctx, &component);
}
```

As mentioned before, the Truth does not reflect the runtime data and only holds the data you can edit in the Editor. This is why there needs to be some translation between The Truth and the ECS. This magic is happening in the `tm_component_i.load_asset()`. This function allows you to translate a `tm_tt_id_t` asset to the plain old data of the component.

```c
static bool component__load_asset(tm_component_manager_o* man, tm_entity_t e, void* c_vp, const tm_the_truth_o* tt, tm_tt_id_t asset)
{
    struct tm_custom_component_t* c = c_vp;
    const tm_the_truth_object_o* asset_r = tm_tt_read(tt, asset);
    c->y0 = 0;
    c->frequency = tm_the_truth_api->get_float(tt, asset_r, TM_TT_PROP__CUSTOM_COMPONENT__FREQUENCY);
    c->amplitude = tm_the_truth_api->get_float(tt, asset_r, TM_TT_PROP__CUSTOM_COMPONENT__AMPLITUDE);
    return true;
}
```

The first step is that we cast the given `void*` of the component data `c_vp` to the correct data type. After that, we load the data from the Truth and store it in the component. In the end, we return true because no error occurred.



### Define your engine update

*In the Machinery, gameplay code is mainly driven by Systems and Engines. They define the behaviour while the components the data describes.* 

> **Note:** in some entity systems, these are referred to as *systems* instead, but we choose *Engine* because it is less ambiguous.



This next section of the code is about defining an Engine.

```c
// Runs on (custom_component, transform_component)
static void engine_update__custom_component(tm_engine_o* inst, tm_engine_update_set_t* data)
{
    TM_INIT_TEMP_ALLOCATOR(ta);

    tm_entity_t* mod_transform = 0;

    struct tm_entity_context_o* ctx = (struct tm_entity_context_o*)inst;

    double t = 0;
    for (const tm_entity_blackboard_value_t* bb = data->blackboard_start; bb != data->blackboard_end; ++bb) {
        if (TM_STRHASH_EQUAL(bb->id, TM_ENTITY_BB__TIME))
            t = bb->double_value;
    }

    for (tm_engine_update_array_t* a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
        struct tm_custom_component_t* custom_component = a->components[0];
        tm_transform_component_t* transform = a->components[1];

        for (uint32_t i = 0; i < a->n; ++i) {
            if (!custom_component[i].y0)
                custom_component[i].y0 = transform[i].world.pos.y;
            const float y = custom_component[i].y0 + custom_component[i].amplitude * sinf((float)t * custom_component[i].frequency);

            transform[i].world.pos.y = y;
            ++transform[i].version;
            tm_carray_temp_push(mod_transform, a->entities[i], ta);
        }
    }

    tm_entity_api->notify(ctx, data->engine->components[1], mod_transform, (uint32_t)tm_carray_size(mod_transform));

    TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
}
```



The first thing we do is use a temp allocator for any future allocation that will not leave this function. After that, we cast the `tm_engine_o* inst` to the `tm_entity_context_o*` so we have access to the entity context later on.

The next step is to get the time from the Blackboard Values. 

```c

double t = 0;
for (const tm_entity_blackboard_value_t* bb = data->blackboard_start; bb != data->blackboard_end; ++bb) {
        if (TM_STRHASH_EQUAL(bb->id, TM_ENTITY_BB__TIME))
            t = bb->double_value;
    }
```



The Engine provides a bunch of useful Blackboard values. They are defined in the `plugins/entity/entity.h`.



- `TM_ENTITY_BB__SIMULATION_SPEED` - Speed that the simulation is running at. Defaults to 1.0 for normal speed.
- `TM_ENTITY_BB__DELTA_TIME` - Blackboard item representing the simulation delta time of the current frame.
- `TM_ENTITY_BB__TIME` - Blackboard item representing the total elapsed time in the Simulation.
- `TM_ENTITY_BB__WALL_DELTA_TIME` - Blackboard item representing the wall delta time of the current frame. (Wall delta time is not affected by the Simulation being paused or run in slow motion.)
- `TM_ENTITY_BB__WALL_TIME` - Blackboard item representing the total elapsed wall time in the Simulation.
- `TM_ENTITY_BB__CAMERA` - Blackboard items for the current camera.
- `TM_ENTITY_BB__EDITOR` - Blackboard item that indicates that we are running in *Editor* mode. This may disable some components and/or simulation engines.
- `TM_ENTITY_BB__SIMULATING_IN_EDITOR` - Set to non-zero if the Simulation runs from within the Editor, such as running a game in the simulation tab. It will be zero when we run a game from the Runner. Note the distinction from [TM_ENTITY_BB__EDITOR](https://ourmachinery.com//apidoc/plugins/entity/entity.h.html#tm_entity_bb__editor).



The `tm_engine_update_set_t` gives us access to the needed data, and we can modify our component. The first important information we get are the number of entity types (also known Archetypes). This number is stored in `data->num_arrays`. Now that we know this information we can iterate over them and access the components per entity type. `tm_engine_update_array_t a =  data->arrays` (Gives us the current entity type's components). `a->n` is the number of matching components / entities of this entity type.

```c

    for (tm_engine_update_array_t* a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
        struct tm_custom_component_t* custom_component = a->components[0];
        tm_transform_component_t* transform = a->components[1];

        for (uint32_t i = 0; i < a->n; ++i) {
            if (!custom_component[i].y0)
                custom_component[i].y0 = transform[i].world.pos.y;
            const float y = custom_component[i].y0 + custom_component[i].amplitude * sinf((float)t * custom_component[i].frequency);

            transform[i].world.pos.y = y;
            ++transform[i].version;
            tm_carray_temp_push(mod_transform, a->entities[i], ta);
        }
    }
```

> **Note**: In case you are not that familiar with C this loop:
>
> ```c
>  for (tm_engine_update_array_t* a = data->arrays; a < data->arrays + data->num_arrays; ++a) {
> ```
>
> is kind of the C equivalent to C++'s for each loop: `for(auto a : data->arrays)`

As the last step, we add a notifier function call to notify all entities that their components have changed.

```c
    tm_entity_api->notify(ctx, data->engine->components[1], mod_transform, (uint32_t)tm_carray_size(mod_transform));
```



### Register your Engine to the system

You an register a component to the `TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME` in your plugin load function. This interface expects a function pointer to a create component function of the signature: `void tm_entity_register_engines_i(struct tm_entity_context_o *ctx)`. 



The function itself looks as follows:

```c
static void component__register_engine(struct tm_entity_context_o* ctx)
{
    const tm_component_type_t custom_component = tm_entity_api->lookup_component_type(ctx, TM_TT_TYPE_HASH__CUSTOM_COMPONENT);
    const tm_component_type_t transform_component = tm_entity_api->lookup_component_type(ctx, TM_TT_TYPE_HASH__TRANSFORM_COMPONENT);

    const tm_engine_i custom_component_engine = {
        .ui_name = "Custom Component",
        .hash  = TM_STATIC_HASH("CUSTOM_COMPONENT", 0xe093a8316a6c2d29ULL),
        .num_components = 2,
        .components = { custom_component, transform_component },
        .writes = { false, true },
        .update = engine_update__custom_component,
        .filter = engine_filter__custom_component,
        .inst = (tm_engine_o*)ctx,
    };
    tm_entity_api->register_engine(ctx, &custom_component_engine);
}
```

The first thing we do is looking up the component type. Did we register the type? If not, we will not get the correct type. Here we are using the name we defined beforehand in our component create function.

Then we ask for the transform component next because our Engine shall run on those two components.

After this, we define the actual instance of our engine struct

`tm_engine_i`. 

We provide a `.ui_name` used in the Profiler to identify our Engine. Moreover, we add a unique string hash identifying this engine/system. This is used for scheduling the engine/system concerning other engines and systems, using the`before_me` and `after_me` fields.

Then we tell the system how many components the Engine shall operate on and which ones we will modify. This is used for scheduling the engines later one.

At last, we provide the needed update function, which we have discussed earlier, and a filter function.

```c
static bool engine_filter__custom_component(tm_engine_o* inst, const tm_component_type_t* components, uint32_t num_components, const tm_component_mask_t* mask)
{
    return tm_entity_mask_has_component(mask, components[0]) && tm_entity_mask_has_component(mask, components[1]);
}
```



The filter function will be called on all entity types to determine if the Engine shall run on them or not.  To provide this function is optional. If present it specifies a filter function called for each entity type (as

represented by its component mask) to determine if the Engine should run on that entity type. If no `tm_engine_i.filter()` function is supplied and no `excludes[]` flags are set, the update will run on entity types that have all the components in the `components` array. If some `excludes[]` flags are set, the Engine will run on all entity types that **do not** have any of the components whose `excludes[]` flags are set, but have all the other components in the `components` array. 

> **Note:** For more information, check the [documentation](https://ourmachinery.com//apidoc/plugins/entity/entity.h.html#structtm_engine_i.filter()).

The last thing the register function needs to do is register the Engine to the Entity Context.

```c
 tm_entity_api->register_engine(ctx, &custom_component_engine);
```

### The plugin load function

The most important lines here are the once in which we register our truth types, the component and the engine.

```c
TM_DLL_EXPORT void tm_load_plugin(struct tm_api_registry_api* reg, bool load)
{
    tm_entity_api = reg->get(TM_ENTITY_API_NAME);
    tm_transform_component_api = reg->get(TM_TRANSFORM_COMPONENT_API_NAME);
    tm_the_truth_api = reg->get(TM_THE_TRUTH_API_NAME);
    tm_temp_allocator_api = reg->get(TM_TEMP_ALLOCATOR_API_NAME);
    tm_localizer_api = reg->get(TM_LOCALIZER_API_NAME);

    tm_add_or_remove_implementation(reg, load, TM_THE_TRUTH_CREATE_TYPES_INTERFACE_NAME, truth__create_types);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_CREATE_COMPONENT_INTERFACE_NAME, component__create);
    tm_add_or_remove_implementation(reg, load, TM_ENTITY_SIMULATION_REGISTER_ENGINES_INTERFACE_NAME, component__register_engine);
}

```

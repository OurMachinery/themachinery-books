# Adding Drag and Drop to Assets

This walkthrough shows you how to enable a asset to be drag and dropped. You should have basic knowledge about how to write a custom plugin. If not, you might want to check this [Guide](https://ourmachinery.github.io/themachinery-books/the_machinery_book/extending_the_machinery/the_plugin_system.html). The goal of this walkthrough is to enable you to drag and drop your asset into the Scene!

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
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_truth_types)}}
```

We need to make use of the `tm_asset_scene_api` aspect. This aspect allows the associated Truth Type to be dragged and dropped to the Scene if wanted! We can find it in the `plugins/the_machinery_shared/asset_aspects.h` header.

### Asset Scene Aspect

This aspect expects an instance of the `tm_asset_scene_api`. When we provide a call-back called

`bool (*droppable)(struct tm_asset_scene_o *inst, struct tm_the_truth_o *tt, tm_tt_id_t asset);` we tell the scene that we can drag the asset out of the asset browser. We need to return true for this. In this case you need to provide the `create_entity` function. When you drag your asset into the Scene, this function is called by the Engine. In this function, you can create a new entity and attach it to the parent entity ( which might be the world.  If you drag it on top of another entity, you can attach the newly created entity as a child entity to this one. 

Before we can make use of this we need some component to be created for our Text Asset! Lets call it Story Component.

## The story component

Let us create a use case for our text file. Let us assume we wanted to make a very simple story-based game, and all our text files are the basis for our stories. This means we need to create first a story component.

> **Note**: For more details on how to create a component, follow this [guide]({{the_machinery_book}}/gameplay_coding/ecs/write_a_custom_component.html).

Here we have the whole source code for the story component:

```c
// more apis
static struct tm_entity_api *tm_entity_api;
// more includes
#include <plugins/entity/entity.h>
#include <plugins/the_machinery_shared/component_interfaces/editor_ui_interface.h>
// more code

{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,comp_meta)}}

{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_truth_types,off)}}

{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,component_def)}}

{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,plugin_load)}}

```



First, we create our component, and we need a way to guarantee that our truth data exists during runtime as well. Therefore, we use the Entity Manager to allocate our Story data and store just a pointer and its size to the allocated data in the Manager.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,component_manager)}}
```



The most important function here is the `component__load_asset` function, in which we translate the Truth Representation into an ECS representation. We load the text buffer, allocate it with the Manager, and store a pointer in our component. With this, we could create a reference-counted system in which multiple components point to the same story data, and only when the last component goes we deallocate this. Another alternative would be to avoid loading when we create the component, and the story is already allocated.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,component__load_asset)}}
```



When the Entity context gets destroyed, we need to clean up and destroy our Manager. Important that we call `call_remove_on_all_entities` to make sure all instances of the component are gone.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,component__remove_destroy)}}
```

#### Custom UI

**This part is optional!**, see next part where we use the `TM_TT_PROP_ASPECT__PROPERTIES__ASSET_PICKER`.

We also can to provide a custom UI for our reference to the asset! When we define our Truth type we tell the system that it should be a reference **only** of type `TM_TT_TYPE_HASH__TXT_ASSET`.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,none_asset_picker)}}
```

This makes sure that in the Editor the user cannot store any other Truth type in this property. The Truth will check for it

We need to add the `TM_TT_ASPECT__PROPERTIES` aspect to our type to make sure it has a custom UI.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,story_component)}}
```

And than we need to define our custom UI:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,component_custom_ui)}}
```

In there we get all objects of type `TM_TT_TYPE_HASH__TXT_ASSET` we know that this type can only exist as a sub object of the Asset Truth Type.

> The type can only be created a part of the asset at this point!

This information is important because we need a name for our asset and therefore we just iterate over all our TXT Assets and check if they are owned by a Truth Asset type. If yes we get the name from it and store it in a names array. At the end we add all the IDs of the objects in a array so the user can select them in the drop down menu of the `tm_properties_view_api.ui_reference_popup_picker()`.

## Using the Asset Picker Property Aspect

Instead of implementing our own UI, which can be full of boilerplate code we can also use the following aspect on our truth type: `TM_TT_PROP_ASPECT__PROPERTIES__ASSET_PICKER` or if we want to store a entity an provide a entity from the scene: `TM_TT_PROP_ASPECT__PROPERTIES__USE_LOCAL_ENTITY_PICKER`. The following code can be adjusted. In your `create_truth_types()` we need to add this aspect to our type property like this:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,story_component)}}
tm_tt_set_property_aspect(tt, story_component_type, TM_TT_PROP__STORY_COMPONENT__ASSET, tm_tt_prop_aspect__properties__asset_picker, TM_TT_TYPE__MY_ASSET);
}
```



## Drag and drop a Text Asset into the Scene and create an entity

Finally, we can do what we came here to do: Make our Asset drag and droppable! We make use of the `TM_TT_ASPECT__ASSET_SCENE`!

We define the aspect as described above:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,scene_api_def)}}
```

In the Create Truth Type function you need to add the aspect `TM_TT_ASPECT__ASSET_SCENE`:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_truth_types,off)}}
//..
}
```

Than, we provide a `droppable()` function:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,droppable)}}
```



After this, the more important function comes:

```c
#include <plugins/entity/transform_component.h>
#include <plugins/the_machinery_shared/scene_common.h>
// ... more code
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_entity_fn)}}
```



First, we create an entity:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_entity)}}
//...
}
```

Suppose it needs a transform. If not, we don't! In this case, we add the transform to the entity, just to make a point:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_entity_transform)}}
    // ...
}
```

Then, we add the story component to the entity we follow the same steps as before.

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_entity_story)}}
}
```

After all this, we can commit our changes to the Truth. After this we could place it in the scene with the `tm_scene_common_api.place_entity()`. This step is not needed but is nice to do!

Do not forget to add the undo scope to make sure we can undo our action and return the created entity!

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_entity_fn)}}
```

Now we have added the ability to add this to our asset!

> **Note:** This is all not done at run time, since we are dealing with the Truth here and not with the ECS our changes will apply first to the ECS when we simulate the game!



## Modify a already existing asset

It is important to understand that you can add this to any truth type even if you do not define them in your plugin. Lets assume you have created a new plugin which uses the txt file asset. You are not the owner of this plugin and its source code so you cannot modify it like we did above. What you can do on the other hand you can add the aspect to the truth type:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,plugin_load)}}
```

and then in the `create_truth_types` function you can add the aspect to the truth type:

```c
{{insert_code(env.TM_BOOK_CODE_SNIPPETS/custom_assets/drag_drop/txt.c,create_truth_types_modify)}}
```

In here we get the `asset_type` from the Truth. Important here is we need to make sure the type exists already! if not it makes no sense to add the aspect to it. More over we need to make sure that the asset has not already this aspect. Since a Object can have only one aspect at the same time!
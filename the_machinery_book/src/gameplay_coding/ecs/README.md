# Entity Component System

The purpose of the entity system is to provide a flexible model for *objects in a simulation*, that
allows us to compose complex objects from simpler components in a flexible and performant way.

An *entity* is a game object composed of *components*. Entities live in a *entity context* — an
isolated world of entities. 

Components are there to hold the needed data while *Engines*/*Systems* are there to provide behaviour.

Each context (*entity context*) can have a number of *engines* or *systems* registered. *(ECS)* Engines updates
are running on subset of entities that posses some set of components. 

> **Note**: in some entity systems, these are referred to as *systems* instead, but we choose *engine*, because it is less ambiguous.

While Systems are just a update with a provided access to the entity context. When we refer to a context in this chapter we mean the entity context.

**Table of Content**

* auto-gen TOC;
{:toc}
## What is an Entity?

An entity is the fundamental part of the Entity Component System. An entity is a handle to your data. Itself does not store any data or behavior.  The data is stored in components, which are associated with the Entity. The behavior is defined in Systems and Engines which process those components. Therefore a entity acts as an identifier or key to the data stored in components.

![](https://www.dropbox.com/s/5956267ltb4l14x/tm_guide_entity.png?dl=1)

> **Note:** In this example both entities have the same set of components, but they do not own the data they just refer to it!

Entities are managed by the Entity API and exist within an Entity Context. An Entity struct refers to an entity, but is not a real reference. Rather the Entity struct contains an index used to access entity data.

## What is an Entity Context?

The Entity Context is the simulation world. It contains all the Entites and Systems/Engines as well owns all the Component Data. There can be multiple Entity Contexts in the Editor. For example the Simulate tag, Preview Tab have both a Entity Context. When you Register A System/Engine you an decide in which context they shall run. The Default is in all contexts. 



## Where do Entities live?

- Entities **do not live in The Truth**. The truth is for *assets*, not for *simulation.*
- Entity data is owned by the entity context and thrown away when the entity context is destroyed.
- Entities can be spawned from *entity assets* in The Truth. Multiple entities can be spawned from
  the same asset.
- Changes to entity assets can be propagated into a context where those assets are spawned. This is
  the main way in which we will provide a “preview” of assets in a simulation context.
- An entity always belongs to a specific entity context and entity IDs are only unique within the entity contexts. Entity IDs act as weak references. If you have an ID you can ask the context whether that entity is still alive or not. `tm_entity_api.is_alive()`



## How is the data stored?

- An entity is a 64-bit value divided into a 32-bit index and a 32-bit generation.
- The index points to a slot where entity data is stored.
- The generation is increased every time we recycle a slot. This allows us to detect stale entity
  IDs (i.e., weak referencing through `is_alive()`.



## What is an Entity types / Archetype?

An Entity Types is a unique combination of component types. The Entity API uses the entity type to group all entities that have the same sets of components.

![](https://www.dropbox.com/s/453d1nqrwnsntbw/tm_guide_entity_entity_type.png?dl=1)

> **Note:** In this example Entities A-B are of the same entity type while C has a different entity type!

- An entity type is shared by all entities with a certain component mask.
- When components are added to or removed from an entity, it’s entity type changes, thus its data
  must be copied over to the new type.
- Pointers to component data are thus not permanent.



{{#include what_are_components.md}}



## What is a Component Manager?

- Can store persitsent data from the beginning of the Entity Context till the end

- Can provide a way to allocate data on adding/removing a component

  

![](https://www.dropbox.com/s/kre84a4vqouq37z/tm_guide_component_manager.png?dl=1)

## Game Logic

The behavior is defined in Systems and Engines which process those components. Systems and Engines can be seen as data transfromation actions. They take some input (components) and process them to some output (changed component data, different rendering) and a chain of small system together makes up your game!

 ![](https://www.dropbox.com/s/5wqvcf27vvx5b7v/engines.png?dl=1)

### What are Engines?

> **Note**: in some entity systems, these are referred to as *systems* instead, but we choose *engine*, because it is less ambiguous.

- An engine is an update that runs for all components matching a certain *component mask*.

- Engines registered with the context runs automatically on update, in parallel.

- Parallelization is done automatic, by looking at the components that each engine reads or writes.
  Before running, an engine waits for the previous engines that wrote to the components that the
  engine is interested in.
  
  The following image shows how a time based movement System could look like:
  
  ![](https://www.dropbox.com/s/vn3n7ai2y28u695/tm_guide_ecs_engine_flow.png?dl=1)
  
  

### What are Systems?

- General Update loop that has access to the Entity Context.
- Can be used for none component specific interactions
- Can be used for serial interactions that do not interact with the entity system. (Such as Input)



## How are Entity Assets translated to ECS Entities?

Since the Truth is a editor concept and our main data model, your scene is stored in the Truth. When you start the simulation your Assets get translated to the ECS via the `asset_load()` function! In your `tm_component_i` you can provide this function if you want your component to translate to the ECS world. In there you have access to the Truth, afterwards not anymore! Besides you can provide some other callbacks for differnt stages of the translation process. 

![](https://www.dropbox.com/s/ao6cs4fpyx9i078/truth_ecs%20%282%29.png?dl=1)

>  **Important:** A Component representation in The Truth may **not** reflect the runtime ECS representation. This can be used to separate a Truth representation into smaller bits for gameplay programming sake but keep the simplicty for the Front End user.

*Example:*

You have a `Movement Controller Component` that can be used via the UI to determine the Entities movement speed. The actual movement system interacts with a `Movement Component` which keeps track of the actual current speed and can be influenced by other systems while the Movement Controller is only there to keep the fixed `const` state and can only be influenced by a Skill Update system or something like this.



## Child entities

- Child entities are entities that are spawned and destroyed together with their parent.

  > **Note**: that we only store child pointers, not parent pointers. Deleting a child entity does not
  > automatically delete it from its parent — it will remain in the parent as a dead pointer.


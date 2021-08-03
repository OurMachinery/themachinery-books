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
## Entity Context

The Entity Context is the simulation world. It contains all the Entites and Systems/Engines as well owns all the Component Data. There can be multiple Entity Contexts in the Editor. For example the Simulate tag, Preview Tab have both a Entity Context. When you Register A System/Engine you an decide in which context they shall run. The Default is in all contexts. 



## Entities and The Truth

- Entities **do not live in The Truth**. The truth is for *assets*, not for *simulation.*
- Entity data is owned by the context and thrown away when the context is destroyed.
- Entities can be spawned from *entity assets* in The Truth. Multiple entities can be spawned from
  the same asset.
- Changes to entity assets can be propagated into a context where those assets are spawned. This is
  the main way in which we will provide a “preview” of assets in a simulation context.
- An entity always belongs to a specific context and entity IDs are only unique within the contexts. Entity IDs act as weak references. If you have an ID you can ask the context whether that entity is still alive or not. `tm_entity_api.is_alive()`



## Entity data storage

- An entity is a 64-bit value divided into a 32-bit index and a 32-bit generation.
- The index points to a slot where entity data is stored.
- The generation is increased every time we recycle a slot. This allows us to detect stale entitiy
  IDs (i.e., weak referencing through `is_alive()`.



## Entity types / Archetype

- An entity type is shared by all entities with a certain component mask.
- When components are added to or removed from an entity, it’s entity type changes, thus its data
  must be copied over to the new type.
- Pointers to component data are thus not permanent.



## Components

- A component is defined by `tm_component_i` — it consists of a fixed-size piece of POD data.
- This data is stored in a huge buffer for each entity type, and indexed by the index.
- In addition, a component can have a *manager*. The manager is notified when the component is added
  or removed.
- The manager can store additional data for the component that doesn’t fit in the POD data — such as
  lists, strings, buffers, etc.



> **Note**:  Keep in mind they do not need a Truth Representation. If They do not have one the Engine cannot display them in the Entity Tree View. This is useful for runtime only components.

 

## Component Manager 

- Can store persitsent data from the beginning of the Entity Context till the end
- Can provide a way to allocate data on adding/removing a component
- The manager is notified when the component is added or removed.




## Engines

> Note: in some entity systems, these are referred to as *systems* instead, but we choose *engine*, because it is less ambiguous.

- An engine is an update that runs for all components matching a certain *component mask*.

- Engines registered with the context runs automatically on update, in parallel.

- Parallelization is done automatic, by looking at the components that each engine reads or writes.
  Before running, an engine waits for the previous engines that wrote to the components that the
  engine is interested in.
  
  

## Systems

- General Update loop that has access to the Entity Context.
- Can be used for none component specific interactions
- Can be used for serial interactions that do not interact with the entity system. (Such as Input)



## Assets

- An entity asset has a list of components and child entities.

- Parsing of component data is done by a `load_asset()` function that is registered together with
  the component.
  
- Component assets may reference other entity assets within the same entity tree.

**Important:** A Component representation in The Truth may **not** reflect the runtime ECS representation. This can be used to separate a Truth representation into smaller bits for gameplay programming sake but keep the simplicty for the Front End user.

*Example:*

You have a `Movement Controller Component` that can be used via the UI to determine the Entities movement speed. The actual movement system interacts with a `Movement Component` which keeps track of the actual current speed and can be influenced by other systems while the Movement Controller is only there to keep the fixed `const` state and can only be influenced by a Skill Update system or something like this.



## Child entities

- Child entities are entities that are spawned and destroyed together with their parent.

  > **Note**: that we only store child pointers, not parent pointers. Deleting a child entity does not
  > automatically delete it from its parent — it will remain in the parent as a dead pointer.


# Gameplay Entry Point Comparison

In the Machinery you have multiple entry points for your game play code to live in. You can make use of *Simulation Entries*, *Entity Component System: Systems or Engines* and also make use of a *Entity Graph* or custom scripting language component. The question is more when to use which of the tools? The answer to this depends on your games needs. To summarize it in the Engine you have about four build in entry points for your game play code which you can use all at the same time and which one to use depends on your use case.

The following table will give a brief overview of the different types and their properties:

| Type                           | Parallel Execution | Lifetime based on entity | Random Memory Access by default | Runs only on a Subset of Entities | Runs per entity | Execution order can be  set |
| ------------------------------ | ------------------ | ------------------------ | ------------------------------- | --------------------------------- | --------------- | --------------------------- |
| Simulation Entry               | No                 | Yes                      | Yes                             | No                                | No              | Yes*                        |
| ECS System                     | Maybe              | No                       | Yes                             | No                                | No              | Yes*                        |
| ECS Engine                     | Maybe              | No                       | No                              | Yes                               | No              | Yes*                        |
| Entity Graph (Graph Component) | No                 | Yes                      | Yes                             | No                                | Yes             | No                          |

** via `.phase` or `.before_me` and `.after_me` when defining the interface*



## Recommendation

>  **Note:** These recommendations are no guidelines! You do not **have to follow them** they are just here to give another more example driven overview of the different types of gameplay entry points.

### System vs Engine

**Systems**

It is recommended to use a **System over an Engine** when you try to write a complex gameplay system that will handle **a few** **different entity types** simultaneously. The number of entities here is important. Since a System uses random memory access through get_component() which may lead to cache misses.

Moreover, a System is a preferred way of updating when the data in the component is just a pointer into some external system. (This is the case, for example, for PhysX components). In the case of PhysX, it is assumed to store its data in a cache-friendly order, which means we do *not* want to iterate over the entities in the order they are stored in the entity system since this would cause a pointer chasing in the external System. Instead, we just want to send a single update to the external System. It will process the entities in its own (cache-friendly) order.



Another reason to use **System over an Engine** is that you can use it to execute things on initialization and on the game's shutdown since only **Systems** have a `init()` and a `shutdown()` function, Engines do not.



**Engines**

It is recommended to use an **Engine over a System** when you try to write a complex gameplay system that will handle **a lot of entities with the same set of components** simultaneously. The ECS scheduler will gather all entities with the set of components and enable you to iterate over them in a cache-friendly manner. This allows you to write an engine that can manipulate a lot of entities simultaneously without any loss of performance.



### Simulation Entry vs System

It is recommended to use a **Simulation Entry** when you want to tie the lifetime of the underlying System to an Entity lifetime. This is a very similar concept to the "GameObject" Script concept in Unity. Suppose the entity that hosts the Simulation Entry Component is destroyed. In that case, the Update function will not be ticked anymore, and the System is destroyed. This can be a useful concept for level-specific Gameplay moments. A Simulation Entry also has a `start()` and `stop()` function. They are executed when the Simulation Entry is added or removed.



It is **not** recommended to use a Simulation Entry to handle a large mass of entities. For the same reason as the System is not used for this kind of purpose. The Simulation Entry will **not run parallel** and have random memory access.



### Entity Graph

It is recommended to use a **Entity Graph** when you want to tie the lifetime to a Entity and if you want to execute none performant code since the Entity Graph is a Visual Scripting language that is interpreted. It will be naturally slow. The Entity Graph is also good to handle UI/UX elements or for quick prototyping when performance is not important. Keep in mind that a Entity Graph is not executed in parallel and also only access memory via random access.


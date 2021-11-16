# How to design a Systems & Engines

In the Machinery, you provide the behavior for your gameplay code via Engines and Systems. The difference between Engines and Systems is that Engines provide an explicitly defined subset of components while Systems give you only access to the Entity Context.

> **Note:** Unsure what a System or an Engine is? Please read  [here]({{the_machinery_book}}/gameplay_coding/ecs/index.html)

This separation means that Engines are better used for high-frequency operations on many entities. At the same time, Systems are better used for broader operations such as input on a few Entities / Single entities.



> **Documentation:** The difference between *engines* and *systems* is that engines are fed component data, whereas systems are not. Thus, systems are useful when the data is stored externally from the components (for example to update a physics simulation), whereas *engines* are more efficient when the data  is stored in the components. (You could use a *system* to update data in components, but it would be inefficient, because you would have to perform a lot of lookups to access the component data.)



These are a couple of questions you should ask yourself in advance.

- On what data do we operate?
- What is our domain?
- What is the possible input for our transformation?
- What is the usage frequency of the data?
- What are we actually transforming?
- What could our algorithm look like?
- How often do we perform our transformation?

> More details about those questions click here : [How entities can interact.]({{base_url}}/gameplay_coding/ecs/how_entites_can_interact.html)

At the end of this, you should be able to answer the following questions:

- What kind of data am I going to read?
- What kind of data am I going to write?
- Should my operation be exclusive? Hence not to be executed in parallel?
- In which phase does it run? 
- What dependencies do I have?

Those answers are important for the automatic scheduling of the Systems/Engines. Based on all those inputs, the Entity System can determine when and how to schedule what.

## Best Practice

- **System/Engine Scope:** Systems should be designed to have one job only. This can be difficult at times, especially when designing new features. Therefore it is fine to first create a bigger system and then with time make them smaller. If you find that your engine/system does a lot of things, don't worry. In an ECS things are decoupled from everything else, therefore it is generally pretty easy to split them up into smaller units. This allows you to increase reusability of systems
- **System/Engine Scheduling:** Always provide a write list and a list of components your Engine/System is operating on. This is important so the scheduler can do its best! Also do not forget to make use of `.before_me`, `.after_me` and `.phase` more about this in the next chapter!

## Example 

```c
{{$include {TM_BOOK_CODE_SNIPPETS}/gameplay_code/ecs_system_engine.c:22:30}}
```

This movement engine will operate on:

- `keyboard_component`
- `movement_component`
- `transform_component`
- `mover_component`

components. The scheduler can now look for those components in other engines and determine based on the .`write` field how to schedule it efficiently.

In this example the scheduler can schedule any engine that writes to the keyboard and the movement component that the same time as this engine if they do not write to the transform and mover component!

## What is next?

More details on writing your own system or engine is explained in the next chapter




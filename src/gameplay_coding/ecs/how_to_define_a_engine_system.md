

# Defining a System and Engines

You have to pass the  `tm_entity_system_i` or `tm_engine_i` instance in your register function.

**Table of Content**

* {:toc}
## Ask yourself those questions before you design an Engine / System

The following questions are better explained in the chapter: [How entities can interact.]({{base_url}}/gameplay_coding/ecs/how_entites_can_interact.html)

- On what data do we operate?
- What is our domain?
- What is the possible input for our transformation?
- What is the usage frequency of the data?
- What are we actually transforming?
- What could our algorithm look like?
- How often do we perform our transformation?

and my answers

- What kind of data am I going to read?
- What kind of data am I going to write?
- What kind of data do I want to ignore? (**only important for engines**)
- Should my operation be exclusive? Hence not to be executed in parallel?
- In which phase does it run? 
- What dependencies do I have?

Now it is time to define the dependencies / important items for scheduling.



### How do those questions translate?



**What kind of data am I going to read?  && What kind of data am I going to write?**

They translate `.write` and `.components.` With those fields, we tell the scheduler what components this system operates. From which components it intends to read from and to which one it writes.

**What kind of data do I want to ignore?** (only important for engines)

In the `tm_engine_i` you can provide a way to filter your component. Thus you can decide on which components the engine shall run.  The field `.excluded` is used for this in there you can define which components an entity type shall **not** have. This means that when the engine is scheduled all entities will be ignored with those components. 

For more information see [Tagging Entities]({{base_url}}/gameplay_coding/ecs/tagging_entities.html) and [Filtering Entities]({{base_url}}/gameplay_coding/ecs/filtering_entities.html)

**Should my operation be exclusive? Hence not to be executed in parallel?**

If we are sure that our system/engine should not run parallel, we need to tell the scheduler by setting the `.exclusive` flag to true. It will not run in parallel with any other systems or engines in the entity context. If it is **false** then the components and writes will be used to determine parallelism.

**In which phase does it run?** 

We can define the `.phase` to tell the system in which phase we want our operation to run.

**What dependencies do I have?**

We can define dependencies by saying: `.before_me` and `.after_me`. We just pass the string hash of the other engine/system to this, and the scheduler does the rest.



## What is next?

In the next chapter we translate this to actual code!

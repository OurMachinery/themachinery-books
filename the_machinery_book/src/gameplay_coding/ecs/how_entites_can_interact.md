## How can we implement interaction between entities?

There are two problems in an ECS (Entity Component System) regarding the interaction between Entities: The **read** and the **write** access. 

The truth about the interaction between Entities is that interactions do not genuinely exist. They are hidden beneath the implementation of the underlying relationship. A relationship is then nothing else than the transformation of data.

To choose the right tool for creating those transformations, we need to reason about our code (and what we want to achieve) and ask ourselves the following five questions: 

- On what data do we operate? 
- What is our domain?
- What is the possible input for our transformation? 
- What is the usage frequency of the data? 
- What are we actually transforming?
- What could our algorithm look like? 
- How often do we perform our transformation?

For infrequent read access we can easily use the `tm_entity_api.get_component()` . It allows access to the underlying data directly from a provided entity. It is not recommended to use that for read-access because it is quite slow. You perform random data access. But again, if it is infrequent of the operation and the number of targets (Entities), which are interesting to choose the right tool.

> Here, you can use a System better than an `Engine`, since a System does not run in parallel and provides access to the Entity Context.



## The problem

When creating interactions between entities, we mainly face two types of problems:

1. **Read Access:** It means we have to read specific properties from a particular entity (object) and react based on this. **In terms of games:** An Actor needs to query/know some information from another part of the game. **For example, within a Quest System:** Have all tasks been completed?
2. **Write access:** It means we have to write specific properties to a particular entity (object).



**The transformation from \*Interaction\* towards \*Relationships\***



To start this transformation, we should have a quick look at the first principle of *Data-Oriented Design*:

> Data is not the problem domain. For some, it would seem that data-oriented design is the antithesis of most other programming paradigms because data-oriented design is a technique that does not readily allow the problem domain to enter into the software so readily. It does not recognize the concept of an object in any way, as data is consistent without meaning […] The data-oriented design approach doesn’t build the real-world problem into the code. This could be seen as a failure of the data-oriented approach by veteran object-oriented developers, as many examples of the success of object-oriented design come from being able to bring human concepts to the machine. In this middle ground, a solution can be written in this language that is understandable by both humans and computers. The data-oriented approach gives up some of the human readability by leaving the problem domain in the design document but stops the machine from having to handle human concepts at any level by just that same action — [Data Oriented Design Book Chapter 1.2](http://www.dataorienteddesign.com/)



This principle helps us recognize that interactions *do not truly exist. They hide the implementation of the underlying relationship*. A relationship is nothing else than a transformation of data. In the case of an ECS, the Entity Manager (In our case, Entity Context) can be seen as a database and the Entity as a Lookup table key that indexes relationships between components. 

The systems (or engines) are just here to interpret those relationships and give them meaning. Therefore, a system and engines should only do one job and do this well. 

Systems/Engines perform transformations of data. This understanding allows us to create generic systems which are decoupled and easy to reuse, and as such, we should keep the following in mind:

One of the main design goals for *Data-Oriented Design-driven* applications is to focus on reusability through decoupling whenever possible. 

> Thus, the Unix philosophy *Write programs that do one thing and do it well. Write programs to work together — McIlroy* is a good way of expressing what a system/engine should do.



Most ECS's are built with the idea of relationships in mind. When writing systems/engines, we transform data from one state to another to give the data meaning. Therefore systems/engines are defining the purpose of the data relationships. This decoupling provides us with the flexibility we need to design complex software such as video games. 

With such a design, we can modify behavior later on without breaking any dependencies.



>  *For example:*
>
> *You have one movement engine designed for the Player at first. Later on, you want to reuse it for all entities with a movement controller component. It contains the data provided by the Input System, such as which keys have been pressed. Therefore, an AI system can feed this as well for any other Unit (With the Movement Controller component, not the Player). The Movement Engine does not care about where the data comes from or who has it as long as it is present and the other needed component. (E.g. The Physics Mover or Transform)*



**How do we design Systems?**

To implement the before-mentioned relationships, we have to undertake a couple of steps. 

> These steps are also interesting for programmers who design gameplay systems. Having those fleshed out when they design game mechanics can be good and speed up your work. 

We have to ask the following questions:

**1.** What data transformations are we going to do and on which data? 

This question should lead to “what components do we need to create this relationship?” We should always be able to give a reason why we need this data.

**2.** What is our possible domain? (What kind of inputs do we have?)

When we figure this out, we can make the right decision later. Also, we can reason about our code and how to implement these relationships.

**3.** How often does the data change? 

To determine how often we change the data, we go through component by component and discuss how often we change it. This process is vital to pick the right tool. Knowing those numbers or tendencies is great for reasoning about possible performance bottlenecks and where we could apply optimizations.

**4.** What are we actually transforming?

Writing down the algorithm (in code or on paper) or the constraints of what we are actually doing with our data is a great solution.  To pick the right tool based on the planned algorithm, we need to consider the **cost** of our algorithm.

What does **cost** mean? It can mean anything from runtime costs to implementation costs. It is essential first to establish what the proper criteria are. The costs at the end enable us to reason about the code.

To pick the right tool, we need to reason about the costs an algorithm costs us. If we take run time performance as a measurement, it is okay to have a slow algorithm if we do not execute this frequently. If this is not the case, you should consider another solution.

**5.** How often do we execute the algorithm/transformation?

Based on the information we have already about the data we need for the transformation, it’s pretty easy to determine the execution frequency. The total number of entities/objects is known at this time. (It may be an estimation). Therefore, we can guess how often this might run. Keep in mind that we previously discussed how often we suspect the data to be changed. This leads to transparency, which gives a good idea of the costs of this code.

Keep in mind that the main goal is to keep things simple. A System/Engine should do one job. As the variety of components defines the data type of the Entity. And the combination of Systems/Engines defines the actual game behavior. Therefore you do not need to write diagrams, blueprints, pseudo-code or anything. You may even be able to just write the engine as one goal. It is recommended to do those steps even in your mind before you write your system.

> **IMPORTANT:** When the data changes, the problem changes. Therefore, we have to properly evaluate with the descriptive method the possible outcome and maybe change the implementation.

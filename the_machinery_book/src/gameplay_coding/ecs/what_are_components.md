## What are Components?

They are data, that is all they are. Designing them is the most important task you will find yourself doing in an ESC driven game. The reason is that if you change a component you have to update all systems that use it. This data composed together makes up an Entity. It can be changed at runtime, in what ever way required. This data is transformed in Systems/Engines and therefore Systems/Engines provide the Behaviour of our game based on the input/output of other Systems/Engines.

> **Note**:  Keep in mind they do not need a Truth Representation. If they do not have one, the Engine cannot display them in the Entity Tree View. This is useful for runtime only components.

- A component is defined by `tm_component_i` — it consists of a fixed-size piece of POD data.
- This data is stored in a huge buffer for each entity type, and indexed by the index.
- In addition, a component can have a *manager*.
- The manager can store additional data for the component that doesn’t fit in the POD data — such as
  lists, strings, buffers, etc.

You can add callbacks to the component interface which allow you to perform actions on `add` and `remove`. The general lifetime of a component is bound to the Entity Context.

![](https://www.dropbox.com/s/1d39bh17zqgeloy/tm_guide_ecs_component.png?dl=1)



> **It's all about the data**
>
> Data is all we have. Data is what we need to transform in order to create a user experience. Data is what we load when we open a document. Data is the graphics on the screen and the pulses from the buttons on your gamepad and the cause of your speakers and headphones producing waves in the air and the method by which you level up and how the bad guy knew where you were to shoot at you and how long the dynamite took to explode and how many rings you dropped when you fell on the spikes and the current velocity of every particle in the beautiful scene that ended the game, that was loaded off the disc and into your life. Any application is nothing without its data. Photoshop without the images is nothing. Word is nothing without the characters. Cubase is worthless without the events. All the applications that have ever been written have been written to output data based on some input data. The form of that data can be extremely complex, or so simple it requires no documentation at all, but all applications produce and need data. ([Source](https://www.dataorienteddesign.com/dodmain/node3.html))



### Best Practice

- **Component Size:** Keep them small and atomic. The main reason for this is  that it improves caching performance. Besides having a lot of small components allows for more reusability and compostability! Besides if they are atomic units of data, they increase their value to be reused across projects better and can provide more combinations. *The biggest disadvantage* is that small components make it harder to find them, the larger your project is.
- **Complex component data:** Generally speaking you want to avoid storing complex data such as arrays or heap allocated data in a component. It is possible and sometimes not possible to avoid, but it is always good to ask yourself if it is needed.


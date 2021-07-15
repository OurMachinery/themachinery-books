## Sculpt Tool

> **Note:** This tool is in a preview state.

With the Sculpt Tool The Machinery supportes rapid prototyping when it comes to level white boxing. You make use of the tool by adding a Sclupt Component to an Entity. Using the sculpt component you can quickly sketch out levels or make beautiful blocky art:

![A blocky character in a blocky forest setting.](https://ourmachinery.com/images/beta_20_11__blocky.png)

*A blocky character in a blocky forest setting.*

## How to use the Tool

To use the Sculpt Component, first add it to an entity, by right-clicking the entity in the *Entity Tree* and selecting *Add Component.* Then, select the newly created *Sculpt* component in the *Entity Tree*.

This gives you a new sculpt tool in the toolbar:

![Sculpt tool.](https://ourmachinery.com/images/beta_20_11__sculpt_tool.png)

*Sculpt tool.*

With this tool selected, you can drag out prototype boxes on the ground. You can also drag on an existing prototype box to create boxes attached to that box.

The standard *Select*, *Move*, *Rotate,* and *Scale* tools can be used to move or clone (by shift-dragging) boxes.

You can add physics to your sculpts, by adding a *Physics Shape Component*, just as you would for any other object. 

> **Note**: If you are cooking a physics mesh or convex from your sculpt data, you need to explicitly recook whenever the sculpt data changes.

Here is a video of sculpting in action:

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/YUyz1qPf1CM?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=ourmachinery.com"></iframe>

> **Note:** Currently, all the sculpting is done with boxes. We may add additional shape support in the future. 

## Additional though

In addition to being a useful tool, the *Sculpt Component* also shows the deep integration you can get with custom plugins in The Machinery. The *Sculpt Component* is a separate plugin, completely isolated from the rest of The Machinery and if you wanted to, you could write your own plugins to do similar things.
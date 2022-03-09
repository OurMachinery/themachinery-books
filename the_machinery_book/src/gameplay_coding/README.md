# Gameplay Coding in The Machinery

In this section, you will learn the basics about Gameplay Coding in *The Machinery.* There are two primary ways of creating a vivid and active world:

- Using our C APIs [API Documentation]({{docs}}apidoc.html).
- Using the [Visual Scripting Language]({{base_url}}editing_workflows/visual-scripting.html), which you can extend as well.

## Coding within our Entity Component System

The Machinery uses an Entity Component System; therefore, most of your gameplay code will run via Engines or Systems. To learn more about these, please follow this [link]({{base_url}}/gameplay_coding/ecs/index.html).

## General code entry points using Simulation Entry Component

The Machinery also offers you a Simulation Entry Component which will, when the parent entity is spawned, set up a system with that is used to run code at start-up and each frame. Read more [here]({{base_url}}gameplay_coding/simulation_entry.html).
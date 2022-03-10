## Prototypes

The Machinery has a prototype system that allows entity assets to be used inside
other entities. 

**Table of Content**

* {:toc}


So you can for example create an entity asset that represents a
room, and then create a house entity that has a bunch of these room entities
placed into it:

![Three Room entities placed to form a House entity.](https://www.dropbox.com/s/2hpnogh7bff9jge/house-entity.png?dl=1)



## Difference between a Prototype, an Instance and an Asset

We call the room asset a *prototype*, and we call each placed room entity an
*instance* of that prototype. Note that prototypes are not special assets, any
entity asset can be used as a prototype, with instances of it placed in another
entity asset.

In the Entity Tree tab, prototype instances are shown in yellow to distinguish them from locally
owned child entities (which are shown in white).

## Instance Properties: Inspect

If you expand an instance you will notice that most of its components and child entities are grayed
out and can't be selected. This is because they are inherited from the prototype, and the prototype
controls their values. If the prototype is modified — for example if we scatter some more props on
the floor — those changes are reflected everywhere the prototype has been placed. In the example
above, all three room instances would get the scattered objects.

## Instance Properties: Override

If we want to, however, we can choose to *override* some of the prototype’s
properties. When we override a property, we modify its value for *this instance*
of the prototype only. Other instances will keep the value from the prototype.

To initiate an override, right-click (or double click) the component or child entity whose
properties you want to override and choose **Override** in the context
menu. In addition to modifying properties, you can also add or remove components
or child entities on the overridden entity.

>  **Note:** If you override the property of some node deep in the hierarchy of the placed entity, all its
> parents will automatically get overridden too. Let's modify the position of the barrel in the
> front-most room:

![Barrel position overridden.](https://www.dropbox.com/s/uy0rzwhrjzen42i/override.png?dl=1)

The overridden entities and components are drawn in blue. We change the x and z components of the
position to move the barrel. Note how the changed values are shown in white, while the values that
are inherited from the prototype are shown in gray.

If you look back to the first picture you will see that the Link Component was
automatically overridden when the prototype was instanced. This is needed
because if we didn’t override the Link Component, it would use the values from
the prototype, which means all three room instances would be placed in the same
position.

When we override something on an instance, all the things not explicitly
overridden are still inherited from the prototype. If we modify the prototype —
for example change the barrel to a torch — all instances will get the change,
since it was only the x and z positions of the object that we changed.

## Instance Properties: Reset or Propagate

The context menus can be used to perform other prototype operations. For example,
you can **Reset** properties back to the prototype values. You can also
**Propagate** the changes you have made to an overridden component or entity
back to the prototype so that all instances get the changes. Finally, you can
**Remove** the overrides and get the instance back to being an exact replica of
the prototype.

## Other forms of prototypes: e.g. Graphs

Prototypes can also be used for other things than entities. For example, if you have a graph that
you want to reuse in different places you can create a Graph Asset to hold the graph, and then
instantiate that asset in the various places where you want to use it. Just as with the entity
instances, you can override specific nodes in the graph instance to customize the behavior.

TODO: Add link

## What is next?

- [How to create a prototype?]({{base_url}}/editing_workflows/prototype_workflow/how_to_create_prototypes.html)
- [How to instantiate Prototypes]({{base_url}}editing_workflows/prototype_workflow/how_to_instantiate_prototypes.html#how-to-instantiate-prototypes)

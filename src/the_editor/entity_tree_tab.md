# **Entity Tree Tab**

The **Entity Tree** shows the hierarchy of the entity you choose to edit. This view allows you to organize and add new entities as well as new components to the entities.



> **Note:**  Just be aware that the Entity Tree does not reflect the current runtime state. 



Besides, it is essential to remember is that *The Machinery* does not have specific *Scene* assets. A scene in *The Machinery* is just an entity with a lot of child entities.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625427931504_image.png)

**Table of Content**

* auto-gen TOC;
{:toc}
## How to edit a Scene / Entity

In this tab, you can edit any entity from the current project. To start editing, you can either use **Right Click → Open** or **Double Click** the entity to open them. This action will update the Scene Tab and the entity tree view tab. If you close the Scene Tab, the Entity Tree Tab will display an empty tree.



## Managing Entities
A Scene is composed of child Entities and Parent Entities. When you create a new project, it starts with a "world" entity. This entity can be edited and lives as `world.entity` in your Asset Browser. You can create other Entities that function as your Scene. Any entity in the Asset Browser can serve as your Scene. Later, when publishing your game, you can choose the world entity you like. 

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428013195_image.png)


Click a parent entity's drop-down arrow (on the left-hand side of its name) to show or hide its children. This action is also possible via the Keyboard: Arrow keys down and up let you navigate through the tree, while Arrow keys left and right allow you to show or hide the entity children. 

### Prototypes in the Entity Tree View

The Entity Tree view, prototype instances are shown in yellow to distinguish them from locally owned child entities (which are shown in white).

**Prototypes:** Prototypes are just entities that live in the Asset Browser as assets (.entity and the current entity in the Entity Tree View is based upon those entity assets. You can overwrite them in the Entity Tree View and make them unique, but any change to the asset will propagate to the entities based on the original prototype. [More here]({{base_url}}editing_workflows/prototype_workflow/index.html)

If you expand an instance, you will notice that most of its components and child entities are grayed out. They cannot be selected because they are inherited from the prototype, and the prototype controls their values.

![The light entity is an instance of a prototype and the Render Component is inherited](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428053926_image.png)

If the prototype is modified — for example, if we scatter some more props on the floor — those changes reflect everywhere the prototype is placed.

### Adding new child entities
When you want to reorder one entity as a child to another, you can drag and drop them on them onto each other.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428282189_sort_entity_tree.gif)


You can add new children to an Entity through right-click and *"Add Child Entity"* or dragging an Entity Asset from the Asset Browser into the Entity Tree View.

### Searching and changing the visibility of Entities
You can search for entities via the filter icon, and you can hide all the components with the little *gear* icon next to it. You can also change the visibility of each entity via the little *eye* icon next to its name. If you change the visibility, you will hide the entity in the Scene View.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428346946_image.png)


The Lock Icon makes sure you cannot select the entity in the Scene Tab. It can help to avoid miss-clicking.

## Keyboard bindings

| Key                | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| Arrow Up & Down    | Navigate through the tree                                    |
| Arrow Left & Right | Expand or collapse the selected Entities                     |
| F                  | Selected Entity will be framed in Scene Tab                  |
| H                  | Selected Entity will be hidden in Scene Tab                  |
| F2                 | Start renaming the selected Entity                           |
| F3                 | Adds child entity to parent                                  |
| Space              | Opens Add Component menu to selected Entity                  |
| Space + Shift      | Open Add Entity Menu to add child entity                     |
| CTRL + L           | Moves selected entities one level up in the Entity Hierarchy |
| CTRL + F           | Opens the filter / search menu                               |
| CTRL + H           | Don’t show components in the Entity Tree                     |
| CTRL + D           | Duplicates selected Entities                                 |
| CTRL + C           | Copies Entities                                              |
| CTRL + V           | Pastes Entities                                              |
| CTRL + X           | Cuts Entities                                                |

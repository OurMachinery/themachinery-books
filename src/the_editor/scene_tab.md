# Scene Tab

The **Scene** tab is the view into your world. You can use the **Scene tab** to select, manipulate assets, and position new ones in your world. 

**Table of Content**

* {:toc}


## Navigate through your Scene
The Scene Tab allows for different ways of navigating through your world. The primary method of navigating through the Scene is via the mouse and the keyboard. 

**Movement**

- **Middle Mouse Button:** Keep pressed down to move through the scene.
- **Left Mouse Button:** Keep pressed down to rotate in the Scene by rotating the mouse. If you keep the mouse pressed so you can also use **WASD** to move through the Scene. To increase or decrease the movement speed, you need to move the mouse wheel.

**Zoom in**

- **Mouse Wheel**: To zoom in, you can zoom in or out via the mouse wheel.

**Frame Entities or the scene**


- **Press F**: To frame the currently selected entity or if you have nothing selected the Scene. Alternatively, you can double click on an entity the Entity Tree Tab.

### Opening an Entity Asset
Through a double click on an Entity Asset in the Asset Browser, you will load the asset. If you want to move between previously loaded entities, the toolbar provides a back and forth navigation option.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428401593_image.png)


Alternatively, you can use the context menu of the tab label and navigate through the previously focused entities.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428456420_image.png)

## Working in the Scene
The Scene tab comes with tools that allow for editing and moving entities in the current Scene.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428493292_image.png)


The main tools you will be working with in to edit the scene are the

- **Select Tool**: To select Entities in the Scene
- **Move Tool**: For moving Entities in the Scene
- **Rotate Tool**: Rotates selected Entities
- **Scale Tool**: Scales Entities
- **Snapping:** Enable or disable snapping and the snap distance

You can manipulate the Grid via **Main Menu → Scene → Grid Settings**.

If you do not like the layout of the current toolbar, you can change its layout by dragging them around.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428649231_new_order_toolbars.gif)



### Box Select in the Scene Tab

The Machinery now supports a long awaited feature — box selection.

To select multiple items in the scene, simply drag out a selection rectangle with the mouse:


![Box dragging to select multiple entities.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617220755615_image.png)


The touched entities will become selected in the scene:


![The resulting selection.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617220785668_image.png)



## Simulate your Scene or change visualization modes
You can simulate your current Scene and manipulate the way your Scene's visualization with this toolbar:

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428527987_image.png)

- The simulation button ▶: Simulates your scene in a new tab if no simulation tab is open.
- The camera button 📷: Allows you to change the camera in your viewport.
- The light button 💡:  Use Lighting Environment Asset. Will create a lighting environment in the scene. Automatically enabled for assets with no light.
- Visualize button: Allows to enable more visualization modes.
  - Lighting Model
    - Visualize Albedo
    - Visualize Normals
    - Visualize Specular
    - Visualize Roughness
    - Visualize Shadow Maps
    - Visualize Pixel Velocity
    - Visualize NaN / INF
    - Show as Overlay
  - Exposure
    - Visualize EV100
    - Visualize Histogram

## Keyboard bindings

| Key                     | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| F                       | Frames either the current scene if nothing is selected or the selected objects |
| G                       | Enables and disables the Grid                                |
| ESC                     | Deselect objects                                             |
| CTRL + D                | Duplicates selected objects                                  |
| Shift + Drag with mouse | Duplicates selected objects                                  |
| CTRL + C                | Copies object                                                |
| CTRL + V                | Pastes object                                                |
| CTRL + X                | Cuts object                                                  |

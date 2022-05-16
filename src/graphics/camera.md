# Camera

In The Machinery a [camera]({{docs}}plugins/entity/camera_component.h.html) is an object that converts the simulated world into a two-dimensional image. It can do this with in a physically plausible way or in a more arcade way depending on how it is set up. The method chosen is called the projection mode and The Machinery offers three modes: Perspective, Orthographic, and Physical.


## Adding a camera to the scene

A camera must be used to view any scene, the [Scene Tab]({{base_url}}the_editor/scene_tab.html) therefor starts with a default camera. But once you wish to simulate this world an additional camera is needed. This can be done by adding a Camera Component to any entity in the scene and setting it as the viewing camera using the Set Camera node.

![](https://www.dropbox.com/s/7cwc768hu7ltll4/tm_guide_camera_tree_tab.png?raw=1)

![](https://www.dropbox.com/s/foeulmeuaef5c2j/tm_guide_camera_graph.png?raw=1)


You can see a preview of the newly added camera in real time in the [Preview Tab]({{base_url}}the_editor/preview_tab.html) when selecting the camera component.

![](https://www.dropbox.com/s/y7rafonxt7abm7h/tm_guide_camera_perspective.png?raw=1)

## Customizing the camera

The first thing to consider when adding a camera to a scene is which projection mode it should use. \
**Perspective** is the default projection mode. This projection mode linearly projects three-dimensional objects into two-dimensions, this was the effect that objects further away from the camera appear smaller than objects near the camera. This camera is controlled by changed the Vertical Field of View property. \
**Physical** cameras use the same projection as perspective cameras, but instead of controlling the camera using FoV, this camera is controlled using focal length. This camera is intended for users familiar with real world cameras and aims to be more physically descriptive than its protective counterpart. \
**Orthographic** cameras use parallel projection instead of linear projection. This means that depth has no impact on the objects scale. These cameras are often useful when making a 2D or isometric game. This camera is controlled using the box height property.

![Orthographic camera](https://www.dropbox.com/s/qpk260eul8fms22/tm_guide_camera_orthographic.png?raw=1)


Additionally all projection modes define near and far plane properties. These directly correlate to the visible range of the camera. Lowering the visible range can improve precision within that range which might reduce depth artifacts. But this can also be used to create impossible shots, like being able to view through walls.

![Setting the near plane to 4 allows us to place the camera outside of the room whilst still being able to view into it.](https://www.dropbox.com/s/8l33j979p9spfty/tm_guide_camera_near_clipping.png?raw=1)


## All camera properties

| **Property**                        | **Description**                                                                                                                                                                                                                                                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Projection Mode                     | Specifies which projection mode to use.                                                                                                                                                                                                                                                                                                                                  |
| Near Plane                          | Specifies the near clipping plane of the camera.                                                                                                                                                                                                                                                                                                                         |
| Far Plane                           | Specifies the far clipping plane of the camera.                                                                                                                                                                                                                                                                                                                          |
| Vertical FoV (**Perspective Only**) | Specifies the vertical field of view of the camera (in degrees in the editor, and in radians in code).                                                                                                                                                                                                                                                                   |
| Box Height (**Orthographic Only**)  | Specifies the height of the box used for orthographic projection in meters.                                                                                                                                                                                                                                                                                              |
| Focal Length (**Physical Only**)    | Specifies the distance between the lens and the image sensor in millimeters.                                                                                                                                                                                                                                                                                             |
| ISO                                 | Specifies the sensor’s ISO sensitivity with 100 being native ISO. This property can be used by the exposure and film grain post process effects if these are set to use the camera properties. Otherwise this property is ignored.                                                                                                                                       |
| Shutter Speed                       | Specifies the time (in seconds) the camera shutter is open. The longer the shutter is open the more light hits the sensor, which brightens the image, but also increases the motion blur. This property is only used when the respective post-processing effects are set to use the camera properties.                                                                   |
| Sensor Size (**Physical Only**)     | Specifies the size of the camera’s sensor in millimeters. This property can be used for image gating when desired. It also plays a role in the focus breathing effect.                                                                                                                                                                                                   |
| Focus Distance                      | Specifies the distance in meters to the point of perfect focus. If the depth-of-field post process effect is active, then any point not on the focal plane will become blurry.                                                                                                                                                                                           |
| Aperture                            | Specifies the aperture ratio of the lens. This is expressed as an f-number or f-stop. Smaller f-numbers relate to larger diaphragm openings in the lens which allow more light onto the sensor. This brightens the image, but also lowers the depth of field. This property is only used when the relative post-processing effects are set to use the camera properties. |

## Example

The properties of the camera can be manipulated to create interested and film like effects. For example, by decreasing the focal length whilst dollying the camera backwards we can create a [Dolly Zoom](https://en.wikipedia.org/wiki/Dolly_zoom) effect. 

<video  controls>
  <source src="https://www.dropbox.com/s/ty552e9hchgmhue/tm_guide_camera_dolly_zoom.mp4?raw=1" type="video/mp4">
Your browser does not support the video tag.
</video>

## Camera Effects

The Machinery can simulate various camera effects as desired. These are implemented as separate components to allow full freedom in their application. Currently the following effects are available:

| **Effect**     | **Description**                                                                                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Bloom]({{base_url}}/graphics/post_processing/bloom.html)       | The bloom effects adds fringes of light extending from the borders of bright areas of the scene. This simulates the real world glow that comes from viewing bright lights through a lens.                                            |
| [Exposure]({{base_url}}/graphics/post_processing/exposure.html) | Exposure controls the amount of light that hits the sensor. This has the effect of brightening or darkening the scene as desired. This can either be set using real world camera parameters or automatically as the human eye would. |
| Depth of Field                                         | Real world lenses cannot focus on the entire scene at the same time. The depth of field effect simulated this be blurring out of focus areas of the scene.                                                                           |


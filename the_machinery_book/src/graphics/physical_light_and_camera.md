# Physically based light and cameras

The Machinery’s default render pipeline uses exclusively physically based rendering for accurate and predictable results based on real-life measurements. Using physically based units to set light intensity and camera parameters are therefor paramount to synthesizing accurate images. These units are widely used in the real-world, like on light bulb packaging, DSLR-cameras, and light meters.


## Basics of physical light

For the purposes of real-time rendering we can split up light into two parts: the luminous flux and the chromaticity. Here the luminous flux is the strength of power of the light source, i.e. the more luminous flux the brighter the light. The chromaticity on the other hand is the color of the light regardless of its luminance. 

Note that when we talk about luminous flux we are referring to the total amount light emitted from the source, not the light received by an object. In this case we would refer to illuminance, which is the total amount of light falling on a given surface. This distinction is important as The Machinery allows the user to specify their light intensity in both luminance and illuminance, where illuminance assumes a unit area (1 m^2) for the light to fall on.

![By Jrh.main - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=69452076](https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Illuminance_Diagram.tif/lossy-page1-1280px-Illuminance_Diagram.tif.jpg)


The Machinery supports a wide range of light units. It is up to the user to determine which light unit they wish to use. The available units are:

| **Unit**            | **Type**           | S**hort Description**                                                                                         |
| ------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| Candela (cd)        | Luminous Intensity | Scientific measurement of light being emitted in a certain direction.                                         |
| Lumen (lm)          | Luminous Flux      | Total amount of light emitted from a source. This is easiest to reference with real-world artificial lights.  |
| Lux (lx)            | Illuminance        | Amount of light hitting one square meter. Most useful for directional lights.                                 |
| Nits                | Luminance          | Total light intensity of an area light. Easy to reference with real-world monitors and TVs.                   |
| Exposure Value (EV) | Camera             | Units relative to the viewing camera. Easiest unit to use if you’re not familiar with physically based units. |



### Candela (cd)

Candela is the SI base unit of luminous intensity (not to be confused with luminous flux). It measures the amount of light emitted in a particular direction as perceived by the human eye. Candela is mainly useful when accurate measurements relative to the human eye are required. A common wax candle emits light with a luminous intensity of roughly one candela. Because of its scientific nature; we only allow the use of candela for punctual light sources (point and spot lights) as they have a well defined area of effect.


### Lumen (lm)

Lumen is the SI unit used to measure luminous flux. This measures the total amount of light emitted by a light source relative to the human eye. Lumens are useful units when describing artificial light sources like lamps. Therefor they are available for punctual light sources (point and spot lights) and area lights. The amount of lumen produced by an artificial light source can often be found on the light bulb’s box. For instance a decorative light might emit about 30 lm, whilst a interior light might emit 1000 lm.


### Lux (lx)

Lux is an SI derived unit for illuminance and is equal to one lumen per square meter. The Machinery uses a scaled version of lux as its main light unit when rendering, meaning this unit is almost directly mapped to the rendering pipeline. Lux is particularly useful when describing a light source that doesn’t have a well defined source (like directional or IBL lights). Lux can be measured by devices available to the consumer. For reference, a starlit night might produce 0.001 lx, whilst a overcast day might produce around 1000 lx. 


### Nits (cd/m^2)

The Nit is an SI derived unit for luminance and is equal to one candela per square meter. It describes how much light in emitted from a particular area and is therefor only available for area lights as they have a well defined area. Nits are particularly useful when modeling a virtual display as most displays specify their brightness on the box using Nits. For example, the sRGB specification targets monitors at 80 Nits, most LCD consumer monitors are around 300 Nits, and HDR monitors can range from 450 to 1600 Nits.


### Exposure Value (EV)

Exposure Value is a derived unit for illuminance relative to a camera at ISO level 100. Although not a unit of light, exposure value is a very useful unit as it describes light intensity in a more human readable way. For example 1 EV is about a moonlit night, whilst 10 EV is an overcast scene. Exposure value is available for all light sources as it describes intensity as perceived by a camera.


### Chromaticity

Light color can be described using various specifications in The Machinery. The most artist friendly ways of specifying light color being RGB and HSV. Both of these methods employ a trichromacy model to describe color which is assumed by most models in color science. Another way to specify color is using color temperature with Kelvin. This is often used in the real world for light bulbs to indicate which hue is emitted by them, ranging from a dark orange to a light blue. For example 1850 K specified the hue emitted by a wax candle, whilst 3000 K is often closer to LED's. 


## Basics of physical cameras

The use of physically based light can create a scene which has greater accuracy than a scene without regards for physical correctness, however any scene in inevitably viewed through a camera. Using the physical camera with post processing effects based on that camera greatly increases the accuracy of the synthesized scene. Note that this is not always desired as it comes as the cost of artist flexibility and requires the user to be familiar with real-world cameras. This section will focus on the physical camera, for more information about camera in general see [Camera].

Real-world camera setups can be roughly divided into two parts, the camera itself and the lens. If a first-person view is desired than the brain can be though of as the camera, whilst the eye will function as the lens. Here the camera is the object that transforms the visible scene into an image whilst the lens modifies the view that the camera has into the scene.

![http://www.rags-int-inc.com/phototechstuff/lens101/LensDiagram_1024.gif](http://www.rags-int-inc.com/phototechstuff/lens101/LensDiagram_1024.gif)


The diagram above shows a simplified diagram of how a real-world camera projects the scene onto the sensor. In The Machinery we don’t simulate all aspects of a real-world camera, as that would be too expensive for games. Instead we use a [thin lens](https://en.wikipedia.org/wiki/Thin_lens) model or a simple [pinhole camera](https://en.wikipedia.org/wiki/Pinhole_camera) based on the desired post-processing effects. This means that the physical camera has the following properties which should be familiar to anyone who has worked in the field of photography.

| **Property**   | **Short Description**                                                       |
| -------------- | --------------------------------------------------------------------------- |
| Focal Length   | The distance in millimeters from the center of the lens to the focal plane. |
| Shutter Speed  | The amount of seconds that the shutter allows light onto the sensor.        |
| Aperture       | The aperture size in f-stops.                                               |
| ISO            | The sensors sensitivity, 100 is the native sensitivity.                     |
| Sensor Size    | The physical size of the sensor in millimeters.                             |
| Focus Distance | The distance in meters from the focal plane to the object in perfect focus. |

### Focal Length

The focal length the lens specified how strongly the lens converges or diverges the incoming light. This is mainly determined by the curvature of the lens. i.e. the thicker the lens the shorter the focal length. This is also the main driver behind the field of view of the camera. A long focal length (i.e. a thin lens) creates a narrow field of view, whilst a short focal length (i.e. a thick lens) creates a wide field of view. When zooming in on a physical camera you would increase the focal length of the camera by physically moving one or more lens elements forwards in the lens. Conversely, to zoom out you would decrease the distance between one or more lens elements and the image sensor.


### Shutter Speed

The shutter speed of the camera determines how long light is allowed to fall onto the camera sensor. The more light is allowed onto the sensor the brighter the image, which might be required in dark scenes. But, this introduces motion blur as subjects move whilst the frame is being taken. conversely in bright scenes the shutter speed could be very short which makes motion blur less noticeable. In The Machinery motion blur is an (not yet implemented) optional post-processing effect, and increasing the shutter speed doesn’t actually change the time it takes to take a frame.


### Aperture

The aperture of a lens describes the size of the opening that allows light to pass onto the sensor. Just like with shutter speed, the more light is allowed onto the sensor the brighter the image. But, when the aperture is opened it lowers the depth of field. The aperture of the lens isn’t actually specified as a physical size, instead a ratio is used between the focal length of the lens and the diameter opening, this ratio is often referred to as f-stops or f-numbers. Perhaps unintuitively, as the f-number decreases the lens diaphragm opens increasing the lens opening.


### ISO

The ISO of the camera specifies the sensitivity of the camera sensor to light. A more sensitive sensor captures more light which brightens the image, but this introduces noise and film grain on the final frame. Note that film grain is an (not yet implemented) optional post-processing effect.


### Sensor Size

The width and height of the sensor in millimeters. This is the second driver behind the final field of view of the camera. The size of the sensor should also impact the aspect ratio of the final frame, but this is not yet implemented. Typically the sensor size would be set to a constant value and a fitting algorithm would determine how the image is displayed on the users screen. For example, by stretching or cropping the image.


### Focus Distance

The focus distance of the camera determines at which distance the an objects needs to be from the camera to be in perfect focus. This parameter is only used when the depth-of-field post-processing effect is active. The focus distance is proportional to the focal length and the image distance.


## Additional Resources
- [The Candela](https://www.lne.fr/en/learn-more/international-system-units/candela): An academic resource on the SI units of light.
- [The Challenges of High-Speed Filming](https://www.youtube.com/watch?v=_lZvF-YyP0s): visual explanation of shutter speed and aperture relative to exposure.


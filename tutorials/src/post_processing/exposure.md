# Adjusting exposure

In photography, exposure is the amount of light per unit area. The Machinery uses physically based lighting, materials, and cameras so setting up the scene exposure correctly is important to getting the final image looking correct. To start using exposure add an `Exposure Component` to your scene.


## Tools

Exposure is generally measured in EV100 ([Exposure Value](https://en.wikipedia.org/wiki/Exposure_value) at ISO 100) or [IRE](https://en.wikipedia.org/wiki/IRE_(unit)). Both can be visualized in The Machinery in the `Render/Exposure/` menu.

![EV100 Visualization](https://www.dropbox.com/s/8spmtkfs33jf7xw/tm_tut_exposure_ev100.png?dl=1)


The EV100 visualizer shows the luminance per pixel relative to the camera’s exposure range. By default the camera has a range of [-1, 15], but in this scene it is [-1.2, 15]. In this view higher values mean higher luminance. Note that this is an absolute scale, values in the higher and lower ranges might be clipped after exposure is applied.


![IRE Visualization](https://www.dropbox.com/s/6sygin0tafnxdfk/tm_tut_exposure_ire.png?dl=1)


The IRE visualizer (false color) shows the luminance per pixel after exposure. This scale is relative to the dynamic range of sRGB. The view works by splitting the luminance range into bands (where red is fully clipped at the top range). This view is useful when exposing to a specific element in your scene. The [43, 47] (green) band is the typical range for middle grey and the [77, 84] band is a typical Caucasian skin tone.

The machinery offers three workflows for metering exposure:

- Manual: this mode is easy to use for static scenes where you want to focus on a specific luminance range.
- Camera Driven: this mode is best used if you prefer to recreate a real world camera. This mode requires some understanding of real world camera properties.
- Automatic: this mode (also known as eye adaptation) is best used on characters or other moving cameras in your scene.


## Using manual exposure
![](https://www.dropbox.com/s/568lt9m1jcdlxqb/tm_tut_exposure_manual.png?dl=1)


Manual exposure just has one setting to change, `Exposure Compensation`. This value is added to the target exposure (zero for manual mode). Therefor this value should be increased if the luminance of the scene is increased as well (higher compensation corresponds to a darker scene).


## Using camera driven exposure
![](https://www.dropbox.com/s/reniyj1qgfgc3dr/tm_tut_exposure_camera_driven.png?dl=1)


Camera driven exposure has no settings of its own. Instead the `Shutter Speed`, `Aperture`, and `ISO` settings are using from the viewing camera. This mode is best used if you have a good understanding of camera properties, but in general: lowering shutter speed darkens the scene, increasing aperture (f-number) darkens the scene, and lowering ISO darkens the scene.


## Using automatic exposure
![](https://www.dropbox.com/s/btprh1pkb273q7r/tm_tut_exposure_automatic.png?dl=1)

![](https://www.dropbox.com/s/axil4eizps5oiwk/tm_tut_exposure_histogram.png?dl=1)


Automatic exposure uses a histogram to calculate the average exposure value of the scene and exposes to it accordingly. The histogram can be visualized in the `Render/Exposure/` menu. The settings for this mode are:

- Min/Max EV100: these settings define the acceptable range of the automatic exposure, any value outside of this range is clamped to the outer buckets.
- Exposure Compensation: this allows you to offset the target exposure by a specific amount, unlike in manual mode; this setting is linear.
- Speed Up/Down: these settings allow you to alter the speed at which the automatic exposure interpolates to the target value. By default it will expose faster to a change upwards rather than downwards.
- Mask Mode: this allows you to weigh the scene samples based on a mask. Currently the only supported mask is `Favor Center` which weighs the samples at the center of the screen higher than the edges. 


## General workflow

Let’s use the tools to manually expose this scene. Note that there is no right way to apply exposure to a scene. The example shown below is meant to be a bit dark, so making it brighter might go against the artistic direction.

![](https://www.dropbox.com/s/phk7fzqyqz623ql/tm_tut_exposure_example_source.png?dl=1)

![](https://www.dropbox.com/s/rl8hwrwl72yxnk5/tm_tut_exposure_example_source_ire.png?dl=1)


In the false color visualization we can see that there are many areas where the scene is too dark to distinguish the colors. We can also see a little bit of bright clipping on the top side of the rock. The background sky on the other hand is pretty well exposed. Let’s try to brighten up the scene to focus more on the foreground rather than the background. I’ve done this by decreasing the exposure compensation from -0.4 to -1.3.

![](https://www.dropbox.com/s/yjm0vbr6pyy9axq/tm_tut_exposure_example_dest.png?dl=1)

![](https://www.dropbox.com/s/xslx4rbbq3zqe4b/tm_tut_exposure_example_dest_ire.png?dl=1)


You can see that the scene feels a lot brighter (and somewhat warmer) than before. The foliage has noticeably more detail and the highlight on the rock is more pronounced. The sky in the background is now clipping a lot, but it is not as noticeable.

## Localized exposure

Often times you want to have exposure settings localized to a specific region in your scene. This is done using the `Volume Component`. Once the camera enters a region defined by the volume component it will use the highest order exposure component it can find. In this example it would use the exposure component on the same entity as the volume component if the camera is inside the volume and the global exposure component if it’s outside the volume. For more information see the volume component documentation.

![](https://www.dropbox.com/s/pluala3w4h59gx9/tm_tut_exposure_volume.png?dl=1)
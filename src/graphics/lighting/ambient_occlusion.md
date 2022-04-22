# Ambient Occlusion

Ambient Occlusion is an effect as part of global illumination that approximates the attenuation of light due to occlusion. 

![SSAO](https://www.dropbox.com/s/9hemw29ib130jf3/tm_tut_ssao.png?dl=1)

The easiest way to get AO in your scene is by adding SSAO component which is a method that calculates ambient occlusion in screen space using the depth and normal buffer from the GBuffer rendering pass.

| **Property** | **Description** |
| :-- | :----- |
| Radius       | Defines the sample radius in world space units. Larger radius needs more step count to be more correct but higher step count can hurt performance. Having larger radius also makes cutoffs on the edges of the screen more visible because screen space effects don't have scene information outside of screen. |
| | &nbsp;![SSAO radius compare](https://www.dropbox.com/s/pcekns9g3qbzh5d/tm_tut_ssao_radius_comp.png?dl=1) *SSAO with radius set to 1(Left) &nbsp; SSAO with radius set to 5(Right)*|
| Power        | Controls the strength of the darkening effect that, increases the contrast.|
| | &nbsp;![SSAO power compare](https://www.dropbox.com/s/ktp9l66mmqptrrk/tm_tut_ssao_power_comp.png?dl=1) *SSAO with power set to 1.5(Left) &nbsp; SSAO with power set to 3.0(Right)* |
| Bias         | Depth buffer precision in the distance and high-frequency details in normals can cause some artifacts and noise. This parameter allows you to tweak it. But higher value will reduce details. |
| | &nbsp;![SSAO power compare](https://www.dropbox.com/s/m1h2qic1g7fpwh0/tm_tut_ssao_bias_comp.png?dl=1) *SSAO with bias set to 0.0(Left) &nbsp; SSAO with bias set to 0.1(Right)* |
| Step Count   | The number of depth samples for each sample direction. This property has direct corelation with performance. Keeping it in 4-6 range will result optimal performance/quality ratio. |

## Technical Details

The SSAO implementation is based on the slides from [Practical Real-Time Strategies for Accurate Indirect Occlusion](https://blog.selfshadow.com/publications/s2016-shading-course/#course_content) presented at Siggraph 2016. It consist of 4 passes:
 - **Half Screen Trace Pass:** Calculates the horizon for a sample direction and the corresponding occlusion with 4x4 noise.
 - **Half Screen Spatial Denoiser:** Resolves that 4x4 noise with a bilateral 4x4 box blur.
 - **Half Screen Temporal Denoiser:** Temporally stables the result from spatial blur. Increases the sample count and reduces the flickering.
 - **Full Screen Bilateral Upscale:** Depth aware upscale pass that brings the denoised AO target to full resolution.

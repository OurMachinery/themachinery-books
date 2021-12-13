# Bloom

Bloom (or glow) is an effect for real world lenses that produces fringes of light that extend from the borders of bright areas in the scene. It is produced by diffraction patterns of light sources through a lens aperture. This particularly affects lights sources and emissive materials.
In The Machinery this is implemented as multiple Gaussian blurs that only affect the bright areas on the scene.

![Bloom On (left) and Off (right)](https://www.dropbox.com/s/zqx30bzzt86rqyo/tm_tut_bloom_on_off.png?dl=1)

| **Property** | **Description**                                                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Threshold    | The luminance threshold for bloom to start considering a sample. This is roughly measured in Lux.                                                           |
| Falloff      | Defines the size of the bloom fringes. More falloff means larger fringes.                                                                                   |
| Tint         | A chromatic tint mask that will be applied to the bloom effect. Setting this to black will render the bloom effect useless without any performance benefit. |
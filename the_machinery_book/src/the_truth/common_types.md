# Common Types

The Truth comes with several useful common types. You can find them in the `the_truth_types.  ([API Documentation]({{docs}}foundation/the_truth_types.h.html#structtm_the_truth_common_types_api)).



| Macro                                                        | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `TM_TT_TYPE__BOOL`/`TM_TT_TYPE_HASH__BOOL` | The first property contains the value.                       |
| `TM_TT_TYPE__UINT32_T`/`TM_TT_TYPE_HASH__UINT32_T` | The first property contains the value.                       |
| `TM_TT_TYPE__UINT64_T`/`TM_TT_TYPE_HASH__UINT64_T`| The first property contains the value.                       |
| `TM_TT_TYPE__FLOAT`/`TM_TT_TYPE_HASH__FLOAT`| The first property contains the value.                       |
| `TM_TT_TYPE__DOUBLE` /`TM_TT_TYPE_HASH__DOUBLE` | The first property contains the value.                       |
| `TM_TT_TYPE__STRING`/`TM_TT_TYPE_HASH__STRING` | The first property contains the value.                       |
| `TM_TT_TYPE__VEC2`/`TM_TT_TYPE_HASH__VEC2` | The first property contains the x value and the second the y value. |
| `TM_TT_TYPE__VEC3`/`TM_TT_TYPE_HASH__VEC3`| The first property contains the x value and the second the y value and the third the z value. |
| `TM_TT_TYPE__VEC4`/`TM_TT_TYPE_HASH__VEC4`| The first property contains the x value and the second the y value and the third the z value while the last one contains the w value. |
| `TM_TT_TYPE__POSITION`/`TM_TT_TYPE_HASH__POSITION` | Same as `vec4`.                                              |
| `TM_TT_TYPE__ROTATION`/`TM_TT_TYPE_HASH__ROTATION` | Based on a `vec4`. Used to represent the rotation of an object via quaternions. |
| `TM_TT_TYPE__SCALE`/`TM_TT_TYPE_HASH__SCALE` | Same as `vec3.`                                              |
| `TM_TT_TYPE__COLOR_RGB`/`TM_TT_TYPE_HASH__COLOR_RGB`| Represents a RGB colour.                                     |
| `TM_TT_TYPE__COLOR_RGBA`/`TM_TT_TYPE_HASH__COLOR_RGBA`| Represents a RGBA colour.                                    |
| `TM_TT_TYPE__RECT`/`TM_TT_TYPE_HASH__RECT` | The first property contains the x value and the second the y value and the third the width value while the last one contains the height value. |

There is a helper API to handle all of these types in an easy way, to reduce the boilerplate code: `tm_the_truth_common_types_api`. 

> **Note:** There is a list of all Truth Types the Engine comes with available on our [API Documentation]({{docs}}truth_types.html)

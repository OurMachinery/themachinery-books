# Creating tab layouts through code

The Machinery allows you to fully customize the editor layout. For personal layouts this system can be fully utilized without using code (see [Interface Customizations]({{the_machinery_book}}the_editor/customizations) for more information), but you might want to create custom default layouts that get defined procedurally, this allows for more control when loading and saving the layout.

Creating layouts in code can be done though the `tm_tab_layout_api`. Here various functions are available for tab management. In this tutorial we’ll go over how the default workspace is created using the `save_layout` function.

In order to create a layout for The Machinery editor we need access to the editor settings. This is done through `tm_the_machinery_api`. This tutorial uses the `tm_the_machinery_create_layout_i` interface in order to gain access to the settings. In these settings we have access to the window layouts, which is the subobject we want to append our layout to. The first things we should do however is check whether our layout already exists so we don’t create a new one every time on startup.

```c
static void create_layout(tm_application_o *app)
{
	TM_INIT_TEMP_ALLOCATOR(ta);

	// Query the settings object and Truth from The Machinery API.
	tm_tt_id_t app_settings_id;
	tm_the_truth_o *tt = tm_the_machinery_api->settings(app, &app_settings_id);
	const tm_tt_id_t window_layouts_id = tm_the_truth_api->get_subobject(tt, tm_tt_read(tt, app_settings_id), TM_TT_PROP__APPLICATION_SETTINGS__WINDOW_LAYOUTS);

	// Check whether our layout already exists.
	const tm_tt_id_t *window_layouts = tm_the_truth_api->get_subobject_set(tt, tm_tt_read(tt, window_layouts_id), TM_TT_PROP__WINDOW_LAYOUTS__LAYOUTS, ta);
	const uint32_t num_window_layouts = (uint32_t)tm_carray_size(window_layouts);
	for (uint32_t i = 0; i < num_window_layouts; ++i) {
		const tm_strhash_t name_hash = tm_the_truth_api->get_string_hash(tt, tm_tt_read(tt, window_layouts[i]), TM_TT_PROP__WINDOW_LAYOUT__NAME);
		if (TM_STRHASH_EQUAL(name_hash, TM_LAYOUT_NAME_HASH)) {
			TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
			return;
		}
	}
```

After this we can start to define our actual tab layout. This is done through the `tm_tab_layout_t`. In this layout we can recursively define our tab layout with three distinct options per tabwell.

- We can split the tabwell horizontally, creating top and bottom child tabwells.
- We can split the tabwell vertically, creating left and right child tabwells.
- We can define (up to 3) tabs that should be in this tabwell.
![](https://www.dropbox.com/s/ggiq4uv6htgwnpj/tm_tut_default_layout.png?dl=1)

```c
tm_tab_layout_t tabs = {
	.split = TM_TAB_LAYOUT_SPLIT_TYPE__HORIZONTAL,
	.bias = 0.25f,
	.top = &(tm_tab_layout_t){
		.split = TM_TAB_LAYOUT_SPLIT_TYPE__VERTICAL,
		.bias = 0.67f,
		.left = &(tm_tab_layout_t){
			.split = TM_TAB_LAYOUT_SPLIT_TYPE__VERTICAL,
			.bias = -0.67f,
			.right = &(tm_tab_layout_t){ .tab = { TM_SCENE_TAB_VT_NAME_HASH } },
			.left = &(tm_tab_layout_t){ .tab = { TM_TREE_TAB_VT_NAME_HASH } },
		},
		.right = &(tm_tab_layout_t){ .tab = { TM_PROPERTIES_TAB_VT_NAME_HASH } },
	},
	.bottom = &(tm_tab_layout_t){
		.split = TM_TAB_LAYOUT_SPLIT_TYPE__VERTICAL,
		.bias = 0.5f,
		.left = &(tm_tab_layout_t){
			.split = TM_TAB_LAYOUT_SPLIT_TYPE__VERTICAL,
			.bias = -0.5f,
			.right = &(tm_tab_layout_t){ .tab = { TM_ASSET_BROWSER_TAB_VT_NAME_HASH } },
			.left = &(tm_tab_layout_t){ .tab = { TM_CONSOLE_TAB_VT_NAME_HASH } },
		},
		.right = &(tm_tab_layout_t){ .tab = { TM_PREVIEW_TAB_VT_NAME_HASH } },
	},
};
```

Defining the tabs is relatively straight forward, you define them using their name hash. Splitting a tabwell horizontally or vertically however requires a `bias` parameter. This defines the ratio of both tabs. Zero means both tabs are of equal size, whereas 1 means that the primary tab (left or top) fully encompass the tabwell whilst the secondary tab (right or bottom) is hidden. Negative values allow you to use the secondary tab as if it was the primary tab.

```c
const tm_tt_id_t layout_id = tm_the_truth_api->create_object_of_hash(tt, TM_TT_TYPE_HASH__WINDOW_LAYOUT, TM_TT_NO_UNDO_SCOPE);
tm_the_truth_object_o *layout_w = tm_the_truth_api->write(tt, layout_id);

tm_the_truth_object_o *layouts_w = tm_the_truth_api->write(tt, window_layouts_id);
tm_the_truth_api->add_to_subobject_set(tt, layouts_w, TM_TT_PROP__WINDOW_LAYOUTS__LAYOUTS, &layout_w, 1);
tm_the_truth_api->commit(tt, layouts_w, TM_TT_NO_UNDO_SCOPE);

tm_the_truth_api->set_string(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__NAME, TM_LAYOUT_NAME);
tm_the_truth_api->set_uint32_t(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__ICON, TM_UI_ICON__COLOR_WAND);
tm_the_truth_api->set_float(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__WINDOW_X, 0.0f);
tm_the_truth_api->set_float(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__WINDOW_Y, 0.0f);
tm_the_truth_api->set_float(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__WINDOW_WIDTH, 1920.0f);
tm_the_truth_api->set_float(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__WINDOW_HEIGHT, 1080.0f);

const tm_tt_id_t tabwell_id = tm_tab_layout_api->save_layout(tt, &layout, false, TM_TT_NO_UNDO_SCOPE);
tm_the_truth_api->set_subobject_id(tt, layout_w, TM_TT_PROP__WINDOW_LAYOUT__TABWELL, tabwell_id, TM_TT_NO_UNDO_SCOPE);

tm_the_truth_api->commit(tt, layout_w, TM_TT_NO_UNDO_SCOPE);
TM_SHUTDOWN_TEMP_ALLOCATOR(ta);
```

Finally we can store our layout in the application settings. The top level object for this is the window layout. This specified the default position and size of the window if the user decides the instantiate the layout in a new window rather than as a workspace. 


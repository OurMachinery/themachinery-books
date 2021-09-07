# Interface Customizations

In this guide, you will learn about how to customize the Engine's interface.

- Change a theme
- Export/Import a theme
- Change the window scale.
- Add layouts.
- Modify the Global Grid settings.

## Change Theme

Sometimes we do not like the default theme or, based on reasons such as color blindness, and we cannot use the default theme. In the Machinery, you can change the default theme via **Window -> Theme**. You will find a list of themes the user can select and use.

![](https://www.dropbox.com/s/yt180qozhyrw2zc/tm_guide_theme_picker.png?dl=1)

The Engine comes by default with some base themes you can build your themes on top of:

| Theme               |
| ------------------- |
| Dark                |
| Light               |
| High Contrast Dark  |
| High Contrast Light |

## Custom Theme

If you like to customize the default themes or create a new theme, click on the "**New Theme"** menu in the same menu as the theme selection. After clicking this, the current Theme will be used as your base, and the Theme Editor Tab opens.

![](https://www.dropbox.com/s/imcy0y9wgxh252k/tm_guide_theme_create.png?dl=1)

If you do not like the base, you can choose a different theme as a base.

![change base of theme](https://www.dropbox.com/s/o7evmfhx8xn3gfn/tm_guide_theme_change_base.png?dl=1)

All changes are applied and saved directly. All changes will be immediately visible since your new Theme is selected as your current Theme.

![changes are directly visible](https://www.dropbox.com/s/z6sseczp8ccyhui/tm_guide_theme_changes_visible.png?dl=1)

## Export / Import a theme

You can export a custom theme from the **Window -> Theme** and later import it there as well. The Theme will be saved as a `.tm_theme` file. These files are simple `json` like files.



## Change the Scale of the UI

In the **Window** menu, you have a menu point **Zoom**. 

![zom option](https://www.dropbox.com/s/mvdzunm81gj4qj4/tm_guide_window_zoom.png?dl=1)

This allows you to zoom in or out. You can also use the key bindings:

| Meaning  | Keys                             |
| -------- | -------------------------------- |
| Zoom In  | CTRL + Equal, CTRL + Num + Plus  |
| Zoom Out | CTRL + Minus, CTRL + Num + Minus |



## Custom Layout

In case you do not like your current layout, you can always restore the default layout by using the **Window -> Restore Default Layout** menu point. 

![restore default layout](https://www.dropbox.com/s/coy73d8esv1jdew/tm_guide_window_restore_layout.png?dl=1)

If you want to store your current layout, it would be very useful for the later time you can save your current window layout.

![save current layout](https://www.dropbox.com/s/3vfmrnstcrf35gy/tm_guide_window_save_layout.png?dl=1)

You can create a new window or workspace with a layout in case you need it.

![](https://www.dropbox.com/s/dxy29xlb31xsbv9/tm_guide_create_window_with_layout.png?dl=1)

> **Note:** The Engine should restore the last used layout when it shutdown.

If you need to change some details of your Window layout you can do this via the Edit layout menu. 

![edit layout](https://www.dropbox.com/s/bbc8ke0bqgp7vkh/tm_guide_window_edit.png?dl=1)

This will open the settings of the current Layout:

![](https://www.dropbox.com/s/1qt0q6ho4k3jn4d/tm_guide_window_edit_layout.png?dl=1)



## World Grid

In case you need to adjust the World Grid, you can do this at two places:

1. Via the Application Settings

![](https://www.dropbox.com/s/61rdistx6vuxaow/tm_guide_change_grid_settings.png?dl=1)

2. Via any Scene or Preview Tab Application Menu entry.

![](https://www.dropbox.com/s/doenzd3d3gniq0u/tm_guide_change_grid_scene_tab.png?dl=1)

Changes made there will only be applied to the specific tab.


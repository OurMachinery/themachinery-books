# Asset Browser

The **Asset Browser** shows all your project's assets and enables you to manage them. It has multiple views at your exposal, which can make managing assets easier. The asset browser also allows you to search for assets in the current folder.

![The asset browser’s grid view](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625429028821_image.png)

As the image shows, the asset browser contains two components: The Directory Tree View of your project and the actual Asset View Panel.

**Table of Content**

* auto-gen TOC;
{:toc}


## Structure

**The Directory Tree View** reflects all directories and subdirectories of your project. You can use it to navigate quickly through your project. The navigation works either via mouse or via keyboard. You have the same management functionality as in the Asset View Panel:


- Add a new folder or assets to a folder
- Rename, Delete, Copy, Cut, Paste, Duplicate folder
- Drag Drop folder and reorganize the folder structure
- Show in explorer if the current project is a directory project
- Copy the path if the current project is a directory
- Change Views: Change to Grid, Details or List view
- Change the Filter & Sorting

All of those actions can be either done via the Main Menu or via the context menu.

**The Asset View Panel** reflects all directories and sub directories as well as their assets in your project. This is the main place to organize your assets and folders. You have the same management functionality as in the Directory Tree View.

The Asset View Panel comes in three different views: **Grid (default),** **Detail, and List-View.**  You can change the views via the context menu or the *Change View* button next to the search field. Besides, there are also shortcuts to change the views: **Shift + C** will switch to the Grid View, **Shift + L** will change to the List view, and **Shift + D** will change to the details view. 

![Detail View](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625429106698_image.png)

**Different View Modes**

**The Grid View** will display your assets in a grid, which will shrink or grow depending on the tab size. In **Details View** allows you to see the details of your assets: What type are they easily? How big are they, and where on the disc are they located (if it's a directory project). The **List-View** will display your project's content in a list form.

**About filtering, sorting, and changing the view**
There you have the option to filter via file extension or Asset-Labels. You can filter all assets by file extension type / Asset-Labels via the little filter icon or the context menu. You can also mix and match, as you require.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625429197285_image.png)
![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625429212614_image.png)


You can sort them via the context menu or the sort arrow up/down buttons (▲▼). Besides, there are also shortcuts to change the views: **Shift + N** will sort by Name **Shift + S** sort by Size, and **Shift + T** sort by type. The sorting will be applied in all view modes.

## Search

You can search in your project, and the default search is local. If you want to search globally, you want to click on the button with the Globe. This search will search for you in the entire project. Be aware your filters will influence your search!

![Switch from local to global view](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625430508007_image.png)


When searching globally, you can right-click on any search result and open the location of the selected asset.

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625430660296_image.png)

## Asset management

*Editing specific assets*
Double clicks on an asset may open the asset in their corresponding tab or window. Not all assets have a specific action associated with them. 

| Asset                          | Action on double click                                       |
| ------------------------------ | ------------------------------------------------------------ |
| Animation State Machine (.asm) | Opens a new window with the Animation state machine layout.  |
| Creation (.creation)           | Opens a graph tab if no graph tab is open. If a graph tab is open it will load this graph. When ever we have a **.creation** file than the graph is called Creation Graph and is used for working on graphics related workflows such as materials. |
| Entity (.entity)               | Opens a s**cene tab** if no scene tab is open. If a scene tab is open it will change the view to this entity. |
| Entity Graph (.entity_graph)   | Opens a graph tab if no graph tab is open. If a graph tab is open it will load this graph. When ever we have a **.entity_graph** file than the graph is called Entity Graph and is used to make Entity Graph functionality reusable and shareable between multiple graphs. |

A single click will always focus a associated Properties Tab on the selected asset.

*Dragging assets into the Scene*

You can drag assets around in the asset browser. It allows for quick reorganization of assets. It is also possible to drag assets from the asset browser directly into the Scene. Assets can be dragged from the Asset Browser Tab to other tabs if they support the asset type.
You can also drag assets from the Windows-Explorer into your project. This action supports the same formats as the regular importer via **File → Import Assets.** 

*Asset Labelling*

To organize your project, you can use Asset Labels. An asset can be associated with one or more different asset labels. You can use them to filter your asset in the asset browser or plugins via the [asset label api](https://ourmachinery.com//apidoc/plugins/editor_views/asset_label.h.html#structtm_asset_label_api).

There are two types of Asset labels: 

- System Asset Labels: They are added by plugins and cannot be assigned by the user to a asset.
  - User Asset Labels: You add them, and they are part of the project with the file extension: .asset_label and can be found in the asset_label directory.

The user can manage them like any other asset and delete user-defined Asset Labels via the asset browser. There you can also rename them, and this will automatically propagate to all users of those asset labels.

*Add an Asset Label to as Asset* 

You can add asset Labels via the property view to any asset:

- You select an Asset.
- You expand the Label View in the Property View Tab.
- You can type in any asset label name you want. The system will suggest already existing labels or allow you to create the new one.


![1. Asset Label View in the Asset Property View Tab 2. The home of all your asset labels.](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625429529838_image.png)


## Keyboard bindings

| Key              | Descriptions                                                 |
| ---------------- | ------------------------------------------------------------ |
| Arrow Keys       | Allow you to navigate through the Asset browser              |
| Enter            | If selected a folder or a asset will open the folder or asset |
| F2               | Will rename asset or folder in Asset View Panel and Directory Tree View |
| Ctrl + F         | Search in the current project                                |
| CTRL + D         | Duplicates selected Asset                                    |
| CTRL + C         | Copies Assets                                                |
| CTRL + V         | Pastes Assets                                                |
| CTRL + X         | Cuts Assets                                                  |
| Ctrl + Alt + O   | Opens Location of the asset in the asset browser view if in search view. |
| Ctrl + Shift + N | New folder                                                   |
| Ctrl + Shift + E | Open in Explorer                                             |
| Shift + D        | Change to Details View                                       |
| Shift + L        | Change to List View                                          |
| Shift + C        | Change to Grid View                                          |
| Shift + N        | Sort by Name                                                 |
| Shift + S        | Sort by Size                                                 |
| Shift + T        | Sort by File Extension                                       |
| Shift + O        | Opens a Directory or Asset                                   |


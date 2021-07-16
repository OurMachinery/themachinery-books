# Properties Tab 

The **Properties** tab shows the properties of the currently selected object. You can modify the properties by editing them in the properties window. 

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428761738_image.png)

### Use mathematical expression

We’ve also have support for mathematical expression to our property editor. So you can now type both numerical values and expressions.

You can use `x` in the expression to mean whatever value the property had before, so if you type `x + 1` you will increase the current value by 1.


![Using expressions in the property editor.](https://paper-attachments.dropbox.com/s_AF44CABDD4BF19FA7D54C2D4574B155CAAE2ED895AFB490AC3671972A5F81DC2_1617121646846_expressions.gif)

### Multiple tabs with different properties

You can have multiple tabs of different properties open if you wish. In this case, it comes very handily that you can pin Properties Tabs to a specific Object. 
Otherwise, the property tab will reflect the next selected object, and you would have multiple times the same thing open. 
You can pin content by clicking the *Pin* icon on Properties Tab. It will bind the current object to this instance. 

![Pin the properties tab for the prop floor barrel (module dungeon kit example)](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428863969_image.png)


Moreover, if you dock a *Preview* tab in the same window as an *Asset Browser*, it will show a preview of the selected asset in that browser.

**About Prototypes**

The Machinery has a prototype system that allows entity assets to be used within each other. Therefore you can create an Entity-Asset that represents a room and then create a house Entity with a bunch of these room entities placed within. 
We call the room asset a *prototype*, and we call each placed room entity an *instance* of this prototype. 

Any Entity-Asset can be a prototype, with instances of it placed in another entity asset. Note that prototypes are not special assets. More about this [here.]({{base_url}}/the_machinery_book/editing_workflows/prototypes.html)

![](https://paper-attachments.dropbox.com/s_688CFE67758A45D845E788E6DA05448A2BCF730C2B07FEF2D06AB18D2C46F736_1625428959141_image.png)


The overridden entities and components are drawn in blue. We change the x and z components of the position to move the box. Note how the changed values are shown in white, while the values inherited from the prototype are shown in grey. 

Missing

- link somehow somewhere the prototype content

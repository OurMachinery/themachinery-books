# Debugger

The Entity Graph has a Debugger. You can use this Debugger to inspect the current values or set a breakpoint to see if the Graph behaves the way it should. Besides the graph indicated if a node is executed by a highlighted border!

> **Note:**  The Debugger only works if the simulate tab and the graph tab are open at the same time!

![](https://www.dropbox.com/s/80ld50b4n6ohjio/tm_guide_entity_graph_debugger_basic.png?dl=1)

You can find the Debugger when you click on the button in the upper toolbar with the bug symbol **(1)**. It will open the Debugger Overlay. Besides the "Bug" button, you can find a dropdown menu **(2)**. This dropdown menu lets you switch between Graph instances quickly. This is useful if the Graph is part of an Entity Prototype or itself a Subgraph prototype! 



## Debug Overlay

![](https://www.dropbox.com/s/wly93rk8vz97upm/tm_guide_entity_graph_debug_overlay.png?dl=1)

In this overlay, you find three-tab:

1. **Watch Wires;** Contains all data wires you are watching.
2. **Breakpoints;** This Contains a list of all Breakpoints within this Graph and its subgraph
3. **Instances;** A list of all instances of this Graph



## Watch Wires

Like in a normal code editor, you can hover over any data wire and observe the values during the execution. If a value changed, it would be red, otherwise white.

![](https://www.dropbox.com/s/cw86wtsfcb8sg50/tm_guide_entity_graph_watch_wires.png?dl=1)

This might be cucumber some and difficult for observing multiple wires. This is why you can add them to the watch wire list.

![](https://www.dropbox.com/s/1j09t2vxxk4t11b/tm_guide_entity_graph_add_watch_wires.png?dl=1)

The Watch Wire list will indicate as well if a value has changed. You can also remove them there again and find the node with the find node button.

![](https://www.dropbox.com/s/lpx1duqf5lpee0n/tm_guide_entity_graph_watch_wires_overlay.png?dl=1)

Keep in mind that this list only works within the current graph instance and its subgraph.



## Breakpoints

Unlike watching wires which require no extra step, you cannot just add a breakpoint, and it will break immediately since such behaviour could be annoying. You can add breakpoints at any point in time via **Right-Click on a node** -> **Add Breakpoint.** 

> **Note:** You can only add breakpoints to all nodes besides Event and Query nodes.

![](https://www.dropbox.com/s/us6lrw5ad9qpcbg/tm_guide_entity_graph_add_breakpoints.png?dl=1)

To activate the breakpoints, you need to connect to the Simulation by pressing the Connect Button in the Debug Overlay.

![](https://www.dropbox.com/s/34jbcvkt49814kk/tm_guide_entity_graph_connect.png?dl=1)

(*Alternatively, the Breakpoint Overview will inform you that you need to connect to the Simulation)*

The moment you are connected, the Simulation will react appropriately, and your breakpoints will happen.

![](https://www.dropbox.com/s/26awwgjzz93mcu4/tm_guide_entity_graph_debug_mode.png?dl=1)

1. You can disconnect from the Simulation.
2. You can continue till the next breakpoint hits.
3. You can Stepover to the next node.

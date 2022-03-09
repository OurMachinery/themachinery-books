## Simulation

In *The Machinery*, we make a distinction between *simulating* and *editing*. When you are *editing*,
you see a static view of the scene. All the runtime behaviors like physics, animation, destruction,
entity spawning, etc are disabled. (Editing the scene with everything moving around would be very
tricky.)

In contrast, when you are *simulating* or *running*, all the dynamic behaviors are enabled. This
allows you to see the runtime behavior of your entities. If you are building a game, the simulation
mode would correspond to running the game.

To *simulate* a scene, open a scene in the *Simulate* tab.

![Simulate tab.](https://www.dropbox.com/s/7t8elpzqllqkqrb/simulate-tab.png?dl=1)

You can use the controls in the tab to pause, play, or restart the simulation or change the
simulation speed. Note that if you haven't added any simulation components to the scene, the
*Simulate* tab will be just as static as the Scene tab. In order to get something to happen, you
need to add some runtime components.

The *Entity Graph* gives you a visual scripting language for controlling entity behavior. It will
be described in the next section.

You can launch the engine in simulation mode from the command line:

```
the-machinery.exe --load-project project.the_machinery --simulate scene
```

Here `project.the_machinery` should be the name of your project file and `scene` the name of the
entity you want to simulate. This will open a window with just the *Simulate* tab, simulating the
scene that you specified.

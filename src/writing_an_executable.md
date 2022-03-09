## Writing an executable

Writing a stand-alone executable is similar to writing a plugin except that you need to write
initialization code for booting up all the systems that you want to use as well as the main loop
code that runs the executable.

`bin/simple-draw.exe` is a sample executable that uses the UI / Draw2D interfaces of The Machinery
to implement a simple drawing program:

![Simple Draw executable.](https://www.dropbox.com/s/bilirde9yud4rn3/simple-draw.png?dl=1)

The source code of this sample program is available in the `samples` directory. By playing with
and modifying this, you can see how to build your own applications on top of *The Machinery*.

Note that just as when writing plugins, you need a Visual Studio installation (2019) to build an
executable. You need to set `TM_SDK_DIR` to the location of The Machinery SDK you are using, and you
use `tmbuild.exe` to build the executable.

`bin/simple-3d.exe` is a sample executable that uses the full 3D API.

![Simple 3D executable.](https://www.dropbox.com/s/oz9zob150yksnhr/simple-3d.png?dl=1)

You will find the source code for this too in the samples directory.
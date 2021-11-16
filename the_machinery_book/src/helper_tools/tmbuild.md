# How to use tmbuild

We described `tmbuild`'s core idea in our blog-post [*One-button source code builds*](https://ourmachinery.com/post/one-button-source-code-builds/). `tmbuild` is our custom one-click "build system." and it is quite a powerful tool. It allows you to do the most important tasks when developing with The Machinery: Building your plugin or the whole engine.

You can execute the tool from any terminal such as PowerShell or the VS Code internal Console window.

The key features are:

- building
- packaging
- cleaning the solution/folder
- downloading all the dependencies
- running our unit tests

This walkthrough introduces you to `tmbuild` and shows you how to use and manipulate The Machinery Projects. You will learn about:


- How to build with it
- How to build a specific project with it
- How to package your project

Also, you will learn some more advanced topics such as:

- How to build/manipulate tmbuild

**Table of Content**

* auto-gen TOC;
{:toc}



## **Installing tmbuild**

When you download and unzip [The Machinery](https://ourmachinery.com/) either via the [website](https://ourmachinery.com/beta.html) or via the [download tab](#) you can find tmbuild in the bin folder in the root. 

> Alternatively, you can build it from source `code\utils.` We will talk about this later in this walkthrough. 

Before we use tmbuild, we need to ensure that we have installed either *build-essentials* under Linux, *XCode* on Mac, or *Visual Studio 2017 or 2019* (Either the Editor such as the Community Edition or the Build Tools). 

**Windows Side nodes:**

On Windows, it is essential to install the C/C++ Build tools. 
If you run into the issue that tmbuild cannot find Visual Studios 2019 on Windows, it could be because you installed it on a typical path.  No problem, you can just set the environment variable `TM_VS2017_DIR` or `TM_VS2019_DIR` to the root `C:\Program Files (x86)\Microsoft Visual Studio\2019`. The tool will find the right installed version automagically.



## **Set up our environment variables**

Before we can build any project, we need to set up our environment. You need to set the following environment variable: 
(If this one has not been set the tool will not be able to build)

- `TM_SDK_DIR` - This is the path to find the folder `headers` and the folder `lib`

If the following variable is not set, the tool will assume that you intend to use the current working directory:

- `TM_LIB_DIR` - The folder which determines where to download and install all dependencies (besides the build environments)



**How to add environment variables?**

**Windows**

On Windows all you need to do is you need to add the folder where you installed The Machinery to your environment variables. You can do this like this:
**Start > Edit the system environment variables > environment variables > system variables > click New... >** add `TM_SDK_DIR` or `TM_LIB_DIR` as the Variable Name and the needed path as the Variable Value.
Close and restart the terminal or Visual Studio / Visual Studio Code.
As an alternative, you can set an environment variable via PowerShell before you execute tmbuild, which will stay alive till the end of the session:
`$Env:TM_SDK_DIR="..PATH"`



**Debian/Ubuntu Linux**

You open the terminal or edit with your favorite text editor `~/.bashrc` and you add the following lines:

    #...
    export TM_SDK_DIR=path/to/themachinery/
    export TM_LIB_DIR=path/to/themachinery/libs

(e.g. via nano nano `~/.bashrc`)



## **Let us Build a plugin**.

All you need to do is: navigate to the **root folder** of your plugin and run in PowerShell `tmbuild.exe`. 

> If you have not added tmbuild.exe to your global PATH, you need to have the right path to where tmbuild is located. `user@machine/home/user/tm/plugins/my_plugin/> ./../../bin/tmbuild`



This command does all the magic. tmbuild will automatically download all the needed dependencies etc., for you *(Either in the location set in `TM_LIB_DIR` or in the current working directory)*. 
You may have noticed tmbuild will always run unit tests at the end of your build process.



>  **Note:** tmbuild will only build something when there is a premake5.lua and a libs.json in the current *working directory*.




## **Let us build a specific project**.

Imagine you have been busy and written a bunch of plugins, and they are all connected and managed via the same Lua file (premake5 file). 
Now you do not want to check everything all the time. No problem, you can follow these steps:
If you run `tmbuild --help/-h`, you will see many options. One of those options is `--project`. This one allows you to build a specific project.


    tmbuild.exe --project my-project-name

The tool will automatically find the right project and build it. 
On Windows, you can also provide the relative/absolute path to the project with extension: ``

    tmbuild --project /path/to/project.vcxproj



> **Note:**
> If a project cannot be found it will build all projects.




## How how to package a project via tmbuild?

To package a project via tmbuild, all you need to do is use the `-p [package name]` or `--package [package name]` command. A package file needs to be of type `.json` and follow our package scheme, which you can find [here](#).




## How to build or manipulate tmbuild from source

You can find the source code of tmbuild in the folder `code\utils\tmbuild`. In the folder `code\utils`, you can also find the source code of all the other uses the engine uses.

You can build tmbuild via tmbuild. All you need to do is navigate the `code\utils` folder and run `tmbuild --project tmbuild`. 

If you do not have access to a build version of tmbuild but to the whole source, you have to follow the following steps:

**Windows 10**

Make sure you have Visual Studio 19 and the Build Tools installed. Besides, check if you can find `msbuild` in the terminal. You can install `msbuild / vs studio` via PowerShell: [https://github.com/Microsoft/vssetup.powershell](https://github.com/Microsoft/vssetup.powershell)

To check just run:

```bash
msbuild
```


if you cannot find it just add it to your environment path variables: with e.g.
`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\`

**To build from source:**

Open a PowerShell instance in The Machinery folder and run the following commands:

```powershell
# this part can be skipped if you have already downloaded
# all the dependencies and created a highlevel folder to your lib dependencies:
mkdir lib
cd lib
 wget https://ourmachinery.com/lib/bearssl-0.6-r1-win64.zip -OutFile bearssl-0.6-r1-win64.zip
 wget https://ourmachinery.com/lib/premake-5.0.0-alpha14-windows.zip -OutFile premake-5.0.0-alpha14-windows.zip
Expand-Archive -LiteralPath './bearssl-0.6-r1-win64.zip' -DestinationPath "."
Expand-Archive -LiteralPath './premake-5.0.0-alpha14-windows.zip' -DestinationPath "."
cd ..
# continue here if the dependencies are already downloaded
# set TM_LIB_DIR if you have not set it already
$env:TM_LIB_DIR="/path/to/themachinery/lib"
$env:TM_SDK_DIR="/path/to/themachinery/"
# run premake
./../../lib/premake-5.0.0-alpha14-windows/premake5 [vs2019|vs2017]
# navigate to the highlevel folder of the code (here you find the libs.json and the
# premake5.lua
cd code/utils
msbuild.exe "build/tmbuild/tmbuild.vcxproj" /p:Configuration="Debug Win64" /p:Platform=x64
```

*Make sure that you either choose vs2019 or vs2017 not* [vs2019|vs2017]

**On Debian/Ubuntu**

Open a terminal instance and run the following commands:

```bash
# If you do not have the huild essentials installed make sure you do:
sudo apt install build-essential clang zip -y
# otherweise continue here:
cd your-folder-of-tm
# this part can be skiped if you have already downloaded
# all the dependencies and created a highlevel folder to your lib dependencies:
mkdir lib
cd ./lib
wget https://ourmachinery.com/lib/bearssl-0.6-r1-linux.zip
wget https://ourmachinery.com/lib/premake-5.0.0-alpha15-linux.zip
unzuip bearssl-0.6-r1-linux.zip .
unzip premake-5.0.0-alpha15-linux.zip .
chmod +x ./premake-5.0.0-alpha15-linux/premake5
cd ..
# continue here if the dependencies are already downloaded
# set TM_LIB_DIR if you have not set it already
export TM_LIB_DIR=/path/to/themachinery/lib
export TM_SDK_DIR=/path/to/themachinery/
# run premake
./../../lib/premake-5.0.0-alpha15-linux/premake5 gmake
# navigate to the highlevel folder of the code (here you find the libs.json and the
# premake5.lua
cd code/utils
# run make:
make tmbuild
```



## How to add tmbuild globally accessible?

**Windows**
On Windows, all you need to do is you need to add the folder/bin to your environment variables. This can be done like this:
**Start > Edit the system environment variables > environment variables > system variables > search in the list for path > click Edit > click new >** add the absolute path to `themachinery/bin` in there
re-login or reboot.

**Debian/Ubuntu Linux**
You open the terminal or edit with your favorite text editor `~/.bashrc`, and you add the following lines:
`export PATH=path/to/themachinery/bin:$PATH`
(e.g. via nano nano `~/.bashrc`)


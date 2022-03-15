# Troubleshooting

This section addresses common problems that can arise when using The Machinery. 


## System Requirements

### Windows
| Name                     | Requirement                                       |
| ------------------------ | ------------------------------------------------- |
| Operating System Version | 10, 11                                            |
| GPU                      | A Vulkan 1.2 capable GPU with the latest drivers. |

### Linux

| Name             | Requirement                                                  |
| ---------------- | ------------------------------------------------------------ |
| Operating System | 64-bit Linux machine running Ubuntu 20.04 or a recent ArchLinux. |
| GPU              | A Vulkan 1.2 capable GPU with the latest drivers.            |
| Packages         | `sudo apt-get install libxcb-ewmh2 libxcb-cursor0 libxcb-xrm0 unzip` |

> **Note:** Other Linux distributions have not been extensively tested, but you are welcome to try.


## A Crash happened

Did The Machinery Crash? There are a few first troubleshooting steps:

1. Is your System (Window or Linux) up-to-date?
2. Do you have the latest Graphics Driver installed?
3. Does your system support `vulkan 1.2`?
4. Does your system fulfill our system requirements?
4. Did someone else have this issue before? Check on [Discord](https://discord.com/invite/SHHSZaH) or [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues)

In case you cannot debug the crash yourself you should create a issue on our Issue Tracker: [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). To obtain the logs or crash dumps follow the next steps:

### Windows 10 & Windows 11 Editor

When it comes to crashes on Windows which you cannot debug yourself, you can enable a full crash dumb via the file `utils/enable-full-dumps.reg` that we ships as part of the engine. After enabling full dumps, you can be find them in `%AppData%\..\Local\The Machinery` and then in the  `CrashDumps` folder. In case of an error report it can be very helpful to provide access to the crash dump. You can submit bugs on our public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). Please do not forget to mention your current Engine version.

In order to obtain log files you have to go to the same folder where you can find the CrashDumps (`%AppData%\..\Local\The Machinery`) but they will instead be in the `Logs` subfolder.

### Linux

When it comes to crashes on Linux which you cannot debug yourself. The dumps can be found in the folder `/home/YOU_USER/.the_machinery` and then in the  `CrashDumps` folder. In case of an error report it can be very helpful to provide access to the crash dump. You can submit bugs on our public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). Please do not forget to mention your current Engine version.

In order to obtain log files you have to go to the same folder where you can find the Crash Dumps (`/home/YOU_USER/.the_machinery`) but they will instead be in the `Logs` subfolder.

### Graphics

If the crash happens on the GPU or in graphics related code, then the crash error message will say so. The first step in a Vulkan related crash is to update your graphics drivers. If this doesn't help then please report the issue to us with the following information:

- The error message you got when the crash happened, this should include file information and a Vulkan error code, it's vital to share these.
- The log file, see the previous section on how to obtain this.
- A crash dump file, see the previous section on how to obtain this.

You can submit bugs on our public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). Please do not forget to mention your current Engine version and provide a copy of your logs.


## tmbuild cannot find build tools

On Windows, make sure you have Visual Studio installed. If you do, but you did some sor of non-typical installation, setup some environment variable before running tmbuild: `TM_VS2017_DIR` or `TM_VS2019_DIR`. They need to point to the root directory of your Visual Studio installation.


## tmbuild cannot find environment variables

Before we can build any project, you need to set the following environment variable:

- `TM_SDK_DIR` - This should point to your The Machinery root folder, i.e. where the `headers` lives.

If the following variable is optional:

- `TM_LIB_DIR` - This is where libraries we depen upon are downloaded and extracted. If not set, then libraries will be downloaded to the `lib` subfolder of `TM_SDK_DIR`.

You can also refer to this guide on [tmbuild]({{base_url}}/build_tools/tmbuild.html).


## clang-format pollutes my git commits

When you do commits to the git repository, we automatically run `clang-format` as a git commit hook, it is an application that does some auto-formatting of the code. It only changes files that already have changes. However, you really need to make sure you have the correct version of `clang-format` installed, as different versions format differently, having the wrong version can result in changes to code you never touched (although, it will as mentioned only touch file you already touched). Therefore, we provide it as a library (put alongside the other libraries `tmbuild` downloads). Visual Studio comes with its own version, so make sure to go into the settings of Visual Studio and point it to our version. To make command-line git find it you may want to add it to your `PATH` environment variable.


## Where to report bugs or feedback

1. If you have any problems running the software, encounter bugs or crashes, etc, then please report them on our [public bug tracker](https://github.com/OurMachinery/themachinery-public/issues). We will fix bugs as soon as we can and provide updated executables for download on the website. If you have a source code license and fixed something yourself, we'd gladly review and accept Pull Requests.
2. If you have other feedback or questions, post them on our [forum](https://github.com/OurMachinery/themachinery-public/discussions). We appreciate candid, honest opinions.

Note that you need to create a separate login to log in to the forum (we might unify the logins in the future).
You can also join our [Discord Server](https://discord.gg/SHHSZaH). You will frequently find us there, answering questions.


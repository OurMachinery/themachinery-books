# Troubleshooting

This section addresses common problems that can arise when using The Machinery. 


## Windows 10 Editor

When it comes to crashes on Windows which you cannot debug yourself. You can enable a full crash dumb via the following file `utils/enable-full-dumps.reg`. The dumps can be found in the folder `AppData\Local\The Machinery` and then in the  `CrashDumps` folder. In case of an error report it can be very helpful to provide access to the crash dump. You can submit bugs on our public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). Please do not forget to mention your current Engine version.

In order to obtain log files you have to go to the same folder where you can find the CrashDumps (`AppData\Local\The Machinery`) but they till instead be in the `Logs` subfolder.



## Windows 11

We have not tested windows 11 yet therefore possible problems are to be expected. Please report them to us on the public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues) so we can keep track of them.




## tmbuild cannot find build tools

In case of a non typical installation of Visual Studios you have to provide to tmbuild the correct environment variables: `TM_VS2017_DIR` or `TM_VS2019_DIR`. They need to point to the root directory of your Visual Studio installation.



## tmbuild cannot find environment variables

Before we can build any project, we need to set up our environment. You need to set the following environment variable: (If this one has not been set the tool will not be able to build)

- `TM_SDK_DIR` - This is the path to find the folder `headers` and the folder `lib`

If the following variable is not set, the tool will assume that you intend to use the current working directory:

- `TM_LIB_DIR` - The folder which determines where to download and install all dependencies (besides the build environments)

Make sure you have added the needed environment variables. Follow this guide on [tmbuild]({{the_machinery_book}}/helper_tools/tmbuild.html).



## clang-format pollutes my git commits

Make sure that you are using the `clang-format` version the engine downloads for you and add to the `TM_LIB_DIR`. The engine uses the version 6.0. In case you are using visual studio or visual studio code make sure it points to the right executable!




## Graphics

In case of a crash you will get an error message, this will give some information about the details of the crash. The first step in a Vulkan related crash is to update your graphics drivers. If this didn’t help then please report the issue to us with the following information.

- The error message you got when the crash happened, this should include file information and a Vulkan error code, it’s vital to share these.
- The log file, see the previous section on how to obtain this.
- A crash dump file, see the previous section on how to obtain this.

You can submit bugs on our public [GitHub issues page](https://github.com/OurMachinery/themachinery-public/issues). Please do not forget to mention your current Engine version.




## Where to report bugs or feedback


1. If you have any problems running the software, encounter crashes, etc, report them on our [public bug tracker](https://github.com/OurMachinery/themachinery-public/issues) as soon as possible. We will fix bugs as soon as we can and provide updated executables for download on the website.
2. If you have other feedback or questions, post them on our [forum](https://github.com/OurMachinery/themachinery-public/discussions). We appreciate candid, honest opinions.

Note that you need to create a separate login to log in to the forum. (We might unify the logins in the future.)
You can also drop in on our [Discord Server](https://discord.gg/SHHSZaH). You will frequently find us there, answering questions. We'll pay special attention on Thursdays.


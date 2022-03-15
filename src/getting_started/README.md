# Getting started

To run The Machinery you need:

- A 64-bit Windows 10 machine with the latest Vulkan drivers
- **Or** a 64-bit Ubuntu 20.04 Linux machine with the latest Vulkan drivers (ArchLinux should also work, no guarantees are made for other distros)
- **And** an [ourmachinery.com](https://ourmachinery.com/) account. [Sign up here!](https://ourmachinery.com/sign-up.html)

On Linux, you also need to install the following packages for the runtime:

~~~bash
sudo apt-get install libxcb-ewmh2 libxcb-cursor0 libxcb-xrm0 unzip
~~~

*This does not work on your distro*? No problem, visit our [Linux installation process across distributions guide](https://github.com/OurMachinery/themachinery-public/discussions/616).

## Getting up and running

Quick steps to get up and running:

1. Download The Machinery at [https://ourmachinery.com/download.html](https://ourmachinery.com/download.html).

2. Sign up for an [ourmachinery.com](https://ourmachinery.com/) account [here](https://ourmachinery.com/sign-up.html). (It's free!)

3. Unzip the downloaded zip file to a location of your choosing.

4. Run `bin/the-machinery.exe` in the downloaded folder to start The Machinery.

5. Login with your [ourmachinery.com](https://ourmachinery.com/) account at the login screen and approve the EULA.

6. To find some samples to play with go to **Help > Download Sample Projects** in the main menu.

7. Pick one of the sample projects (for example **Physics**), click **Get** and then **Open**.

8. Play around with it, try some other samples and read the rest of this document to find out what
   else you can do with The Machinery.

If you get errors that mention Vulkan or if you see weird rendering glitches, make sure to update
your GPU drivers to the latest version. If that doesn't work, post an issue with our [issue
tracker](https://github.com/OurMachinery/themachinery-public/issues) or ping us on [Discord](https://discord.gg/uJtkbVr) and we will help you.

Related videos to these topics are:

<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="788.54" height="443" type="text/html" src="https://www.youtube.com/embed/oQGghpCqBhI?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0&origin=http://ourmachinery.com"></iframe>

## Source Code access

You can make use of `tmbuild` (from the binary build) to download the engine (source code) and install all needed dependencies as well. This can be done via `tmbuild --install` in this case you may want to use `--github-token` as well and provide your token. Alternatively you can also manually clone the repo as you are used to from any other git repositories



### I signed up for source code but didn't get access.

Make sure your GitHub account is correctly entered on the [Profile](https://ourmachinery.com/profile.html) page. It should be your account name, not your email.

GitHub invites frequently end up in the Spam folder. Check there or go to the [repository](https://github.com/ourmachinery/themachinery) to see your invite.

If you still have problems despite this, then contact us on ping@ourmachinery.com.
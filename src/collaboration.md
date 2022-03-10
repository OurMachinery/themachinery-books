## Collaboration

The editor has built-in support for real-time collaboration, allowing multiple people to work
together in the same project. All user actions — importing assets, creating and editing entities,
etc, are supported in the collaborative workflow.

If you just want to try out collaboration on your own, you can run the client and the host on the
same machine (just start two instances of the_machinery.exe) and connect using the LAN option.

**Table of Content**

* {:toc}
## Who's project is edited?

In our collaboration model, one of the users always acts as a host. The host invites others to join her in editing *her* project. All the changes made by the participants in the session end up in the host’s project and it’s the host’s responsibility to save the project, check in the changes into version control, or do whatever else is needed to make the changes permanent.

> **WARNING:** Please only connect to people you trust. Be aware that Plugin Assets will be sent via a collaboration as well. The Engine will warn you every time a plugin asset is sent.

## Host or Join Sessions

You have three options to host or join a collaboration Session:

### Host a LAN Server

Host a server on your LAN. The system will choose a free port on your machine for hosting. Other users on the same LAN can join your session by choosing *Join LAN Server* and selecting your machine.

![Host locally](https://www.dropbox.com/s/0amm9km2jiejxx1/tm_guide_collab_host_local.png?dl=1)

1. Select "Host LAN Server" from the dropdown
2. Your Handle, in case of hosting this will be the name the session will have as well as your username.
3. When you press Host the session starts.

#### Join a local Server

When you open the collaboration tab the default view is the "Join LAN Server" view. In this view you can join a local server.

![The default view of the collab tab is the join local option](https://www.dropbox.com/s/1cx17p05swuu6mg/tm_guide_collab_join_local.png?dl=1)

1. Select "Join LAN Server" from the dropdown
2. You can select a collaboration session. If there is no session available this field is disabled.
3. Your Handle, the name the other user can see on their side.
4. If you selected a session you can press this button to join. When you join the Engine will download the host's Project.

### Host Internet Server

Host a server that can be accessed over the internet on a specified port.

![Host Internet Server](https://www.dropbox.com/s/q3q7ltunpqmepeq/tm_guide_collab_host_internet.png?dl=1)

1. You can select the port of your session. If your router does not support **UPnP** you might have to port forward your selected port.
2. Your Handle, the name the other user can see on their side.
3. If you check the "Use UPnP" checkbox the system will attempt to use UPnP to open the port in your router, so that external users can access your server.
4. If you selected a session you can press this button to join. When you join the Engine will download the host's Project.

> **Note**: There is no guarantee that UPnP works with your particular router. If Internet hosting is not working for you, you may have to manually forward the hosting port in your router.

#### Join an internet Server

To connect, an external user would choose *Join Internet Server* and specify your external IP address.

![Join a Internet Server](https://www.dropbox.com/s/n1fhqm7p3jr6yx8/tm_guide_collab_join_internet.png?dl=1)

1. You need the Online Host's IP Address. In the format: `89.89.89.89:1234`. 
2. Your Handle, the name the other user can see on their side.
3. It will try to connect to the other user.

> **WARNING:** Please only connect to people you trust. Be aware that Plugin Assets will be sent via a collaboration as well. The Engine will warn you every time a plugin asset is sent.



### Host a Discord based Session

The Machinery allows you to connect via Discord with your co-workers, team mates or friends. Important for this to work is that both parties: Host and Clients have the following option enabled in their Discord Options: **Discord Settings -> Activity Status**

![](https://media.discordapp.net/attachments/879451114355965973/879452121668407306/unknown.png)

> **Note:** Host and client cannot be invisible otherwise invites wont work!

After this setting is enabled you need to add The Machinery as a game so others can see you are playing it. This allows you now to invite your friends via the Engine into your session and vice versa.

![](https://www.dropbox.com/s/6e6lanbsz5etfkm/tm_guide_collab_discord_host.png?dl=1)

## Connected

When you are connected to a collaboration session you have this view. In the connected view you can chat with the other participants of the chat. The session will **not** terminate / disconnect if you close the tab.

![](https://www.dropbox.com/s/ehg9x2l8frvlo04/tm_guide_collab_connected.png?dl=1)

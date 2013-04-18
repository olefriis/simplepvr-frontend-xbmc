What?
=====
A plug-in for XBMC, so that you can enjoy your [SimplePVR](https://github.com/olefriis/simplepvr)
recordings in your existing media center.

Status
======
This plug-in is currently under development, so you have to check out this repository and follow
the developer guide below.

Usage
=====
After installing the plug-in, remember to look through the plug-in's settings page in XBMC.
Here, you set up the server URL and username / password, in case you have secured your server as
described above. If you run XBMC on the same machine as the back-end is running, check the
"Backend runs on this machine" option, in which case XBMC will use the local files directly
instead of streaming through HTTP.

The plug-in allows you to browse your recordings, watch them, and delete them. To delete, press
the "C" key, or right-click your mouse on a show or a recording. Then you can choose "Delete" from
the context menu.

To get information on a given recording, press the "I" key when a recording is selected.

Please note: XBMC currently has to run on the same machine as the SimplePVR backend. This may change
in the future, but currently the backend is not fast enough at streaming files through HTTP.

Development
===========
Generate a ZIP file containing the plug-in and install it through XBMC's settings page (the ZIP
file will be placed in the "output" folder) by running this in the plugins/xbmc folder:

        rake package

After installing the plug-in, you can edit it directly in the XBMC installation (on MacOS):

        /Users/<your_user_name>/Library/Application Support/XBMC/addons/plugins.video.simplepvr/

The XBMC debug log is placed here (on MacOS):

        /Users/<your_user_name>/Library/Logs/XBMC.log

TODO
====
The code currently STINKS! It's messy and not unit tested at all. I want to change that.

Also, using Rake for building the package probably isn't the Python way to do it...?
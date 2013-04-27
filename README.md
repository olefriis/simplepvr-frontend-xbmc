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
the context menu. The context menu isn't available by default on all remote controls - for my MCE
remote, I had to create the following file as ~/.xbmc/userdata/keymaps/keyboard.xml:

		<keymap>
		  <global>
		    <keyboard>
		      <key id="22">ContextMenu</key>
		    </keyboard>
		  </global>
		</keymap>

Then the context menu appears when I press the "ENTER" button on the remote. See
[here](http://forum.xbmc.org/showthread.php?tid=156950) for a little explanation.

To get information on a given recording, press the "I" key when a recording is selected.

Please note: XBMC currently has to run on the same machine as the SimplePVR backend. This may change
in the future, but currently the backend is not fast enough at streaming files through HTTP.

Development
===========
Before running the tests, you need to install pytest and simplejson:

        sudo easy_install -U pytest
        sudo easy_install simplejson

Generate a ZIP file containing the plug-in and install it through XBMC's settings page (the ZIP
file will be placed in the "output" folder) by running this in the plugins/xbmc folder:

        rake package

PLEASE NOTE: Before installing a newly generated ZIP file, be sure to clean XBMC's cache containing
your old ZIP file:

		rm -rf ~/Library/Application\ Support/XBMC/addons/packages/plugin.video.simplepvr*

(Boy, I spent a lot of time fooling around before finding this...)

After installing the plug-in, you can edit it directly in the XBMC installation (on MacOS):

        /Users/<your_user_name>/Library/Application Support/XBMC/addons/plugin.video.simplepvr/

The XBMC debug log is placed here (on MacOS):

        /Users/<your_user_name>/Library/Logs/xbmc.log

TODO
====
The code currently STINKS! It's messy and not unit tested at all. I want to change that.

Also, using Rake for building the package probably isn't the Python way to do it...?
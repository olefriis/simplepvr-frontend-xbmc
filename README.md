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

Then simply run the tests by issuing

        py.test

from the command-line.

Generate a ZIP file containing the plug-in and install it through XBMC's settings page (the ZIP
file will be placed in the "output" folder) by running this:

        rake package

PLEASE NOTE: Before installing a newly generated ZIP file, be sure to shut down XBMC and clean
XBMC's cache containing your old ZIP file (Boy, I spent a lot of time fooling around before finding
this...):

		rm ~/Library/Application\ Support/XBMC/addons/packages/plugin.video.simplepvr*

After installing the plug-in, you can edit it directly in the XBMC installation (on MacOS):

        ~/Library/Application Support/XBMC/addons/plugin.video.simplepvr/

The XBMC debug log is placed here (on MacOS):

        ~/Library/Logs/xbmc.log

Release
=======
Remember to bump version number in `addon.xml` file, `Rakefile`, and make sure that the information
in `changelog.txt` is correct.

I haven't released "for real" yet (so that people can just install the plug-in directly from XBMC),
so a description of that is missing for now.

TODO
====
I'm a Python and XBMC newbie, so probably I'm doing lots of things wrong. I'm trying to adhere to
[PEP 8](http://www.python.org/dev/peps/pep-0008/) and doing my best to create clean code, but
please let me know if I got something wrong Python- and XBMC-wise.

Using Rake for building the package probably isn't the Python way to do it...? It just seems like
Python has no default build tool...?

The code is missing some error handling:

* If "same machine" is checked, but the local file URL is not present, a nice, helpful error message
  would be nice.

Also, there seems to be a bug:

* If you have set up a wrong username and password, XBMC simply crashes. SimplePvrClient ought to
  handle it quite nicely (it's tested and all), and the XBMC log gives nothing.

Oh, and if you can paint a nicer SimplePVR logo, do go ahead :-)
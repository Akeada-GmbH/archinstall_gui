import json
import urllib.request
from os import walk
from os.path import isdir, isfile, abspath
from time import time

html = """
<div class="padded_content flex_grow flex column" style="min-width:100%;">
	<h3><b>WILLKOMMEN ZUR PRIVASTICK INSTALLATION</b></h3>
	
	<span>
    BITTE SEHEN SIE SICH DAS VIDEO AN, WELCHES ERKLÄRT, WIE DIE INSTALLATION ABLÄUFT UND WAS SIE VOR DER INSTALLATION BEACHTEN SOLLTEN.
	</span>

    <!--

	<ul>
		<li>The default <a target="_blank" href="https://wiki.archlinux.org/index.php/Kernel">Linux kernel</a> <i>(and firmware for common hardware)</i></li>
		<li>The <a target="_blank" href="https://www.archlinux.org/packages/core/any/base/">base</a> package.</li>
		<li>A bootloader called <a target="_blank" href="https://wiki.archlinux.org/index.php/systemd-boot">systemd-boot</a></li>
	</ul>


	<div class="warning">
		<div class="warningHeader"><div class="noteIcon"></div><span>Warning</span></div>
		<div class="noteBody">
			Arch Linux will not automatically connect to the internet or a network after you reboot into your installation, you must therefore read and understand the <a target="_blank" href="https://wiki.archlinux.org/index.php/Network_configuration">Network Configuration</a> article. A <a target="_blank" href="https://wiki.archlinux.org/index.php/Category:Network_managers">Network Manager</a> could help new users get going, but please <b>read both Wiki articles before asking questions</b>.
		</div>
	</div>

	<span>
	After which, all optional steps on the left hand side are configured and installed.
	</span>

	<ul>
		<li>Language and region settings</li>
		<li><a target="_blank" href="https://archinstaller.readthedocs.io/en/latest/profiles">Profiles</a> <i>(pre defined configurations for new users to try out different setups)</i></li>
		<li>Additional applications</li>
		<li>Personlised user and password</li>
		<li>AUR package support</li>
	</ul>

	<!--
	<div class="note">
		<div class="noteHeader"><div class="noteIcon"></div><span>Note</span></div>
		<div class="noteBody">
			The installer will not provide or set a <div class="inlineCode">root</div> password, after a successful boot, <a target="_blank" href="https://wiki.archlinux.org/index.php/installation_guide#Root_password">root password</a> must be set manually.
		</div>
	</div>
	-->

<!-- <video id="player" width="350" height="250" preload="none" controls>      <source id="video-src">   </video> -->

<div class='embed-container' style='padding-top:100px;max-height:40%; padding-top=100px;'>
  <iframe src='https://player.vimeo.com/video/574111364' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>
  </div>

    <div class="note">
        <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
        <div class="noteBody">
            <b>Folgende Daten sollten Sie für die Erstinstallation bereithalten</b>
            <ul>
            <li>WLAN Zugangsdaten</li>
            <li>PrivaVPN Zugangsdaten</li>
            <li>Blatt und Stift zum Notieren Ihres Passworts</li>
            </ul>
        </div>
    </div>

</div>

<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="skip_step" class="btn btn-primary btn-lg float-right"
            type="submit">
         Weiter
    </button>
</div>
"""

## TODO:
## Needs to be loaded this way, since we can't inject JS into divs etc in the HTML above.
javascript = """
document.querySelector('#skip_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/rechtliches',
    })
})
"""

def on_request(frame):
	if '_module' in frame.data and frame.data['_module'] == 'installation_steps/willkommen':
		yield {
			'html' : html,
			'javascript' : javascript,
			'_modules' : 'vpn'
		}

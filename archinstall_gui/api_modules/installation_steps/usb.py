import json
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import session

if 'harddrive' in session.steps:
#if True in session.steps:
	html = f"""
    <div class="padded_content flex_grow flex column" style="min-width:100%">
		<h3><b>PRIVASTICK VERSCHLÜSSELUNG (OPTIONAL)</b></h3>
		<span>UM IHRE DATEN AUF DEM PRIVASTICK VOR UNERLAUBTEM ZUGRIFF ZU SCHÜTZTEN, KÖNNEN SIE IHR EIGENES VERSCHLÜSSELUNGS-PASSWORT VERGEBEN.</span>

		<div class="note">
			<div class="noteHeader"><div class="noteIcon"></div><span>Note</span></div>
			<div class="noteBody">
				<!--Disk encryption is optional, but if you value your local data <i>(including web browser history and logins)</i>, it's strongly
				adviced that disk encryption is enabled. The minimum system requirements for disk encryption increases to <div class="inlineCode">1 GB</div> of RAM.-->
				Die Sicherheit Ihrer Daten hängt von der Stärke Ihres Passworts ab.
			</div>
		</div>

		<div class="warning">
			<div class="warningHeader"><div class="noteIcon"></div><span>Warning</span></div>
			<div class="noteBody">
				<!--The password prompt while unlocking a drive is always <div class="inlineCode">en_US.UTF-8</div>, keep this in mind if you choose a password with special characters, that when prompted during boot for a disk password, the passphrase will be inputted with US keyboard layout<a target="_blank" href="https://bbs.archlinux.org/viewtopic.php?id=173506">[1]</a>.-->
				ACHTUNG: Falls Sie Ihr Passwort verlieren sollten, gibt es im Falle eines starken Passworts keinen Weg wie Sie Ihre Daten retten können. Notieren Sie sich Ihr Passwort und bewahren Sie es an einem sicheren Ort auf.
			</div>
		</div>


		<div class="form-area" id="form-area">
			<div class="input-form" id="input-form">
				<input type="text" id="password1" required autocomplete="off" onkeyup="check(this);"/>
				<label class="label">
					<span class="label-content">Passwort hier eingeben...</span>
				</label>
			</div>
		</div>

		<div class="form-area" id="form-area">
			<div class="input-form" id="input-form">
				<input type="text" id="password2" required autocomplete="off" onkeyup="check(this);"/>
				<label class="label">
					<span class="label-content">Passwort hier bestätigen...</span>
				</label>
			</div>
		</div>
		
		<!--
		<div class="buttons bottom" id="buttons">
			<button id="saveButton">Enable Disk Encryption</button>
			<button id="skipButton">Don't use disk encryption</button>
		</div>
		-->

</div>
<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="back_step" class="btn btn-primary btn-lg"
            type="submit">
         Zurück
    </button>
    <button id="connect" class="btn btn-primary btn-lg float-right"
            type="submit">
         Fertigstellen
    </button>
</div>
	"""
else:
	html = 'Previous step not completed.'

javascript = """
window.disk_password_input = document.querySelector('#disk_password');
window.hostname_input = document.querySelector('#hostname');

function check_(input) {
		console.log(input);
}

function check(input) {
		console.log(input);
		let input1 = document.querySelector('#user').value
		let input2 = document.querySelector('#password').value
		if ( input1.includes("@privavpn.de") && input2.length == 9) {
				var continue_button = document.getElementById("connect");
				continue_button.classList.remove("no-click");
				continue_button.classList.remove("btn-secondary");
				continue_button.classList.add("btn-primary");
		} else {
				var continue_button = document.getElementById("connect");
				continue_button.classList.add("no-click");
				continue_button.classList.add("btn-secondary");
				continue_button.classList.remove("btn-primary");
		}
}

*/
if(disk_password) {
	disk_password_input.value = disk_password;
	disk_password_input.disabled = true;
}
*/

if(hostname) {
	hostname_input.value = hostname;
}

document.querySelector('#saveButton').addEventListener('click', function() {
	disk_password = document.querySelector('#disk_password').value;

	socket.send({
		'_module' : 'installation_steps/encryption',
		'disk_password' : disk_password
	})
})

document.querySelector('#skipButton').addEventListener('click', function() {
	socket.send({
		'_module' : 'installation_steps/harddrive',
		'format' : true
	})
})
"""

def notify_partitioning_started(worker, *args, **kwargs):
	worker.frame.CLIENT_IDENTITY.send({
		'type' : 'notification',
		'source' : 'harddrive',
		'message' : f"Paritioning has started on <div class=\"inlineCode\">{session.information['drive']}</div>",
		'status' : 'active'
	})
def notify_base_install_done(worker, *args, **kwargs):
	worker.frame.CLIENT_IDENTITY.send({
		'type' : 'notification',
		'source' : 'arch_linux',
		'message' : '<div class="balloon">Base installation complete.</div>',
		'status' : 'complete'
	})

def strap_in_the_basics_with_encryption(frame, disk_password, drive, worker, hostname='Archnistall', *args, **kwargs):
	with archinstall.Filesystem(drive, archinstall.GPT) as fs:
		# Use partitioning helper to set up the disk partitions.
		fs.use_entire_disk('luks2')

		if drive.partition[1].size == '512M':
			raise OSError('Trying to encrypt the boot partition for petes sake..')
		
		frame.CLIENT_IDENTITY.send({
			'type' : 'notification',
			'source' : 'harddrive',
			'message' : 'Paritioning is done',
			'status' : 'complete'
		})

		frame.CLIENT_IDENTITY.send({
			'type' : 'notification',
			'source' : 'encryption',
			'message' : f"Encrypting <div class=\"inlineCode\">{drive.partition[1]}</div>",
			'status' : 'active'
		})

		drive.partition[0].format('fat32')
		# First encrypt and unlock, then format the desired partition inside the encrypted part.
		with archinstall.luks2(drive.partition[1], 'luksloop', disk_password) as unlocked_device:
			unlocked_device.format('btrfs')

			frame.CLIENT_IDENTITY.send({
				'type' : 'notification',
				'source' : 'encryption',
				'message' : f"Encryption is done.",
				'status' : 'complete'
			})
			
			session.handles['filesystem'] = fs
			session.handles['boot'] = drive.partition[0]
			session.handles['root'] = unlocked_device

			frame.CLIENT_IDENTITY.send({
				'type' : 'notification',
				'source' : 'arch_linux',
				'message' : 'Installing base operating system',
				'status' : 'active'
			})

			with archinstall.Installer(unlocked_device, boot_partition=drive.partition[0], hostname=hostname) as installation:
				if installation.minimal_installation():
					installation.add_bootloader()

					session.steps['arch_linux'] = installation
					session.steps['arch_linux_worker'] = worker

	return True

def on_request(frame):
	if '_module' in frame.data and frame.data['_module'] == 'installation_steps/usb':
		if not 'harddrive' in session.steps:
			session.steps['harddrive'] = True
			yield {
				'status' : 'error',
				'_modules' : 'usb',
				'next' : 'usb'
			}
			return

		if not 'disk_password' in frame.data:
			yield {
				'html' : html,
				'javascript' : javascript,
				'_modules' : 'usb'
			}
		else:
			#session.steps['encryption'] = spawn(frame, strap_in_the_basics_with_encryption, disk_password=frame.data['disk_password'], drive=session.information['drive'], start_callback=notify_partitioning_started, callback=notify_base_install_done, dependency='mirrors')
			yield {
				'html' : html,
				'javascript' : javascript,
				'_modules' : 'usb' 
			}

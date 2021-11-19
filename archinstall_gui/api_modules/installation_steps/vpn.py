import json
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import session

if 'internet' in session.steps:
#if 'harddrive' in session.steps:
	html = f"""
    <!--
	<div class="padded_content flex_grow flex column">
		<h3>Disk Encryption <i>(Optional)</i></h3>

		<div class="note">
			<div class="noteHeader"><div class="noteIcon"></div><span>Note</span></div>
			<div class="noteBody">
				Disk encryption is optional, but if you value your local data <i>(including web browser history and logins)</i>, it's strongly
				adviced that disk encryption is enabled. The minimum system requirements for disk encryption increases to <div class="inlineCode">1 GB</div> of RAM.
			</div>
		</div>

		<div class="warning">
			<div class="warningHeader"><div class="noteIcon"></div><span>Warning</span></div>
			<div class="noteBody">
				The password prompt while unlocking a drive is always <div class="inlineCode">en_US.UTF-8</div>, keep this in mind if you choose a password with special characters, that when prompted during boot for a disk password, the passphrase will be inputted with US keyboard layout<a target="_blank" href="https://bbs.archlinux.org/viewtopic.php?id=173506">[1]</a>.
			</div>
		</div>
		<div class="form-area" id="form-area">
			<div class="input-form" id="input-form">
				<input type="password" id="disk_password" required autocomplete="off" />
				<label class="label">
					<span class="label-content">Enter a disk password</span>
				</label>
			</div>
		</div>
		
		<div class="buttons bottom" id="buttons">
			<button id="saveButton">Enable Disk Encryption</button>
			<button id="skipButton">Don't use disk encryption</button>
		</div>
	</div>
    -->

    <div class="padded_content flex_grow flex column">
        <h3>VPN-Verbindung herstellen (Optional)</h3>
        <span>Wenn Sie den VPN-Zugriff einrichten möchten, ermöglicht Ihnen das dies dieser Abschnitt. Sie können den Vorgang aber auch überspringen.</span>

        <div class="note" id="arch_linux_worker_wait">
            <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
            <div class="noteBody">
                Die VPN-Verbindung kann erst hergestellt werden sobald Sie mit dem Internet verbunden sind.
            </div>
        </div>

        <div class="warning">
            <div class="warningHeader"><div class="noteIcon"></div><span>Warnung</span></div>
            <div class="noteBody">
                <!--By default, the <div class="inlineCode">root</div> account is disabled. <b>Skipping this step</b> or <i>not</i> setting sudo permission for the new users <b>requires you to set a root password</b> <i>(A popup prompt will ask you if you skip)</i>.-->
                Ihr VPN-Zugang ist hiernach standardmäßig aktiviert. Sie können den VPN aber zu einem späteren Zeitpunkt noch bequem ein- beziehungsweise ausschalten.
            </div>
        </div>

        <div class="form-area">
            <div class="input-form" id="input-form">
                <input type="text" id="user" required autocomplete="off" />
                <label class="label">
                    <span class="label-content">VPN Nutzername</span>
                </label>
            </div>
        </div>

        <div class="form-area">
            <div class="input-form" id="input-form">
                <input type="text" id="password" required autocomplete="off" />
                <label class="label">
                    <span class="label-content">VPN Passwort</span>
                </label>
            </div>
        </div>

        <!--
        <div class="form-area-oneline">
            <input type="checkbox" id="sudoer" value="yes">
            <label for="sudoer">Add user to sudoer list?</label>
        </div>
        -->

        <div class="buttons bottom">
            <button id="create_user">VPN Verbindung herstellen</button>
            <button id="skip_accounts">Überspringen</button>
			<button id="skipButton">Don't use disk encryption</button>
        </div>
    </div>
	"""
else:
	html = """
	<div class="padded_content flex_grow flex column">
		<div class="warning">
			<div class="warningHeader"><div class="noteIcon"></div><span>Warnung</span></div>
			<div class="noteBody">
                Bitte verbinden sie sich mit dem Internet um fortzufahren.
			</div>
		</div>
    </div>
"""

javascript = """
window.disk_password_input = document.querySelector('#disk_password');
window.hostname_input = document.querySelector('#hostname');

if(disk_password) {
	disk_password_input.value = disk_password;
	disk_password_input.disabled = true;
}

if(hostname) {
	hostname_input.value = hostname;
}

/*
document.querySelector('#saveButton').addEventListener('click', function() {
	disk_password = document.querySelector('#disk_password').value;

	socket.send({
		'_module' : 'installation_steps/encryption',
		'disk_password' : disk_password
	})
})
*/

window.showRootPwPrompt = () => {
	let area = document.createElement('div');
	area.innerHTML = '<span>You opted in to skip this step, or a sudo user was not selected. This requires you to set a root password <i>(blank password works fine too)</i> or go back and create a sudo user since the root account is by default locked/disabled. You can go back by closing this popup.</span>'

	let form_area = document.createElement('div');
	form_area.classList = 'form-area';
	area.appendChild(form_area);

	let input_form = document.createElement('div');
	input_form.classList = 'input-form';
	form_area.appendChild(input_form);

	let root_pw_input = document.createElement('input');
	root_pw_input.type = 'password';
	root_pw_input.required = true;
	root_pw_input.autocomplete = 'off'; // Strictly not nessecary
	input_form.appendChild(root_pw_input);

	let root_pw_label = document.createElement('label');
	root_pw_label.classList = 'label';
	input_form.appendChild(root_pw_label);

	let label_span = document.createElement('span');
	label_span.classList='label-content';
	label_span.innerHTML = 'Choose a root password <i>(empty entry is allowed)</i>'
	root_pw_label.appendChild(label_span);

	let buttons = document.createElement('div');
	buttons.classList = 'buttons bottom';
	area.appendChild(buttons);

	let save_btn = document.createElement('button');
	save_btn.innerHTML = 'Set root password';
	buttons.appendChild(save_btn);

	let cancel_btn = document.createElement('button');
	cancel_btn.innerHTML = 'Go back';
	buttons.appendChild(cancel_btn);

	let frame = popup(area);

	save_btn.addEventListener('click', () => {
		socket.send({
			'_module' : 'installation_steps/accounts',
			'root_pw' : root_pw_input.value
		})
		frame.remove();
	})

	cancel_btn.addEventListener('click', () => {
		frame.remove();
	})
}

document.querySelector('#create_user').addEventListener('click', function() {
	let username = document.querySelector('#user').value;
	let password = document.querySelector('#password').value;
	let sudo = document.querySelector('#sudoer').checked;

	if(username.length <= 0 || !sudo) {
		showRootPwPrompt();
	} else {
		reboot_step = 'accounts';

		socket.send({
			'_module' : 'installation_steps/accounts',
			'username' : username,
			'password' : password,
			'sudo' : sudo
		})
	}
})

document.querySelector('#skipButton').addEventListener('click', function() {
	socket.send({
		'_module' : 'installation_steps/vpn',
		'skip_vpn' : true,
        'dependencies' : ['vpn']
	})
})

document.querySelector('#skip_accounts').addEventListener('click', function() {
	socket.send({
		'_module' : 'installation_steps/vpn',
		'skip_vpn' : true,
        'dependencies' : ['vpn']
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
		'message' : '<div class="balloon">Installation complete, click here to <b class="reboot" onClick="reboot();">reboot</b> when you\'re done</div>',
		'sticky' : True,
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
	if '_module' in frame.data and frame.data['_module'] == 'installation_steps/vpn':
		if 'skip_vpn' in frame.data:
			#session.steps['profiles'] = spawn(frame, stub, dependency='vpn')
			yield {
				'_modules' : 'vpn',
				'status' : 'skipped',
				'next' : 'profil'
			}
			return

		if not 'internet' in session.steps:
			yield {
				'status' : 'incomplete',
				'next' : 'internet',
				'_modules' : 'vpn'
			}
			return

		if not 'disk_password' in frame.data:
			yield {
				'status' : 'success',
				'html' : html,
				'javascript' : javascript,
				'_modules' : 'vpn'
			}

		else:
			#session.steps['encryption'] = spawn(frame, strap_in_the_basics_with_encryption, disk_password=frame.data['disk_password'], drive=session.information['drive'], start_callback=notify_partitioning_started, callback=notify_base_install_done, dependency='mirrors')
			yield {
				'status' : 'complete',
				'next' : 'profil',
				'_modules' : 'vpn' 
			}

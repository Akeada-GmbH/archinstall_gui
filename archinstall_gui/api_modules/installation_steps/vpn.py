import json
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import session

if 'internet' in session.steps:
#if 'harddrive' in session.steps:
    html = f"""
    <div class="padded_content flex_grow flex column" style="min-width:100%">
        <h3><b>VPN-VERBINDUNG HERSTELLEN</b></h3>
        <span>IN DIESEM ABSCHNITT KÖNNEN SIE DIE VPN-VERBINDUNG EINRICHTEN.</span>

        <div style="padding-top:50px;">
        <div class="note" id="arch_linux_worker_wait">
            <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
            <div class="noteBody">
                Die VPN-Verbindung kann erst hergestellt werden sobald Sie mit dem Internet verbunden sind.
            </div>
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
                <input type="text" id="user" required autocomplete="off" oninput="check_credentials(this.value);"/>
                <label class="label">
                    <span class="label-content">VPN Nutzername</span>
                </label>
            </div>
        </div>

        <div class="form-area">
            <div class="input-form" id="input-form">
                <input type="text" id="password" required autocomplete="off" oninput="check_credentials(this.value);"/>
                <label class="label">
                    <span class="label-content">VPN Passwort</span>
                </label>
            </div>
        </div>

        <!--<div style="padding-top:100px;text-align:right;"><div style="min-height:360px;"><div style="width:100%;height:0;padding-bottom:50%;position:relative;"><iframe style="border:none;position:absolute;top:0;left:0;width:100%;height:100%;min-height:360px;border:none;overflow:hidden !important;" src="https://www.metercustom.net/plugin/?hl=de"></iframe></div></div>Anbieter <a href="https://www.geschwindigkeit.de">Geschwindigkeit.de</a></div>-->

    </div>

<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="back_step" class="btn btn-primary btn-lg"
            type="submit">
         Zurück
    </button>
    <button id="connect" class="btn btn-secondary btn-lg float-right no-click"
            type="submit">
         Verbinden
    </button>
</div>

    """
elif 'vpn' in session.steps:
    html = """
    <div class="padded_content flex_grow flex column">
        <div class="warning">
            <div class="warningHeader"><div class="noteIcon"></div><span>Warnung</span></div>
            <div class="noteBody">
                Bitte klicken Sie auf den Start-Button um einen Internet-Geschwindigkeitstest durchzuführen.
            </div>
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

function check_credentials(input) {
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


document.querySelector('#connect').addEventListener('click', function() {
    disk_password = document.querySelector('#password').value;

    console.log(password.value)

    socket.send({
        '_module' : 'installation_steps/vpn',
        'disk_password' : password.value
    })
})


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

document.querySelector('#back_step').addEventListener('click', function() {
	console.log("test") 
	socket.send({
		'_module' : 'installation_steps/internet',
	})
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
                'next' : 'apps'
            }
            return

        if not 'internet' in session.steps:
            yield {
                'status' : 'incomplete',
                'next' : 'willkommen',
                '_modules' : 'vpn'
            }
            return

        if not 'disk_password' in frame.data:
            yield {
                'status' : 'error',
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'vpn'
            }

        else:
            #session.steps['encryption'] = spawn(frame, strap_in_the_basics_with_encryption, disk_password=frame.data['disk_password'], drive=session.information['drive'], start_callback=notify_partitioning_started, callback=notify_base_install_done, dependency='mirrors')
            yield {
                'status' : 'complete',
                'next' : 'apps',
                '_modules' : 'vpn' 
            }

import json
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import subprocess

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
while (document.getElementById('popup')) {
    document.getElementById('popup').remove()
}

function check_credentials(input) {
		let input1 = document.querySelector('#user').value
		let input2 = document.querySelector('#password').value
		if ( input1.includes("@privavpn.de") && input2.length == 10) {
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

function check_credentials_2(vpn_username, vpn_password) {
    var url = "http://vpn-api.01.priva.dev:19999";
    var data = JSON.stringify({"Username": vpn_username, "Password": vpn_password});
    // Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'no-cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}
postData(url, data)
  .then(data => {
    console.log(data); // JSON data parsed by `data.json()` call
  });

}



document.querySelector('#connect').addEventListener('click', function() {
    vpn_username = document.querySelector('#user').value;
    vpn_password = document.querySelector('#password').value;

    socket.send({
        '_module' : 'installation_steps/vpn',
        'vpn_credentials' : [ vpn_username, vpn_password ],
    })

    socket.send({
        '_module' : 'installation_steps/vpn',
        'continue' : true,
    })

    console.log(Object.keys('vpn_active'))

	if(vpn_username.length <= 0 ) {
		// showRootPwPrompt();
	} else {
		// showRootPwPrompt();

	}


})

document.querySelector('#back_step').addEventListener('click', function() {
	socket.send({
		'_module' : 'installation_steps/internet',
        'back' : true
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
        if 'back' in frame.data:
            yield {
                'status' : 'success',
                '_modules' : 'vpn'
            }
            yield {
                'next' : 'vpn',
                'status' : 'success',
                '_modules' : 'apps'
            }
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

        if not 'vpn_credentials' in frame.data and not 'continue' in frame.data:
            yield {
                'status' : 'error',
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'vpn'
            }

        else:

            if 'vpn_credentials' in frame.data:

                #session.steps['encryption'] = spawn(frame, strap_in_the_basics_with_encryption, disk_password=frame.data['disk_password'], drive=session.information['drive'], start_callback=notify_partitioning_started, callback=notify_base_install_done, dependency='mirrors')
                vpn_user = frame.data['vpn_credentials'][0]
                vpn_pass = frame.data['vpn_credentials'][1]

                # import pdb; pdb.set_trace()

                mycmd=subprocess.getoutput("echo '{0}\n{1}' | /usr/share/privastick/scripts/PrivastickVPNSetup".format(vpn_user,vpn_pass)).split('\n')[-1]

                if 'Falsche Benutzerdaten.' in mycmd:
                    session.information['vpn_active'] = False
                    yield {
                        'status' : 'error',
                        'html' : html,
                        'javascript' : javascript,
                        '_modules' : 'vpn'
                    }
                else:
                    session.information['vpn_active'] = True
                    yield {
                        'status' : 'complete',
                        'html' : html,
                        'javascript' : javascript,
                        '_modules' : 'vpn'
                    }

            elif 'continue' in frame.data:

                yield {
                    'next' : 'apps',
                    '_modules' : 'vpn' 
                }

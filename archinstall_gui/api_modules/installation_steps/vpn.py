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
                <input type="text" id="user" required autocomplete="off"/>
                <label class="label">
                    <span class="label-content">VPN Nutzername</span>
                </label>
            </div>
        </div>

        <div class="form-area">
            <div class="input-form" id="input-form">
                <input type="text" id="password" required autocomplete="off"/>
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
    <button id="connect" class="btn btn-primary btn-lg float-right"
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

document.querySelector('#connect').addEventListener('click', function() {
    vpn_username = document.querySelector('#user').value;
    vpn_password = document.querySelector('#password').value;

    socket.send({
        '_module' : 'installation_steps/vpn',
        'vpn_credentials' : [ vpn_username, vpn_password ],
    })

    socket.send({
        '_module' : 'installation_steps/finalisieren',
    })

    // console.log(Object.keys('vpn_active'))

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
                '_modules' : 'finalisieren'
            }
        if 'skip_vpn' in frame.data:
            #session.steps['profiles'] = spawn(frame, stub, dependency='vpn')
            yield {
                '_modules' : 'vpn',
                'status' : 'skipped',
                'next' : 'finalisieren'
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

                mycmd=subprocess.getoutput("echo '{0}\n{1}' | /usr/share/privastick/scripts/PrivaStickVPNSetup".format(vpn_user,vpn_pass)).split('\n')[-1]

                #ps = subprocess.Popen(['printf','%s\n', '{0}'.format(vpn_user), '{0}'.format(vpn_pass)], stdout=subprocess.PIPE)

                #output = subprocess.check_output(['/usr/share/privastick/scripts/PrivastickVPNSetup'], stdin=ps.stdout)

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
                        '_modules' : 'vpn',
                    }
                    return

            elif 'continue' in frame.data:

                yield {
                    'status' : 'complete',
                    'next' : 'vpn',
                    '_modules' : 'vpn' 
                }
                return

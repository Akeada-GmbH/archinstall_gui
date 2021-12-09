import json, time
from os.path import isdir, isfile

import os

from dependencies import archinstall
from lib.worker import spawn

import session

DRIVES = None

html = """
<div class="padded_content flex_grow flex column" style="min-width: 80%;">
    <h3><b>INTERNET VERBINDEN</b></h3>
    <span>BITTE WÄHLEN SIE IHR WLAN-NETZWERK AUS UND VERBINDEN SIE SICH MIT DEM INTERNET</span>
    <div class="note">
        <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
        <div class="noteBody">
            Es kann einen Moment dauern, bis Ihnen verfügbare WLAN-Hotspots angezeigt werden.
        </div>
    </div>
    <!--
    <div class="form-area">
        <div class="input-form" id="input-form">
            <input type="text" id="password" required autocomplete="off" />
            <label class="label">
                <span class="label-content">Ihr WLAN-Passwort (falls vorhanden) bitte hier eingeben...</span>
            </label>
        </div>
    </div>
    -->

    <br>
    <br>

    <select id="drives" class="flex_grow" size="3">
    </select>
    <div class="drive_information">

    </div>
</div>

<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="back_step" class="btn btn-primary btn-lg"
            type="submit">
         Zurück
    </button>
    <button id="select_disk" class="btn btn-primary btn-lg float-right"
            type="submit">
         Weiter
    </button>
</div>
"""

## TODO:
## Needs to be loaded this way, since we can't inject JS into divs etc in the HTML above.
javascript = """
window.showWifiPwPrompt = (selected_drive, data) => {
    let area = document.createElement('div');
	area.innerHTML = '<span>Bitte geben Sie Ihr WLAN-Passwort ein <i>(falls vorhanden)</i> und klicken Sie anschließend auf <b>Verbinden</b></span>'

    let form_area = document.createElement('div');
    form_area.classList = 'form-area';
    area.appendChild(form_area);

    let input_form = document.createElement('div');
    input_form.classList = 'input-form';
    form_area.appendChild(input_form);

    let root_pw_input = document.createElement('input');
    root_pw_input.type = 'text';
    root_pw_input.required = true;
    root_pw_input.autocomplete = 'off'; // Strictly not nessecary
    input_form.appendChild(root_pw_input);

    let root_pw_label = document.createElement('label');
    root_pw_label.classList = 'label';
    input_form.appendChild(root_pw_label);

    let label_span = document.createElement('span');
    label_span.classList='label-content';
    // label_span.innerHTML = 'Choose a root password <i>(empty entry is allowed)</i>'
    label_span.innerHTML = 'Passwort hier eingeben...'
    root_pw_label.appendChild(label_span);

    let buttons = document.createElement('div');
    buttons.classList = 'form-group';
    area.appendChild(buttons);

    let save_btn = document.createElement('button');
    save_btn.classList = 'btn btn-primary btn-lg float-right'
    save_btn.style.listStyle = 'padding-bottom:10px;'
    save_btn.innerHTML = 'Verbinden';
    buttons.appendChild(save_btn);

    /*
    let cancel_btn = document.createElement('button');
    cancel_btn.classList = 'btn btn-secondary btn-lg'
    cancel_btn.innerHTML = 'Go back';
    buttons.appendChild(cancel_btn);
    */

    let frame = popup(area);


    save_btn.addEventListener('click', () => {
        console.log(root_pw_input.value);

        socket.send({
            '_module' : 'installation_steps/internet',
            'hardware' : {
                'drive' : [ selected_drive, data ],
                'password' : root_pw_input.value
            },
            'dependencies' : ['vpn']
        })

    })

    /*
    cancel_btn.addEventListener('click', () => {
        frame.remove();
    })
    */
}

window.drives_dropdown = document.querySelector('#drives');

window.refresh_drives = () => {
    window.drives_dropdown.innerHTML = '';
    let i = 0;
    Object.keys(drives).forEach((drive) => {
        i = i + 1;
        let option = document.createElement('option');
        option.value = drive;
        // option.innerHTML = `${drive} (${drives[drive]['info']['size']}, ${drives[drive]['info']['label']}, ${drives[drive]['info']['mountpoint']})`;
        option.innerHTML = `${drives[drive]}`;
        window.drives_dropdown.appendChild(option);
    })
}

window.drives_dropdown.addEventListener('change', function(obj) {
    selected_drive = this.value;
    console.log(selected_drive);

})

document.querySelector('#back_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/rechtliches',
        'back' : true
    })
})

window.update_drives = (data) => {
    console.log(data);
    if(typeof data['drives'] !== 'undefined') {
        Object.keys(data['drives']).forEach((drive) => {
            drives[drive] = data['drives'][drive];
        })
        window.refresh_drives()
        document.querySelector('#select_disk').addEventListener('click', function() {
            showWifiPwPrompt(selected_drive, data);
        })

    }


}

if(socket.subscriptions('drive_list') != 2)
    socket.subscribe('drive_list', update_drives);

socket.send({
    '_module' : 'installation_steps/internet',
    'hardware' : 'refresh'
})

"""

def notify_partitioning_started(worker, *args, **kwargs):
    worker.frame.CLIENT_IDENTITY.send({
        'type' : 'notification',
        'source' : 'internet',
        'message' : f"Paritioning has started on <div class=\"inlineCode\">{session.information['drive']}</div>",
        'status' : 'active'
    })
def notify_partitioning_done(worker, *args, **kwargs):
    worker.frame.CLIENT_IDENTITY.send({
        'type' : 'notification',
        'source' : 'internet',
        'message' : 'Paritioning is done',
        'status' : 'complete'
    })
def notify_base_install_started(worker, *args, **kwargs):
    worker.frame.CLIENT_IDENTITY.send({
        'type' : 'notification',
        'source' : 'arch_linux',
        'message' : 'Installing base operating system',
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

def strap_in_the_basics(frame, drive, worker, hostname='Archnistall', *args, **kwargs):
    with archinstall.Filesystem(drive, archinstall.GPT) as fs:
        # Use partitioning helper to set up the disk partitions.
        fs.use_entire_disk('ext4')

        if drive.partition[1].size == '512M':
            raise OSError('Trying to encrypt the boot partition for petes sake..')

        drive.partition[0].format('fat32')
        drive.partition[1].format('ext4')

        session.handles['filesystem'] = fs
        session.handles['boot'] = drive.partition[0]
        session.handles['root'] = drive.partition[1]

        frame.CLIENT_IDENTITY.send({
            'type' : 'notification',
            'source' : 'internet',
            'message' : 'Paritioning is done',
            'status' : 'complete'
        })

        frame.CLIENT_IDENTITY.send({
            'type' : 'notification',
            'source' : 'vpn',
            'message' : 'Installing base operating system',
            'status' : 'active'
        })

        with archinstall.Installer(drive.partition[1], boot_partition=drive.partition[0], hostname=hostname) as installation:
            if installation.minimal_installation():
                installation.add_bootloader()

                session.steps['arch_linux'] = installation
                session.steps['arch_linux_worker'] = worker

    # Verified: Filesystem() doesn't do anything shady on __exit__
    #           other than sync being called.
    return True

def on_request(frame):
    if '_module' in frame.data and frame.data['_module'] == 'installation_steps/internet':
        if 'back' in frame.data:
            yield {
                'status' : 'success',
                '_modules' : 'internet'
            }
            yield {
                'next' : 'internet',
                'status' : 'success',
                '_modules' : 'vpn'
            }
        if 'skip' in frame.data:
            #session.steps['profiles'] = spawn(frame, stub, dependency='vpn')
            session.steps['internet'] = True
            yield {
                '_modules' : 'rechtliches',
                'status' : 'complete',
                'next' : 'vpn'
            }
            yield {
                '_modules' : 'internet',
                'status' : 'complete',
                'next' : 'vpn'
            }
        if not 'hardware' in frame.data and 'format' not in frame.data:
            yield {
                '_modules' : 'rechtliches',
                'status' : 'complete',
            }
            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'internet'
            }
        elif 'hardware' in frame.data and frame.data['hardware'] == 'refresh':

            DRIVES = archinstall.get_wireless_networks("wlan0")

            yield {
                'drives' : DRIVES,
                '_modules' : 'drive_list'
            }

        elif 'hardware' in frame.data and type(frame.data['hardware']) == dict:


            if 'drive' in frame.data['hardware']:
                selected_drive = frame.data['hardware']['drive']
                os.system("nmcli d wifi connect {0} password {1}".format(frame.data['hardware']['drive'][1]['drives'][int(selected_drive[0])].split(':')[2], frame.data['hardware']['password']))
                session.steps['internet'] = True

                yield {
                    'status' : 'complete',
                    '_modules' : 'internet',
                    'next' : 'vpn'
                }

        elif 'format' in frame.data:
            if 'arch_linux' not in session.steps:
                session.steps['arch_linux'] = spawn(frame, strap_in_the_basics, drive=session.information['drive'], start_callback=notify_partitioning_started, callback=notify_base_install_done, dependency='mirrors')
                session.steps['encryption'] = True

                yield {
                    'status' : 'success',
                    'next' : 'mirrors', # arch_linux doesn't contain anything (yet)
                    '_modules' : 'encryption' 
                }

                yield {
                    'type' : 'notification',
                    'source' : 'encryption',
                    'message' : 'Encryption skipped',
                    'status' : 'skipped'
                }

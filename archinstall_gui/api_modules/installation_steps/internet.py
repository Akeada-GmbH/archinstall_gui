import json, time
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import session

html = """
<div class="padded_content flex_grow flex column">
    <h3>WLAN einrichten</h3>
    <span>Wählen Sie einen WLAN-Hotspot aus, mit dem Sie sich verbinden möchten.</span>
    <div class="note">
        <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
        <div class="noteBody">
            Es kann einen Moment dauern, bis Ihnen verfügbare WLAN-Hotspots angezeigt werden.
        </div>
    </div>
    <div class="form-area">
        <div class="input-form" id="input-form">
            <input type="text" id="password" required autocomplete="off" />
            <label class="label">
                <span class="label-content">Ihr WLAN-Passwort (falls vorhanden) bitte hier eingeben...</span>
            </label>
        </div>
    </div>
    <br>
    <br>

    <select id="drives" class="flex_grow" size="3">
    </select>
    <div class="drive_information">

    </div>

    <div class="buttons bottom">
        <button id="select_disk">Verbinden</button>
    </div>
</div>
"""

## TODO:
## Needs to be loaded this way, since we can't inject JS into divs etc in the HTML above.
javascript = """
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

document.querySelector('#select_disk').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/internet',
        'hardware' : {
            'drive' : selected_drive
        },
        'dependencies' : ['vpn']
    })
})

window.update_drives = (data) => {
    console.log(data);
    if(typeof data['drives'] !== 'undefined') {
        Object.keys(data['drives']).forEach((drive) => {
            drives[drive] = data['drives'][drive];
        })
        window.refresh_drives()
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
        if not 'hardware' in frame.data and 'format' not in frame.data:
            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'internet'
            }
        elif 'hardware' in frame.data and frame.data['hardware'] == 'refresh':
            yield {
                'drives' : archinstall.get_wireless_networks("wlan0"),
                '_modules' : 'drive_list'
            }
        elif 'hardware' in frame.data and type(frame.data['hardware']) == dict:
            if 'drive' in frame.data['hardware']:
                selected_drive = frame.data['hardware']['drive']
                session.information['drive'] = archinstall.get_wireless_networks("wlan0")[int(selected_drive)]
                session.steps['internet'] = True

                yield {
                    'status' : 'complete',
                    'next' : 'vpn',
                    '_modules' : 'internet' 
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

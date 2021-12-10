import json
from os.path import isdir, isfile

from dependencies import archinstall
from lib.worker import spawn

import session

import subprocess

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
                <input type="text" id="password1" required autocomplete="off" onkeyup="check_credentials_(this.value);"/>
                <label class="label">
                    <span class="label-content">Passwort hier eingeben...</span>
                </label>
            </div>
        </div>

        <div class="form-area" id="form-area">
            <div class="input-form" id="input-form">
                <input type="text" id="password2" required autocomplete="off" onkeyup="check_credentials_(this.value);"/>
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
    <button id="finish" class="btn btn-primary btn-lg float-right"
            type="submit">
         Installieren
    </button>
</div>
    """
else:
    html = 'Previous step not completed.'

javascript = """
console.log("test")
window.showRootPwPrompt2 = () => {
    let area = document.createElement('div');
    // area.innerHTML = '<span>You opted in to skip this step, or a sudo user was not selected. This requires you to set a root password <i>(blank password works fine too)</i> or go back and create a sudo user since the root account is by default locked/disabled. You can go back by closing this popup.</span>'
    // area.innerHTML = '<div style="width:720px;text-align:right;padding:10px;"><iframe style="border:none;overflow:hidden !important;width:100%;height:360px;" src="https://www.metercustom.net/plugin/?hl=de&th=w"></iframe>Anbieter <a href="https://www.geschwindigkeit.de">Geschwindigkeit.de</a></div>'
    area.innerHTML = "<div class='embed-container' style='min-width:720px;max-height:40%; padding-top=100px;'><iframe src='https://player.vimeo.com/video/574111364' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>"

    /*
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
    */

    let buttons = document.createElement('div');
    buttons.classList = 'form-group';
    area.appendChild(buttons);

    /*
    let save_btn = document.createElement('button');
    save_btn.classList = 'btn btn-primary btn-lg float-right'
    save_btn.style.listStyle = 'padding-bottom:10px;'
    save_btn.innerHTML = 'Weiter';
    buttons.appendChild(save_btn);
    */

    /*
    let cancel_btn = document.createElement('button');
    cancel_btn.classList = 'btn btn-secondary btn-lg'
    cancel_btn.innerHTML = 'Go back';
    buttons.appendChild(cancel_btn);
    */

    let frame = popup(area);

    save_btn.addEventListener('click', () => {

        /*
        socket.send({
            '_module' : 'installation_steps/vpn',
            'vpn_credentials' : [ vpn_username, vpn_password ],
        })
        */


        socket.send({
            '_module' : 'installation_steps/vpn',
            'continue' : true,
        })

        frame.remove();
    })

    /*
    cancel_btn.addEventListener('click', () => {
        frame.remove();
    })
    */
}

function handler(e) {
  e.stopPropagation();
  e.preventDefault();
}


document.querySelector('#finish').addEventListener('click', function() {
    
    disk_password = document.querySelector('#password1').value;
    disk_password_ = document.querySelector('#password2').value;

    if (disk_password == disk_password_) {

        socket.send({
            '_module' : 'installation_steps/usb',
            'disk_password' : disk_password
        })

        var finish_btn = document.getElementById("finish");
        var back_btn = document.getElementById("back_step");

        finish_btn.classList.remove("btn-primary");
        finish_btn.classList.add("no-click");
        finish_btn.classList.add("btn-secondary");

        back_btn.classList.remove("btn-primary");
        back_btn.classList.add("no-click");
        back_btn.classList.add("btn-secondary");

        showRootPwPrompt2();

        document.addEventListener("click", handler, true);

    }
    
})

document.querySelector('#back_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/apps',
        'back' : true
    })
})

function check_credentials_(input) {
        let input1 = document.querySelector('#password1').value
        let input2 = document.querySelector('#password2').value
        if ( input1 == input2) {
                var continue_button = document.getElementById("finish");
                continue_button.classList.remove("no-click");
                continue_button.classList.remove("btn-secondary");
                continue_button.classList.add("btn-primary");
        } else {
                var continue_button = document.getElementById("finish");
                continue_button.classList.add("no-click");
                continue_button.classList.add("btn-secondary");
                continue_button.classList.remove("btn-primary");
        }
}

"""

javascript_ = """
window.disk_password_input = document.querySelector('#disk_password');

window.showRootPwPrompt = () => {
    let area = document.createElement('div');
    // area.innerHTML = '<span>You opted in to skip this step, or a sudo user was not selected. This requires you to set a root password <i>(blank password works fine too)</i> or go back and create a sudo user since the root account is by default locked/disabled. You can go back by closing this popup.</span>'
    area.innerHTML = '<div class='embed-container' style='padding-top:100px;max-height:40%; padding-top=100px;'><iframe src='https://player.vimeo.com/video/574111364' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>

    /*
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
    */

    let buttons = document.createElement('div');
    buttons.classList = 'form-group';
    area.appendChild(buttons);

    let save_btn = document.createElement('button');
    save_btn.classList = 'btn btn-primary btn-lg float-right'
    save_btn.style.listStyle = 'padding-bottom:10px;'
    save_btn.innerHTML = 'Weiter';
    buttons.appendChild(save_btn);

    /*
    let cancel_btn = document.createElement('button');
    cancel_btn.classList = 'btn btn-secondary btn-lg'
    cancel_btn.innerHTML = 'Go back';
    buttons.appendChild(cancel_btn);
    */

    let frame = popup2(area);

    save_btn.addEventListener('click', () => {

        /*
        socket.send({
            '_module' : 'installation_steps/vpn',
            'vpn_credentials' : [ vpn_username, vpn_password ],
        })
        */


        socket.send({
            '_module' : 'installation_steps/usb',
        })

        frame.remove();
    })

    /*
    cancel_btn.addEventListener('click', () => {
        frame.remove();
    })
    */
}

showRootPwPrompt();

/*
if(disk_password) {
    disk_password_input.value = disk_password;
    disk_password_input.disabled = true;
}
*/

if(hostname) {
    hostname_input.value = hostname;
}



document.querySelector('#finish').addEventListener('click', function() {
    
    var finish_button = document.getElementById("finish");

    finish_button.classList.add("no-click");
    finish_button.classList.add("btn-secondary");
    finish_button.classList.remove("btn-primary");
    
    disk_password = document.querySelector('#password1').value;
    disk_password_ = document.querySelector('#password2').value;

    if (disk_password == disk_password_) {

        socket.send({
            '_module' : 'installation_steps/usb',
            'disk_password' : disk_password
        })

        showRootPwPrompt();

    }
    
})
/*
document.querySelector('#skipButton').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/harddrive',
        'format' : true
    })
})
*/
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
            disk_password = frame.data['disk_password']

            #textfile = open("/home/privauser/.cache/.disk_password", "w")
            #a = textfile.write(disk_password)
            #textfile.close()

            import pdb; pdb.set_trace()

            ps_pw = subprocess.Popen(['printf','%s\n', '{0}'.format(disk_password), '{0}'.format(disk_password)], stdout=subprocess.PIPE)

            output = subprocess.check_output(['passwd', 'privauser'], stdin=ps_pw.stdout)

            ps_pw.wait()

            #ps_install=subprocess.getoutput("bash /home/privauser/.config/ps-tools/scripts/install.sh > /home/privauser/.cache/ps-install.log")
            #ps_install.wait()

            ps_reencrypt = subprocess.Popen(['printf','%s\n', 'test', '{0}'.format(disk_password), '{0}'.format(disk_password)], stdout=subprocess.PIPE)

            output = subprocess.check_output(['bash', '/usr/share/privastick/scripts/PrivaStickReencrypt', 'cryptroot'], stdin=ps_reencrypt.stdout)

            ps_reencrypt.wait()


            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'usb' 
            }

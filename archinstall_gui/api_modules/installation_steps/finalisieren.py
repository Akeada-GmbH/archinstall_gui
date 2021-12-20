import json
import os
import time

from dependencies import archinstall
from lib.worker import spawn

import session

import subprocess

#if 'harddrive' in session.steps:
if True:
    html = f"""
    <div class="padded_content flex_grow flex column" style="min-width:100%">
        <h3><b>PRIVASTICK VERSCHLÜSSELUNG (OPTIONAL)</b></h3>
        <span>UM IHRE DATEN AUF DEM PRIVASTICK VOR UNERLAUBTEM ZUGRIFF ZU SCHÜTZTEN, KÖNNEN SIE IHR EIGENES VERSCHLÜSSELUNGS-PASSWORT VERGEBEN.</span>

        <div class="note">
            <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
            <div class="noteBody">
                <!--Disk encryption is optional, but if you value your local data <i>(including web browser history and logins)</i>, it's strongly
                adviced that disk encryption is enabled. The minimum system requirements for disk encryption increases to <div class="inlineCode">1 GB</div> of RAM.-->
                Vergeben Sie ein starkes Passwort, um fremden Zugriff zu verhindern.
            </div>
        </div>
        <!--
        <div class="warning">
            <div class="warningHeader"><div class="noteIcon"></div><span>Warnung</span></div>
            <div class="noteBody">
                ACHTUNG: Falls Sie Ihr Passwort verlieren sollten, gibt es im Falle eines starken Passworts keinen Weg wie Sie Ihre Daten retten können. Notieren Sie sich Ihr Passwort und bewahren Sie es an einem sicheren Ort auf.
            </div>
        </div>
        -->
        
    <span style="padding-top:5px;">
    Sie können die Software-Lizenzen
    <button id="show_licenses" onclick="show_license(this);">
    hier
    </button>
    einsehen.
    </span>


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

document.querySelector('#back_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/vpn',
        'back' : true
    })
})

document.querySelector('#finish').addEventListener('click', function() {
    
    disk_password = document.querySelector('#password1').value;
    disk_password_ = document.querySelector('#password2').value;

    if (disk_password == disk_password_) {

        socket.send({
            '_module' : 'installation_steps/finalisieren',
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

        // showRootPwPrompt2();

        document.addEventListener("click", handler, true);

    }
    
})

window.showRootPwPrompt2 = () => {
    let area = document.createElement('div');
    // area.innerHTML = '<span>You opted in to skip this step, or a sudo user was not selected. This requires you to set a root password <i>(blank password works fine too)</i> or go back and create a sudo user since the root account is by default locked/disabled. You can go back by closing this popup.</span>'
    // area.innerHTML = '<div style="width:720px;text-align:right;padding:10px;"><iframe style="border:none;overflow:hidden !important;width:100%;height:360px;" src="https://www.metercustom.net/plugin/?hl=de&th=w"></iframe>Anbieter <a href="https://www.geschwindigkeit.de">Geschwindigkeit.de</a></div>'
    area.innerHTML = "<div class='embed-container' style='min-width:720px;max-height:40%; padding-top=100px;'><iframe src='https://player.vimeo.com/video/574111364' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>"
    area.innerHTML = '<iframe style="min-width:500px; min-height:400px;" src="http://priva.dev/licenses" title="Software-Lizenzen"></iframe>'

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

    let frame = popup2(area);

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



function show_license(input) {

        showRootPwPrompt2();
}

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

document.querySelector('#back_step').addEventListener('click', function() {
    console.log("test");
    socket.send({
        '_module' : 'installation_steps/vpn',
        'skip' : true,
        'dependencies' : ['vpn']
    })
})

window.showRootPwPrompt2 = () => {
    let area = document.createElement('div');
    // area.innerHTML = '<span>You opted in to skip this step, or a sudo user was not selected. This requires you to set a root password <i>(blank password works fine too)</i> or go back and create a sudo user since the root account is by default locked/disabled. You can go back by closing this popup.</span>'
    // area.innerHTML = '<div style="width:720px;text-align:right;padding:10px;"><iframe style="border:none;overflow:hidden !important;width:100%;height:360px;" src="https://www.metercustom.net/plugin/?hl=de&th=w"></iframe>Anbieter <a href="https://www.geschwindigkeit.de">Geschwindigkeit.de</a></div>'
    // area.innerHTML = "<div class='embed-container' style='min-width:720px;max-height:40%; padding-top=100px;'><iframe src='https://player.vimeo.com/video/574111364' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>"
    area.innerHTML = "<iframe src="http://priva.dev:13337/licenses.html" title="Software-Lizenzen"></iframe>"

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

    let frame = popup2(area);

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

document.querySelector('#show_licenses').addEventListener('click', function() {
    show_licences();
})


document.querySelector('#finish').addEventListener('click', function() {

    console.log("test2");
    
    disk_password = document.querySelector('#password1').value;
    disk_password_ = document.querySelector('#password2').value;

    if (disk_password == disk_password_) {

        socket.send({
            '_module' : 'installation_steps/finalisieren',
            'disk_password' : disk_password
        })

        var finish_btn = document.getElementById("finish");
        var back_btn = document.getElementById("back_step");

        finish_btn.classList.remove("btn-primary");
        finish_btn.classList.add("no-click");
        finish_btn.classList.add("btn-secondary");

        /*

        back_btn.classList.remove("btn-primary");
        back_btn.classList.add("no-click");
        back_btn.classList.add("btn-secondary");
        */

        // showRootPwPrompt2();

        document.addEventListener("click", handler, true);

    }
    
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
    if '_module' in frame.data and frame.data['_module'] == 'installation_steps/finalisieren':
        if 'back' in frame.data:
            yield {
                'next' : 'vpn',
                'status' : 'success',
                '_modules' : 'finalisieren'
            }
            return
        if not 'disk_password' in frame.data:
            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'finalisieren'
            }
        else:

            disk_password = frame.data['disk_password']
            
            time.sleep(1)

            kill_pykib=subprocess.getoutput("pkill -f pykib")

            ps_install=subprocess.Popen(["bash", "/usr/share/privastick/scripts/PrivaStickInstaller/install"], stdout=subprocess.PIPE)

            ps_install.wait()

            if disk_password != "" and os.path.exists("/boot/.success"):
                
                ps_pw = subprocess.Popen(['printf','%s\n', '{0}'.format(disk_password), '{0}'.format(disk_password)], stdout=subprocess.PIPE)

                output = subprocess.check_output(['passwd', 'privauser'], stdin=ps_pw.stdout)

                ps_pw.wait()

                ps_reencrypt = subprocess.Popen(['printf','%s\n', 'privaroot', '{0}'.format(disk_password), '{0}'.format(disk_password)], stdout=subprocess.PIPE)

                output = subprocess.check_output(['bash', '/usr/share/privastick/scripts/PrivaStickReencrypt', 'cryptroot'], stdin=ps_reencrypt.stdout)

                ps_reencrypt.wait()

            if os.path.exists("/boot/.success"):

                for c in ["bash /usr/share/privastick/scripts/PrivaStickResize", "sed -i 's/i3/xfce/g' /etc/lightdm/lightdm.conf", "sed -i 's/privauser//g' /etc/lightdm/lightdm.conf", "sed -i 's/NOPASSWD: ALL/NOPASSWD: \/usr\/share\/privastick\/scripts\/PrivaStickVPNSetup, \/usr\/share\/privastick\/scripts\/misc\/toggle-vpn, \/usr\/share\/privastick\/scripts\/misc\/install-app, \/usr\/share\/privastick\/scripts\/misc\/remove-app/g' /etc/sudoers", "passwd -l root", "overlay_flush", "systemctl restart lightdm"]:

                    if c == "sed -i 's/privauser//g' /etc/lightdm/lightdm.conf" and disk_password == "":
                        continue
                        
                    ps_finish=subprocess.getoutput(c)

                    with open("/boot/install.log", "a") as f:
                        f.write(ps_finish)

            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'finalisieren' 
            }

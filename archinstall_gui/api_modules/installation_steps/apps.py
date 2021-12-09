import json, time, os
import urllib.request

from dependencies import archinstall
from lib.worker import spawn
import session

import subprocess

html = """
<div class="padded_content flex_grow flex column" style="min-width: 100%;">
    <h3><b>INSTALLATION DER PROGRAMME</b></h3>
		<span>BITTE WÄHLEN SIE IN DIESEM SCHRITT IHR GEWÜNSCHTES APPL-PROFIL AUS.</span>
		<!--
    <div class="note">
        <div class="noteHeader"><div class="noteIcon"></div><span>Hinweis</span></div>
        <div class="noteBody">
            The official Arch Installer documentation has more in-depth information regarding <a target="_blank" href="https://archinstaller.readthedocs.io/en/latest/">profiles & templates</a>.
        </div>
    </div>
		-->
		<br>
		<br>
		<br>
		<br>
    <select id="templatelist" size="3" class="flex_grow">

    </select>

    <!--<div class="buttons bottom">
        <button id="save_templates">Installieren</button>
        <button id="skip_templates">Überspringen</button>
    </div>-->
</div>

<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="back_step" class="btn btn-primary btn-lg"
            type="submit">
          Zurück
    </button>
    <button id="save_templates" class="btn btn-primary btn-lg float-right"
            type="submit">
         Weiter
    </button>
</div>
"""

## TODO:
## Needs to be loaded this way, since we can't inject JS into divs etc in the HTML above.
javascript = """

document.querySelector('#save_templates').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/apps',
        'template' : document.querySelector('#templatelist').value
    })
})

document.querySelector('#back_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/vpn',
        'back' : true
    })
})

window.refresh_template_list = () => {
    let templatelist_dropdown = document.querySelector('#templatelist');

    Object.keys(window.templates).forEach((template) => {
        let template_info = window.templates[template];
        let option = document.createElement('option');
        option.value = template;
        // option.innerHTML = template + ' (' + template_info['description'] + ')';
        option.innerHTML = template.replace('_',' ');

        templatelist_dropdown.appendChild(option);
    })
}

window.update_templtes = (data) => {
    if(typeof data['templates'] !== 'undefined') {
        window.templates = data['templates'];
        window.refresh_template_list();
    }
    return true;
}

if(socket.subscriptions('templates') != 2)
    socket.subscribe('templates', update_templtes);

socket.send({'_module' : 'installation_steps/apps', 'templates' : 'refresh'})

"""


def notify_template_started(worker, *args, **kwargs):
    worker.frame.CLIENT_IDENTITY.send({
        'type' : 'notification',
        'source' : 'apps',
        'message' : 'Template is being installed',
        'status' : 'active'
    })

def notify_template_installed(worker, *args, **kwargs):
    worker.frame.CLIENT_IDENTITY.send({
        'type' : 'notification',
        'source' : 'apps',
        'message' : 'Template has been installed.',
        'status' : 'complete'
    })

def install_profile(frame, profile_name, worker, hostname='privastick', *args, **kwargs):
    return session.steps['willkommen'].install_profile(session.information['profiles_cache'][profile_name])

def stub(*args, **kwargs):
    return True

def on_request(frame):
    print(frame.data)
    if '_module' in frame.data and frame.data['_module'] == 'installation_steps/apps':
        if 'back' in frame.data:
            yield {
                'status' : 'success',
                '_modules' : 'apps'
            }
            yield {
                'next' : 'apps',
                'status' : 'success',
                '_modules' : 'usb'
            }
        if 'skip' in frame.data:
            session.steps['profil'] = spawn(frame, stub, dependency='vpn')
            yield {
                '_modules' : 'apps',
                'status' : 'skipped',
                'next' : 'willkommen'
            }
            return

        elif 'templates' in frame.data:
            if frame.data['templates'] == 'refresh':
                ## https://github.com/Torxed/archinstall/tree/master/deployments
                ## document.querySelectorAll('.js-navigation-open') -> item.title
                
                session.information['profiles_cache'] = {}
                for root, folders, files in os.walk('./dependencies/archinstall/profiles/'):
                    for file in files:
                        # extension = os.path.splitext(file)[1]
                        # if extension in ('.json', '.py'):
                        #    session.information['profiles_cache'][file] = os.path.join(root, file)
                        session.information['profiles_cache'][file] = os.path.join(root, file)
                    break

                yield {
                    'status' : 'success',
                    'templates' : session.information['profiles_cache']
                }
        
        elif 'template' in frame.data and frame.data['template'].strip():

            #session.steps['profil'] = spawn(frame, install_profile, profile_name=frame.data['template'], start_callback=notify_template_started, callback=notify_template_installed, dependency='internet')


            if frame.data['template'] == "Windows":
                #mycmd=subprocess.getoutput("bash /usr/share/privastick/scripts/switch-desktop-to-win.sh")
                subprocess.run("/home/privauser/.config/ps-tools/scripts/switch-desktop-to-win.sh", user="privauser")

            
            yield {
                'status' : 'complete',
                'next' : 'usb',
                '_modules' : 'apps' 
            }

        else:
            yield {
                'html' : html,
                'javascript' : javascript,
                '_modules' : 'usb'
            }

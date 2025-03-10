import json
from os.path import isdir, isfile
from collections import OrderedDict as oDict

def on_request(frame):
	if '_module' in frame.data and frame.data['_module'] == 'listModules':
		yield {
			'modules' : oDict({
				'Willkommen' : {'required' : False, 'defaults' : {}},
				'Rechtliches' : {'required' : False, 'defaults' : {}},
				'Internet' : {'required' : False, 'defaults' : {}},
				'VPN' : {'required' : False, 'defaults' : {}},
				#'Harddrive' : {'required' : True, 'defaults' : {}},
				#'Encryption' : {'required' : True, 'defaults' : {}},
				#'Mirrors' : {'required' : True, 'defaults' : {}},
				#'Arch Linux' : {'required' : False, 'defaults' : {}},
				#'Language' : {'required' : False, 'defaults' : {}},
				#'Apps' : {'required' : False, 'defaults' : {}},
				'Finalisieren' : {'required' : False, 'defaults' : {}},
				#'Profiles' : {'required' : False, 'defaults' : {}},
				#'Applications' : {'required' : False, 'defaults' : {}},
				#'Accounts' : {'required' : False, 'defaults' : {}},
				#'AUR Packages' : {'required' : False, 'defaults' : {}},
			}),
			'_modules' : 'listModules'
		}

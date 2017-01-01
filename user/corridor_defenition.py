import logging
import rooms.roomloader as roomloader

from constants import *

from localizations import locale_manager

logger = logging.getLogger()

def open_corridor(self, reply):
	if self.state == 'room':
		for item in self.get_items():
			item.on_corridor(self, reply)

	self.state = 'corridor'
	reply(self.get_stats())

	buttons = [ 
		locale_manager.get('corridor.open_next_door', self.lang), 
		locale_manager.get('corridor.player_characteristics', self.lang)#, locale_manager.get('JOIN_TORNAMENT', self.lang)
	]

#	if not self.get_variable('halloween_visited', False) and self.rooms_pack == 'default':
#		buttons.append('Хеллуин!')

	if self.has_item('sign'):
		buttons.append(locale_manager.get('corridor.use_sign', self.lang))

	levels_acts = [ ]
	if self.get_next_level() is not None:
		levels_acts.append(locale_manager.get('corridor.go_down', self.lang))

	if self.get_prev_level() is not None:
		levels_acts.append(locale_manager.get('corridor.go_up', self.lang))

	if len(levels_acts) > 0:
		buttons.append(levels_acts)

	if not self.prayed:
		buttons.append(locale_manager.get('corridor.pray_to_god', self.lang))

	if not self.visited_shop:
		buttons.append(locale_manager.get('corridor.open_shop', self.lang))

	if self.race == RAT_RACE:
		buttons.append(locale_manager.get('corridor.die', self.lang))

	if len(self.items) > 0:
		buttons.append(locale_manager.get('corridor.show_inventory', self.lang))

	buttons.append(locale_manager.get('corridor.other', self.lang))

	reply(locale_manager.get('corridor.what_will_we_do', self.lang), buttons)

def corridor(self, reply, text):
	if self.has_tag('wet'):
		self.remove_tag('wet')
	if self.has_tag('wet_enemy'):
		self.remove_tag('wet_enemy')

	if text == locale_manager.get('corridor.open_next_door', self.lang):
		self.open_room(reply)
	elif text == locale_manager.get('corridor.use_sign', self.lang):
		self.open_room(reply, 'special', 'sign')
	elif text == locale_manager.get('corridor.pray_to_god', self.lang):
		self.pray(reply)
	elif text == locale_manager.get('corridor.open_shop', self.lang):
		self.open_shop(reply)
	elif text == locale_manager.get('corridor.show_inventory', self.lang):
		self.inventory_page = 0
		self.open_inventory(reply)
	elif text == locale_manager.get('corridor.player_characteristics', self.lang):
		self.show_characteristics(reply)
#	elif text == 'Хеллуин!' and not self.get_variable('halloween_visited', False):
#		self.open_room(reply, 'special', 'helloween_shop')
#		self.set_variable('halloween_visited', True)
	elif text == locale_manager.get('corridor.die', self.lang):
		reply(locale_manager.get('corridor.died', self.lang), photo='BQADAgAD5wgAAmrZzgcHFvPa24KvDwI')
		self.death(reply, reason=locale_manager.get('corridor.suicide', self.lang))
	elif text == locale_manager.get('corridor.join_tornament', self.lang):
		self.open_room(reply, 'usual', 'cesar')
	elif self.get_prev_level() is not None and text == locale_manager.get('corridor.go_up', self.lang):
		self.level = self.get_prev_level()
		reply(locale_manager.get('corridor.died', self.lang))

		msg = ''
		for ind, name in enumerate(roomloader.get_level_rooms(self, self.level)):
			msg += '{0}. {1}\n'.format(ind + 1, name)

		reply(msg)

		self.open_corridor(reply)
	elif self.get_next_level() is not None and text == locale_manager.get('corridor.go_down', self.lang):
		self.level = self.get_next_level()
		reply(locale_manager.get('corridor.went_down', self.lang))

		msg = ''
		for ind, name in enumerate(roomloader.get_level_rooms(self, self.level)):
			msg += '{0}. {1}\n'.format(ind + 1, name)

		reply(msg)

		self.open_corridor(reply)
	elif text == locale_manager.get('corridor.other', self.lang):
		self.open_other(reply)
	else:
		self.open_corridor(reply)

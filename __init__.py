from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.parse import match_one, normalize, extract_duration

from mycroft.util.log import getLogger
from ouimeaux.environment import Environment


__author__ = 'cjk8zb'

LOG = getLogger(__name__)

class WemoOutletSkill(MycroftSkill):

    def __init__(self):
        super(WemoOutletSkill, self).__init__(name="WemoOutletSkill")
        env = Environment(self.on_switch, self.on_motion)
        env.start()
        env.discover(seconds=3)

    @intent_file_handler('change_state.intent')
    def handle_change_state_intent(self, message):
        LOG.info("Change state")
        LOG.info(message.data)
        match, confidence = match_one(message.data['state'], ['on', 'off'])
        LOG.info(match)
        LOG.info(confidence)
        if confidence < 0.5:
            return

        button_state = self.switch.get_state()

        if (match == 'on' and button_state == 1) or (match == 'off' and button_state == 0):
            self.speak_dialog("already.set", data={"state": match})
            return

        self.speak('Turning the oven ' + match)
        new_state = 1 if button_state == 0 else 0
        self.switch.set_state(new_state)
        self.speak_dialog("success", data={"state": 'off' if new_state == 0 else 'on'})

    @intent_file_handler('running.intent')
    def handle_running_intent(self, message):
        LOG.info("running intent")
        LOG.info(message.data)
        self.speak_dialog("light.is", data={
            "answer": 'no' if self.switch.get_state() == 0 else 'yes'
            "state": 'off' if self.switch.get_state() == 0 else 'on'
        })

    def on_switch(self, switch):
        print("Switch found!", switch.name)
        if switch.name != 'Outlet':
            return
        self.switch = switch
        button_state = self.switch.get_state()
        print("State:", button_state)

        # new_state = 1 if button_state == 0 else 0
        # switch.set_state(new_state)
        # switch.explain()


    def on_motion(self, motion):
        print("Motion found!", motion.name)


def create_skill():
    return WemoOutletSkill()

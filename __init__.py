# -*- coding: utf-8 -*-
from os.path import dirname, abspath
import sys
import requests
import json
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

sys.path.append(abspath(dirname(__file__)))

from adapt.intent import IntentBuilder
try:
    from mycroft.skills.core import MycroftSkill
except:
    class MycroftSkill:
        pass

__author__ = 'BlackGame'


class GPIO_ControlSkill(MycroftSkill):

    def __init__(self):
        GPIO.output(11,self.on_led_change)
        GPIO.output(12,self.on_led_change)
        GPIO.output(15,self.on_buzzer_change)
        GPIO.output(16,self.on_buzzer_change)
        super(GPIO_ControlSkill, self).__init__(name="GPIO_ControlSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        command_intent = IntentBuilder("IoCommandIntent").require("command").require("ioobject").optionally("ioparam").build()

        self.register_intent(command_intent, self.handle_command_intent)

    def on_led_change(self):
        self.speak("Led is %s" % ledstatus)

    def on_buzzer_change(self):
        self.speak("Buzzer is %s" % buzzerstatus)

    def handle_command_intent(self, message):
        elif message.data["command"].upper() == "TURN":
            if message.data["ioobject"].upper() == "LED":
                if "ioparam" in message.data:
                    if message.data["ioparam"].upper() == "ON":
                        GPIO.output(11,True)
                        GPIO.output(12,True)
                        ledstatus = "On"
                    elif message.data["ioparam"].upper() == "OFF":
                        GPIO.output(11,False)
                        GPIO.output(12,False)
                        ledstatus = "Off"
                else:
                    self.speak_dialog("ipparamrequired")
            if message.data["ioobject"].upper() == "BUZZER":
                if "ioparam" in message.data:
                    if message.data["ioparam"].upper() == "ON":
                        GPIO.output(15,True)
                        GPIO.output(16,True)
                        buzzerstatus = "On"
                    elif message.data["ioparam"].upper() == "OFF":
                        GPIO.output(15,False)
                        GPIO.output(16,False)
                        buzzerstatus = "Off"
                else:
                    self.speak_dialog("ipparamrequired")

def create_skill():
    return GPIO_ControlSkill()

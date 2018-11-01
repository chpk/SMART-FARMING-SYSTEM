# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 02:02:21 2018

@author: Premith Kumar
"""

from twilio.rest import Client
client = Client("ACb1568a6b86c5d19e2cf52e1e63fba93a", "ef3af3a7080398a696f40180034fc3a5")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="9989773443", 
                       from_="9996597934", 
                       body="Hello from Python!")
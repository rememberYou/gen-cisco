from src.scripter import *

SWITCH_PATH = "src/templates/switch/"

class Switch(Scripter):
    name="switch"
    possible_configs=["basic", "etherchannel", "spanning-tree"]
    templates_path=SWITCH_PATH

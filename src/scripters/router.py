from src.scripter import *

ROUTER_PATH = "src/templates/router/"

class Router(Scripter):
    name="router"
    possible_configs = ['basic', 'eigrp', 'hsrp', 'ospf', 'ssh']
    templates_path = ROUTER_PATH

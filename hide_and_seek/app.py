from .ui.game import Game
from .utils.opt import Opt

import yaml
import os


def load_config(level):
    path = "./configs/level_{}.yaml".format(level)
    opt = yaml.load(open(path, "r"), yaml.Loader)
    opt["map"] = os.path.join(opt["map_dir"], "map{}.txt".format(level))
    return opt


def run():
    args = Opt().parse()
    opt = load_config(args.level)
    Game(opt).run()

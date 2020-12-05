import argparse
import os

class Opt():
    def __init__(self):
        parser = argparse.ArgumentParser(description="Hide and Seek simulator")

        parser.add_argument('--level', type=int, required=True, help="""Choose your level (1/2/3/4)""", choices=[1, 2, 3, 4])
        self.parser = parser
    
    def parse(self):
        self.opt = self.parser.parse_args()
        return self.opt


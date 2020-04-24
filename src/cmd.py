from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import clear,set_title
from prompt_toolkit.output.color_depth import ColorDepth
from pygments.lexers.sql import SqlLexer


from playsound import playsound
from mwapi import MWapi
from sc import SC
from utils import try_deco, style, print_f
from wc import wc_data
import os

# The text.

# print_formatted_text(text, style=style)

sql_completer = WordCompleter(wc_data, ignore_case=True)

logo_arr = [
("class:comp", "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"),
("class:comp", "::::::::::::'##::::'##::'#######:::'######::::::::'##::::::::::'#####:::::::::::::::"),
("class:comp", ":::::::::::: ##:::: ##:'##.... ##:'##... ##:::::'####:::::::::'##.. ##::::::::::::::"),
("class:comp", ":::::::::::: ##:::: ##: ##:::: ##: ##:::..::::::.. ##::::::::'##:::: ##:::::::::::::"),
("class:comp", ":::::::::::: ##:::: ##: ##:::: ##: ##::::::::::::: ##:::::::: ##:::: ##:::::::::::::"),
("class:comp", "::::::::::::. ##:: ##:: ##:::: ##: ##::::::::::::: ##:::::::: ##:::: ##:::::::::::::"),
("class:comp", ":::::::::::::. ## ##::: ##:::: ##: ##::: ##::::::: ##:::'###:. ##:: ##::::::::::::::"),
("class:comp", "::::::::::::::. ###::::. #######::. ######::::::'######: ###::. #####:::::::::::::::"),
("class:comp", ":::::::::::::::...::::::.......::::......:::::::......::...::::.....::::::::::::::::"),
]

class Prompt:
    
    def __init__(self):
        self.sc = SC()
        self.mwapi = MWapi()
        self.temp_file = "temp.wav"
        self.session =  PromptSession(PygmentsLexer(SqlLexer), completer=sql_completer, style=style, color_depth=ColorDepth.TRUE_COLOR)
        set_title("voc 1.0")
        print_f([('class:comp', '::::::::::::::::::::::Welcome to use xiaoda dictionary voc 1.0.:::::::::::::::::::::')])
        for each in logo_arr: print_f([each])
        print_f([('class:comp', ':::::::::::::::::::::::::::::Type a word to look up now!::::::::::::::::::::::::::::')])
    

    @try_deco
    def func(self, word):
        # print(word)
        if not self.sc.check(word.strip()):
            return
        self.mwapi.lookup(word.strip())
        playsound(self.temp_file)
        os.remove(self.temp_file)

    def run(self):
        while True:
            try:
                text = self.session.prompt('> ')
                if text.strip() == "*":
                    clear()
                else:
                    self.func(text)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        print('GoodBye!')

if __name__ == '__main__':
    prompt = Prompt()
    prompt.run()
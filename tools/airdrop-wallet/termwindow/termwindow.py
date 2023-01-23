
import sys
import threading
import time
from queue import Queue

from colorama import Fore, Back, Style, init, Cursor
init(autoreset=True)

from termwindow.getch import getch

#from shadowui.windowbase import WindowBase
#from shadowui.section import Section
import shadowui

# Used to signal main loop continue
class InputUsedContinueLoop(Exception): pass
# Used to signal main loop exit
class ProgramExit(Exception): pass
# Used to signal back to previous menu level
class ProgramBack(Exception): pass

class UiColor:
    bg_dark = Back.BLACK
    bg_medium = Back.BLUE
    bg_light = Back.CYAN
    bg_accent = Back.LIGHTCYAN_EX
    bg_alert = Back.RED
    text_bold = Fore.LIGHTWHITE_EX
    text_normal = Fore.WHITE
    text_faded = Fore.BLACK
    text_accent = Fore.LIGHTCYAN_EX
    text_alert = Fore.LIGHTRED_EX
    text_as_bg = Fore.BLACK
Color = UiColor()


class TerminalWindow(shadowui.WindowBase):
    
    input_queue = Queue()
    menu_tools = {}
    at_tools = {}

    def __init__(self, name: str, sub_sections: list = None) -> None:
        super().__init__(name, sub_sections)
    
    def add_menu_tool(self, tool: object):
        self.menu_tools[(tool.short,tool.long)]=tool

    def add_tool(self, tool: object):
        # Check that tool keywords are not used by menu level commands or other tool commands
        for s,l in self.menu_tools | self.at_tools:
            if tool.short == s:
                raise ValueError("shorthand already in use by "+s+" "+l)
            if tool.long == l:
                raise ValueError("tool long keyword already in use by "+s+" "+l)
        self.at_tools[(tool.short,tool.long)]=tool
     
    def open(self):
        self.init()
        self.clear()

        self.clear(Color.bg_dark, Rect(1,1,80,1))
        self.clear(Color.bg_medium, Rect(1,2,80,4))

        self.text(1, 1, ' '+ self.name+' ', Color.text_bold, Color.bg_dark)
        
        self.text(8,3,Color.text_normal + 'Type ' + Color.text_bold + 'help' + Color.text_normal +' for available commands.',back_color=Color.bg_light)
        self.text(8,4,'Use Ctrl-C anytime to abort current command.',Color.text_faded, Color.bg_light)

        self.text(70,2,' ▓█░   ',Color.text_as_bg, Color.bg_accent)
        self.text(70,3,' █  ░▒ ',Color.text_as_bg, Color.bg_accent)
        self.text(70,4,' ▒░  █ ',Color.text_as_bg, Color.bg_accent)
        self.text(70,5,'   ░█▓ ',Color.text_as_bg, Color.bg_accent)


        self.clear(Color.bg_dark, Rect(1,6,80,1))
        self.text(1,6,Color.text_accent + Color.bg_dark+'SW>')

        self.add_menu_tool(ExitCommand())
        self.add_menu_tool(BackCommand())
        self.add_menu_tool(HelpCommand())

        current_tool = None
        user_input=""
        last_update = time.time()

        while True:
            try:
                time.sleep(0.1) # limit framerate
                # if time.time()-last_update>0.5:
                #     sys.stdout.write(".")
                #     sys.stdout.flush()
                #     last_update = time.time()

                if not self.input_queue.empty():
                    k = self.input_queue.get()
                    print('\n'+k+'\n'+str(bytes(k,'utf-8')))
                    if k == '\x03':
                        raise KeyboardInterrupt
                    user_input+=k

                current_tool_str = ""
                if current_tool:
                    current_tool_str = current_tool.long+'>'
                self.clear(Color.bg_dark, Rect(1,6,80,1))
                self.text(1,6,Color.text_accent + Color.bg_dark+'SW>'+current_tool_str+user_input)
                try:
                    input_words = user_input.split(" ")
                    for (short,long),tool in self.menu_tools.items():
                        if input_words[0].casefold() == short or input_words[0].casefold() == long:
                            print('\33[2K\r> '+long)
                            self.menu_tools[(short,long)](*input_words[1:])
                            raise InputUsedContinueLoop
                    if not current_tool:
                        for (short,long),tool in self.at_tools.items():
                            if input_words[0].casefold() == short or input_words[0].casefold() == long:
                                current_tool = tool
                                print('\33[2K\r>>> '+long)
                                self.at_tools[(short,long)](*input_words[1:])
                    else:
                        #reroute input to current tool
                        current_tool(*input_words)
                except InputUsedContinueLoop:
                    pass
                except KeyboardInterrupt:
                    if current_tool:
                        BackCommand()()
                    else:
                        ExitCommand()()
            #except KeyboardInterrupt:
            #    pass
            except ProgramBack:
                current_tool = None
            except ProgramExit:
                print(Fore.LIGHTBLACK_EX + 'Normal program exit')
                exit()
            except Exception as e:
                print("Unhandled exception")
                raise


    """Initialize terminal view"""
    def init(self):
        #set title
        print('\033]2;'+self.name+'\a')
        # Pre-fill with empty lines
        for n in range(1,25):
            print("")
        #reset cursor position
        print(Cursor.POS(1,1)+"", end='')
        
        input_thread = threading.Thread(target=add_input, args=(self.input_queue,))
        input_thread.daemon = True
        input_thread.start()

    """Empty terminal view"""
    def clear(self,bg_color = Back.RESET, rect = None, ):
        if rect:
            for y in range(0, rect.h):
                self.text(rect.x,rect.y+y,' '*rect.w,Fore.RESET, bg_color)
                    
        else:
            print(bg_color+'\033[2J',end='') #clear whole screen

    """Print text at specified position"""
    def text(self,x,y,text,fore_color=Fore.RESET,back_color=Back.RESET):
        print(Cursor.POS(x,y)+fore_color+back_color+text, end='')

    """Empty terminal view"""
    def cursor_pos(self,x,y):
        print(Cursor.POS(x,y)+"", end='')



def add_input(input_queue):
    while True:
        k = getch()
        if k:
            input_queue.put(k)

class Rect:
    x = 1
    y = 1
    w = 1
    h = 1
    def __init__(self,x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        

class ExitCommand:
    short = 'x'
    long = 'exit'
    def __call__(self,*args):
        if prompt_yes_no("Exit?"):
            raise ProgramExit

class BackCommand:
    short = 'b'
    long = 'back'
    def __call__(self,*args):
        raise ProgramBack

class HelpCommand:
    short = 'h'
    long = 'help'
    help = 'Displays context sensitive help.'
    def __call__(self,*args):
        if len(args)>0:
            for (short,long),tool in self.menu_tools.items()|self.at_tools.items():
                if args[0].casefold() == short or args[0].casefold() == long:
                    try:
                        print("\tcommand:\t"+tool.long)
                        print("\tshortcut:\t"+tool.short)
                        print(tool.help)
                        print(tool.help_long)
                    except AttributeError:
                        pass
            return

        print("Commands available everywhere:")
        for (short,long),tool in self.menu_tools.items():
            print('\t'+short+' - '+long+'\t',end='')
            try:
                print(tool.help)
            except AttributeError:
                print("")
        print("Tools:")
        for (short,long),tool in self.at_tools.items():
            print('\t'+short+' - '+long+'\t',end='')
            try:
                print(tool.help)
            except AttributeError:
                print("")
        print("\nUse help <tool> for more help.\n")


"""Prompts an yes or no input from user."""
def prompt_yes_no(prompt: str) -> bool:
    print(prompt+ "(y/n) > ", end='')
    user_input = input()
    print(Cursor.UP(1), end='')
    match user_input: 
        case 'Y'|'y'|'Yes'|'yes':
            return True
    return False

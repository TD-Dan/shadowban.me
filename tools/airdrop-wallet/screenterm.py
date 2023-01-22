from colorama import Fore, Back, Style, init, Cursor
init(autoreset=True)


from screen import Screen

# Used to signal main loop continue
class InputUsedContinueLoop(Exception): pass
# Used to signal main loop exit
class ProgramExit(Exception): pass
# Used to signal back to previous menu level
class ProgramBack(Exception): pass

class TerminalScreen(Screen):
    
    menu_tools = {}
    at_tools = {}

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
        
        print('\033[2J',end='') #clear screen
        
        print(Back.WHITE + Fore.BLACK + ' AIRDROP TOOL v.0.1.1 ')
        print('\nType ' + Fore.LIGHTWHITE_EX + 'help' + Fore.RESET +' for available commands.\nUse Ctrl-C anytime to abort current command.\n')


        self.add_menu_tool(ExitCommand())
        self.add_menu_tool(BackCommand())
        self.add_menu_tool(HelpCommand())

        current_tool = None

        while True:
            try:            
                
                print('\033[2K') #print empty line to avoid screen jumping
                print(Cursor.UP(1)+"", end='')
                current_tool_str = ""
                if current_tool:
                    current_tool_str = Back.GREEN+current_tool.long+'>'+Back.RESET
                print('\33[2K\r'+Back.LIGHTBLACK_EX+Fore.BLACK+'A-T>'+current_tool_str+Fore.RESET+Back.RESET, end='') #\33[2K = erase line, \r = return to line beginning
                try:
                    user_input = input()
                    print(Cursor.UP(1)+"", end='')
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
            except KeyboardInterrupt:
                pass
            except ProgramBack:
                current_tool = None
            except ProgramExit:
                print(Fore.LIGHTBLACK_EX + 'Normal program exit')
                exit()
            except Exception as e:
                print("Unhandled exception")
                raise


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
            for (short,long),tool in menu_tools.items()|at_tools.items():
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
        for (short,long),tool in menu_tools.items():
            print('\t'+short+' - '+long+'\t',end='')
            try:
                print(tool.help)
            except AttributeError:
                print("")
        print("Tools:")
        for (short,long),tool in at_tools.items():
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

#!/usr/bin/env python3
import os
import sys
import time
import random
import datetime
import platform
import shutil
import json
from colorama import  Fore
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{Colors.ENDC}"

class PyOS:
    def __init__(self):
        self.running = True
        self.username = os.getlogin()
        self.current_dir = os.getcwd()
        self.commands = {}
        self.notes = []
        self.todos = []
        self.config_file = "pyos_config.json"
        self.config = {
            "theme": "default",
            "prompt": "KisueerOS > ",
            "welcome_message": "Welcome to KisueerOS! Type 'help' to see available commands."
        }
        
        # Register all commands
        self.register_commands()
        
        # Load configuration if it exists
        self.load_config()
        
    def register_commands(self):
        # Basic commands
        self.register_command("help", self.cmd_help, "Display help information for available commands")
        self.register_command("exit", self.cmd_exit, "Exit KisueerOS")
        self.register_command("clear", self.cmd_clear, "Clear the screen")
        
        # System info commands
        self.register_command("sysinfo", self.cmd_sysinfo, "Display system information")
        self.register_command("time", self.cmd_time, "Display current time")
        self.register_command("date", self.cmd_date, "Display current date")
        
        # File system commands
        self.register_command("ls", self.cmd_ls, "List files in current directory")
        self.register_command("cd", self.cmd_cd, "Change directory")
        self.register_command("pwd", self.cmd_pwd, "Print working directory")
        self.register_command("mkdir", self.cmd_mkdir, "Create a new directory")
        self.register_command("touch", self.cmd_touch, "Create a new empty file")
        self.register_command("cat", self.cmd_cat, "Display content of a file")
        self.register_command("rm", self.cmd_rm, "Remove file or directory")
        
        # User commands
        self.register_command("whoami", self.cmd_whoami, "Display current username")
        self.register_command("setuser", self.cmd_setuser, "Change username")
        
        # Fun commands
        self.register_command("echo", self.cmd_echo, "Echo text back to the terminal")
        self.register_command("fortune", self.cmd_fortune, "Get a random fortune")
        self.register_command("flip", self.cmd_flip, "Flip a coin")
        self.register_command("dice", self.cmd_dice, "Roll a dice (default: 6-sided)")
        self.register_command("banner", self.cmd_banner, "Display a banner")
        self.register_command("ddos", self.cmd_ddos, "DDOS an internet addres")
        self.register_command("device", self.cmd_device, "Scan for devices around you and execute commands")
        
        # Note and todo commands
        self.register_command("note", self.cmd_note, "Add a note")
        self.register_command("notes", self.cmd_notes, "List all notes")
        self.register_command("todo", self.cmd_todo, "Add a todo item")
        self.register_command("todos", self.cmd_todos, "List all todo items")
        self.register_command("done", self.cmd_done, "Mark a todo item as done")
        
        # Configuration commands
        self.register_command("theme", self.cmd_theme, "Change the theme")
        self.register_command("setprompt", self.cmd_setprompt, "Change the prompt string")
        self.register_command("config", self.cmd_config, "Display current configuration")
        
        # Advanced commands
        self.register_command("calc", self.cmd_calc, "Simple calculator")
        self.register_command("countdown", self.cmd_countdown, "Start a countdown timer")
        self.register_command("weather", self.cmd_weather, "Display simulated weather")
        
    def register_command(self, name, function, description):
        """Register a new command"""
        self.commands[name] = {
            "function": function,
            "description": description
        }
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def run(self):
        """Run the PyOS main loop"""
        print(self.config["welcome_message"])
        
        while self.running:
            try:
                user_input = input(f"{Colors.GREEN}┌──{Colors.BLUE}({self.username}㉿Kisueer{Colors.GREEN})-[{Fore.RESET}~{Colors.GREEN}]\n└─{Colors.BLUE}${Fore.RESET} ")
                self.parse_input(user_input)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit PyOS.")
            except Exception as e:
                print(f"Error: {e}")
    
    def parse_input(self, user_input):
        """Parse and execute user input"""
        if not user_input.strip():
            return
            
        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]
        
        if command in self.commands:
            self.commands[command]["function"](args)
        else:
            print(f"Command not found: {command}")
            print("Type 'help' to see available commands.")
    
    def get_display_path(self):
        """Get a shortened display path for the prompt"""
        home = os.path.expanduser("~")
        if self.current_dir.startswith(home):
            return "~" + self.current_dir[len(home):]
        return self.current_dir
    
    # Command implementations
    def cmd_help(self, args):
        """Display help information"""
        if args:
            # Help for specific command
            cmd = args[0].lower()
            if cmd in self.commands:
                print(f"{cmd}: {self.commands[cmd]['description']}")
            else:
                print(f"Command not found: {cmd}")
        else:
            # General help
            print("Available commands:")
            for cmd_name in sorted(self.commands.keys()):
                print(f"  {cmd_name:12} - {self.commands[cmd_name]['description']}")
            print("\nType 'help <command>' for more information on a specific command.")
    
    def cmd_exit(self, args):
        """Exit the shell"""
        print("Exiting PyOS. Goodbye!")
        self.running = False
    
    def cmd_clear(self, args):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cmd_sysinfo(self, args):
        """Display system information"""
        print("=== System Information ===")
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")
        print(f"Processor: {platform.processor()}")
        print(f"Machine: {platform.machine()}")
        print(f"Node: {platform.node()}")
        
        # Memory info
        if hasattr(os, 'statvfs'):  # Unix/Linux
            statvfs = os.statvfs(self.current_dir)
            disk_size = statvfs.f_frsize * statvfs.f_blocks
            disk_free = statvfs.f_frsize * statvfs.f_bfree
            print(f"Disk total: {self.format_size(disk_size)}")
            print(f"Disk free: {self.format_size(disk_free)}")
    
    def format_size(self, size_bytes):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def cmd_time(self, args):
        """Display current time"""
        print(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    def cmd_date(self, args):
        """Display current date"""
        print(f"Current date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    
    def cmd_ls(self, args):
        """List files in current directory"""
        try:
            path = " ".join(args) if args else self.current_dir
            if not os.path.isabs(path):
                path = os.path.join(self.current_dir, path)
                
            if os.path.isdir(path):
                files = os.listdir(path)
                for f in sorted(files):
                    full_path = os.path.join(path, f)
                    if os.path.isdir(full_path):
                        print(f"\033[1;34m{f}/\033[0m")  # Blue for directories
                    elif os.access(full_path, os.X_OK):
                        print(f"\033[1;32m{f}*\033[0m")  # Green for executables
                    else:
                        print(f)
            else:
                print(f"Not a directory: {path}")
        except Exception as e:
            print(f"Error: {e}")
    
    def cmd_cd(self, args):
        """Change directory"""
        if not args:
            # Default to home directory
            new_dir = os.path.expanduser("~")
        else:
            new_dir = " ".join(args)
            
            # Handle relative paths
            if not os.path.isabs(new_dir):
                new_dir = os.path.join(self.current_dir, new_dir)
            
            # Normalize path
            new_dir = os.path.normpath(new_dir)
            
        if os.path.isdir(new_dir):
            self.current_dir = new_dir
        else:
            print(f"Directory not found: {new_dir}")
    
    def cmd_pwd(self, args):
        """Print working directory"""
        print(self.current_dir)
    
    def cmd_mkdir(self, args):
        """Create a new directory"""
        if not args:
            print("Usage: mkdir <directory_name>")
            return
            
        dir_name = " ".join(args)
        if not os.path.isabs(dir_name):
            dir_name = os.path.join(self.current_dir, dir_name)
            
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"Directory created: {dir_name}")
        except Exception as e:
            print(f"Error creating directory: {e}")
    
    def cmd_touch(self, args):
        """Create a new empty file"""
        if not args:
            print("Usage: touch <file_name>")
            return
            
        file_name = " ".join(args)
        if not os.path.isabs(file_name):
            file_name = os.path.join(self.current_dir, file_name)
            
        try:
            Path(file_name).touch()
            print(f"File created: {file_name}")
        except Exception as e:
            print(f"Error creating file: {e}")

    def cmd_ddos(self, args):
        bot_count = random.randint(120, 240)
        banner = f"""
        {Colors.CYAN}╔══════════════════════════════════════════════════╗
        ║{Colors.RED}{Colors.BOLD}                                                  {Colors.CYAN}║
        ║{Colors.RED}{Colors.BOLD}   WRAITH DDOS ATTACK v2.1.7                      {Colors.CYAN}║
        ║{Colors.RED}{Colors.BOLD}                                                  {Colors.CYAN}║
        ║{Colors.GREEN}   BOTNET ONLINE: {bot_count} BOTS                        {Colors.CYAN}║
        ║{Colors.YELLOW}   COMMAND AND CONTROL: ACTIVE                    {Colors.CYAN}║
        ║{Colors.RED}{Colors.BOLD}   C2 SERVER: 102.1*.***.1                        {Colors.CYAN}║
        ╚══════════════════════════════════════════════════╝{Colors.ENDC}    
        """
        print(banner)
    
    def cmd_cat(self, args):
        """Display content of a file"""
        if not args:
            print("Usage: cat <file_name>")
            return
            
        file_name = " ".join(args)
        if not os.path.isabs(file_name):
            file_name = os.path.join(self.current_dir, file_name)
            
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    print(f.read())
            else:
                print(f"File not found: {file_name}")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def cmd_rm(self, args):
        """Remove file or directory"""
        if not args:
            print("Usage: rm <file_or_directory>")
            return
            
        path = " ".join(args)
        if not os.path.isabs(path):
            path = os.path.join(self.current_dir, path)
            
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Directory removed: {path}")
            elif os.path.exists(path):
                os.remove(path)
                print(f"File removed: {path}")
            else:
                print(f"No such file or directory: {path}")
        except Exception as e:
            print(f"Error removing: {e}")
    
    def cmd_whoami(self, args):
        """Display current username"""
        print(self.username)
    
    def cmd_setuser(self, args):
        """Change username"""
        if not args:
            print("Usage: setuser <new_username>")
            return
            
        self.username = args[0]
        print(f"Username changed to: {self.username}")

    def cmd_device(self, args):
        print("Scanning for devices around")
        print("Received connection from 27 devices\n")
        print("""
1. Darius's Android Phone (DB)
2. Tiby's Iphone Phone (DB)
3. Mihai's Android Phone (DB)
4. Mihnea's Android Phone (DB)
5. David's Iphone Phone (DB)
6. Radu's Android Phone (DB)
7. Yasmina's Android Phone (DB)
8. Unknown Android Phone
9. Unknown Android Phone
10. Unknown Android Phone
11. Unknown Android Phone
12. Natalia Android Phone
13. Unknown Android Phone
14. Unknown Android Phone
15. Unknown Android Phone
16. Unknown Android Phone
17. Unknown Android Phone
18. Unknown Android Phone
19. Unknown Android Phone
20. Unknown Android Phone
21. Unknown Iphone Phone
23. Unknown Iphone Phone
24. Unknown Iphone Phone
25. Asus Router (Router DB)
26. HP Built-In PC
27. Unknown Projector\n""")
        choice = input(f"{Colors.BLUE}Select a device (1-27):{Fore.RESET} ")

        if choice == "1":
            self.cmd_clear
            print("""
Options for Android                  

1. Run Android Crash Exploit
2. Run Android Stress Exploit
3. Bruteforce pw
4. BLE Spam\n""")
            choice2 = input(f"{Colors.BLUE}Choice:{Fore.RESET} ")

        if choice == "25":
            self.cmd_clear
            print("""
Options for Routers                  

1. Bruteforce pw
2. Asus Stress Exploit
3. Launch DDOS Attack (183 bots)
4. Get IP Connection\n""")
            choice2 = input(f"{Colors.BLUE}Choice:{Fore.RESET} ")

        if choice == "26":
            self.cmd_clear
            print("""
Options for PC                  

1. Launch DDOS Attack (183 bots)
2. Bruceforce pw
3. BLE Spam\n""")
            choice2 = input(f"{Colors.BLUE}Choice:{Fore.RESET} ")
            
        if choice == "27":
            self.cmd_clear
            print("""
Options for Projector                  

1. IR Remote\n""")
            choice2 = input(f"{Colors.BLUE}Choice:{Fore.RESET} ")

        else:
            self.cmd_clear
            print("""
Option for Android                  
                
1. Run Android Crash Exploit
2. Run Android Stress Exploit
3. Bruteforce pw
4. BLE Spam\n""")
            choice2 = input(f"{Colors.BLUE}Choice:{Fore.RESET} ")


    def cmd_banner(self, args):
        banners = [
        """
          4$$-.                         
           4   ".                                        
           4    ^.                                       
           4     $                                       
           4     'b                                      
           4      "b.                                    
           4        $                                    
           4        $r                                   
           4        $F                                   
-$b========4========$b====*P=-       KisueerOS
           4       *$$F                                  
           4        $$"                                  
           4       .$F                                   
           4       dP                                    
           4      F                                      
           4     @                                       
           4    .                                        
           J. &                                           
           $$

        """,
        """
          /| ________________
O|===|* >____________________>     KisueerOS
          \|
        """,
        """
    ||========================================================================||
    ||                                                                        ||
    ||   K I S U E E R O S   -   THE EDGE OF PERFORMANCE                      ||
    ||________________________________________________________________________||
    ||========================================================================||

        """
    ]
    
        print(random.choice(banners))

    def cmd_echo(self, args):
        """Echo text back to the terminal"""
        print(" ".join(args))
    
    def cmd_fortune(self, args):
        """Get a random fortune"""
        fortunes = [
            "You will have a great day!",
            "Good things come to those who code.",
            "The bugs in your code will soon disappear.",
            "Your next commit will be perfect.",
            "A programmer who breaks something is better than one who never builds.",
            "Today is a good day to learn something new.",
            "Happiness is a bug-free code.",
            "Don't worry about the bugs, they're just features in disguise.",
            "Your code will change the world someday.",
            "The best code is the one that works."
        ]
        print(random.choice(fortunes))
    
    def cmd_flip(self, args):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        print(f"Coin flip: {result}")
    
    def cmd_dice(self, args):
        """Roll a dice"""
        sides = 6
        if args and args[0].isdigit():
            sides = int(args[0])
        
        result = random.randint(1, sides)
        print(f"Dice roll (d{sides}): {result}")
    
    def cmd_note(self, args):
        """Add a note"""
        if not args:
            print("Usage: note <your note text>")
            return
            
        note = " ".join(args)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notes.append({"text": note, "timestamp": timestamp})
        print("Note added!")
    
    def cmd_notes(self, args):
        """List all notes"""
        if not self.notes:
            print("No notes found.")
            return
            
        print("=== Notes ===")
        for i, note in enumerate(self.notes, 1):
            print(f"{i}. [{note['timestamp']}] {note['text']}")
    
    def cmd_todo(self, args):
        """Add a todo item"""
        if not args:
            print("Usage: todo <task description>")
            return
            
        task = " ".join(args)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.todos.append({"task": task, "timestamp": timestamp, "done": False})
        print("Todo added!")
    
    def cmd_todos(self, args):
        """List all todo items"""
        if not self.todos:
            print("No todo items found.")
            return
            
        print("=== Todo List ===")
        for i, todo in enumerate(self.todos, 1):
            status = "[X]" if todo['done'] else "[ ]"
            print(f"{i}. {status} {todo['task']} (Added: {todo['timestamp']})")
    
    def cmd_done(self, args):
        """Mark a todo item as done"""
        if not args or not args[0].isdigit():
            print("Usage: done <todo_number>")
            return
            
        index = int(args[0]) - 1
        if 0 <= index < len(self.todos):
            self.todos[index]['done'] = True
            print(f"Marked todo #{index+1} as done!")
        else:
            print("Invalid todo number.")
    
    def cmd_theme(self, args):
        """Change the theme"""
        themes = ["default", "dark", "light", "colorful"]
        
        if not args:
            print(f"Current theme: {self.config['theme']}")
            print(f"Available themes: {', '.join(themes)}")
            return
            
        theme = args[0].lower()
        if theme in themes:
            self.config['theme'] = theme
            print(f"Theme changed to: {theme}")
            self.save_config()
        else:
            print(f"Unknown theme: {theme}")
            print(f"Available themes: {', '.join(themes)}")
    
    def cmd_setprompt(self, args):
        """Change the prompt string"""
        if not args:
            print(f"Current prompt: {self.config['prompt']}")
            return
            
        new_prompt = " ".join(args)
        self.config['prompt'] = new_prompt
        print(f"Prompt changed to: {new_prompt}")
        self.save_config()
    
    def cmd_config(self, args):
        """Display current configuration"""
        print("=== PyOS Configuration ===")
        for key, value in self.config.items():
            print(f"{key}: {value}")
    
    def cmd_calc(self, args):
        """Simple calculator"""
        if not args:
            print("Usage: calc <expression>")
            return
            
        expr = " ".join(args)
        try:
            # Using eval is generally not safe, but for this simple example it's ok
            # In a real application, you'd want to use a safer evaluation method
            result = eval(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error evaluating expression: {e}")
    
    def cmd_countdown(self, args):
        """Start a countdown timer"""
        if not args or not args[0].isdigit():
            print("Usage: countdown <seconds>")
            return
            
        seconds = int(args[0])
        print(f"Countdown started: {seconds} seconds")
        
        try:
            for i in range(seconds, 0, -1):
                sys.stdout.write(f"\rTime remaining: {i} seconds")
                sys.stdout.flush()
                time.sleep(1)
            print("\nCountdown finished!")
        except KeyboardInterrupt:
            print("\nCountdown interrupted!")
    
    def cmd_weather(self, args):
        """Display simulated weather"""
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy", "Stormy", "Foggy", "Clear"]
        temps = list(range(0, 40))  # 0 to 39 degrees Celsius
        
        condition = random.choice(conditions)
        temp = random.choice(temps)
        humidity = random.randint(30, 90)
        
        print("=== Weather Forecast ===")
        print(f"Condition: {condition}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")


if __name__ == "__main__":
    pyos = PyOS()
    pyos.run()

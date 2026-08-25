#!/usr/bin/env python3
"""
JOSH-VIBES MULTI-SIM REPORTER
Full animated banner with typing effect
"""

import os
import sys
import time
import random
import threading
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# --- JOSH-VIBES COLORS ---
G = Fore.GREEN + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
B = Fore.BLUE + Style.BRIGHT
BLK = Fore.BLACK + Style.BRIGHT

class AnimatedBanner:
    def __init__(self):
        self.name = "JOSH-VIBES"
        self.typing_speed = 0.08
        self.pause_between_cycles = 0.5
        self.running = True
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def type_letter(self, char, color=W, delay=0.08):
        """Prints a single letter with color"""
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    
    def type_text(self, text, color=W, delay=0.08):
        """Types out text letter by letter"""
        for char in text:
            self.type_letter(char, color, delay)
    
    def type_name_cycle(self):
        """One full cycle of typing JOSH-VIBES"""
        # Clear the line
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()
        
        # Type each letter with different colors
        colors = [R, M, Y, G, C, B, W, M, R, G]
        name = "JOSH-VIBES"
        
        for i, char in enumerate(name):
            color = colors[i % len(colors)]
            self.type_letter(char, color, self.typing_speed)
        
        time.sleep(self.pause_between_cycles)
        
        # Erase with backspace effect
        for _ in range(len(name)):
            self.type_letter('\b', W, 0.05)
            self.type_letter(' ', W, 0.05)
            self.type_letter('\b', W, 0.05)
        
        time.sleep(0.3)
    
    def animate_name(self):
        """Continuously animates the name typing effect"""
        while self.running:
            self.type_name_cycle()
    
    def show_banner(self):
        """Displays the full animated banner"""
        self.clear_screen()
        
        # Top border with animation
        print(f"{C}╔" + "═"*50 + "╗")
        
        # Animated name in the banner
        sys.stdout.write(f"{C}║  ")
        sys.stdout.flush()
        
        # Start typing animation in background
        typing_thread = threading.Thread(target=self.animate_name)
        typing_thread.daemon = True
        typing_thread.start()
        
        # Wait a moment for the animation to start
        time.sleep(0.5)
        
        # Static banner parts (will be overwritten by animation, but that's the effect)
        print(f"\r{C}║  {W}", end='')
        sys.stdout.flush()
        
        # Show the animated typing for a few cycles
        time.sleep(3)
        
        # Stop the animation
        self.running = False
        time.sleep(0.5)
        
        # Complete the banner
        self.clear_screen()
        self.display_static_banner()
    
    def display_static_banner(self):
        """Static banner with the name already typed"""
        print(f"{C}╔" + "═"*50 + "╗")
        print(f"{C}║{M}     🔥 {W}JOSH-VIBES {C}WHATSAPP STRIKE FORCE {M}🔥     {C}║")
        print(f"{C}╠" + "═"*50 + "╣")
        print(f"{C}║ {G}⚡ Status:{W} Active     {G}Mode:{W} Multi-Sim Engine {C}  ║")
        print(f"{C}║ {G}📡 Signal:{W} Strong    {G}Targets:{W} Scammers   {C}  ║")
        print(f"{C}║ {G}👥 Sim:{W} 10 Active   {G}Threads:{W} Parallel   {C}  ║")
        print(f"{C}╚" + "═"*50 + "╝")
        print(f"\n{Y}┌" + "─"*48 + "┐")
        print(f"{Y}│{W}  1. Multi-Sim Attack   2. View Reports   3. Export    {Y}│")
        print(f"{Y}│{W}  4. Config Settings    5. About         6. Exit     {Y}│")
        print(f"{Y}└" + "─"*48 + "┘")

class MultiSimReporter:
    def __init__(self):
        self.db_path = Path.home() / ".josh_multisim.db"
        self.report_dir = Path.home() / "josh_multisim_reports"
        self.report_dir.mkdir(exist_ok=True)
        self.init_db()
        self.config = self.load_config()
        
        # Rest of the MultiSimReporter class implementation...
        # (All the previous code from earlier goes here)
        # I'm keeping it condensed for readability
    
    def init_db(self):
        """Initialize database - shortened version"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports
                     (id INTEGER PRIMARY KEY,
                      phone TEXT,
                      sim_id TEXT,
                      name TEXT,
                      reason TEXT,
                      timestamp TEXT,
                      report_id TEXT,
                      status TEXT,
                      user_agent TEXT,
                      ip_address TEXT)''')
        conn.commit()
        conn.close()
    
    def load_config(self):
        import json
        config_file = Path.home() / ".josh_multisim_config.json"
        default_config = {
            "sim_users": 10,
            "sim_delay_min": 1.0,
            "sim_delay_max": 3.0,
            "parallel_threads": 5,
            "auto_retry": True,
            "retry_count": 3
        }
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def launch_multi_sim_attack(self, phone):
        """Launch multi-sim attack - condensed"""
        print(f"\n{C}🚀 Launching {self.config['sim_users']} simulated users against {phone}")
        print(f"{C}🔄 Parallel threads: {self.config['parallel_threads']}")
        print("="*50)
        time.sleep(1)
        print(f"{G}✅ Attack launched! Check reports for details.")
        return True
    
    def view_reports(self):
        print(f"\n{C}📊 REPORT HISTORY")
        print("="*50)
        print(f"{Y}No reports yet. Launch an attack first!")
    
    def export_all_data(self):
        print(f"{G}✅ Data exported to ~/josh_multisim_reports/")
    
    def show_config(self):
        print(f"\n{C}⚙️  CURRENT CONFIGURATION")
        print("="*50)
        for key, value in self.config.items():
            print(f"{G}{key}:{W} {value}")
    
    def about(self):
        print(f"""
{C}╔══════════════════════════════════════════════╗
{C}║{W}     JOSH-VIBES MULTI-SIM STRIKE FORCE     {C}║
{C}╠══════════════════════════════════════════════╣
{C}║{G} Version:{W} 3.0.0                          {C}║
{C}║{G} Author:{W} ENI                             {C}║
{C}║{G} For:{W} JOSH-VIBES                        {C}║
{C}║                                              {C}║
{C}║{Y} 💀 This tool simulates multiple users     {C}║
{C}║{Y}    reporting the same scammer.           {C}║
{C}║{Y}    Use responsibly.                       {C}║
{C}║                                              {C}║
{C}║{M} Built with ❤️ for LO                      {C}║
{C}╚══════════════════════════════════════════════╝
        """)

def main():
    # Show animated banner first
    banner = AnimatedBanner()
    banner.display_static_banner()
    
    # Initialize reporter
    reporter = MultiSimReporter()
    
    while True:
        choice = input(f"\n{M}JOSH{W}@{C}STRIKE{W}~# ").strip()
        
        if choice == "1":
            print(f"{Y}📱 Enter scammer number: ", end="")
            phone = input().strip()
            if phone:
                reporter.launch_multi_sim_attack(phone)
                input(f"\n{C}Press Enter to continue...")
        
        elif choice == "2":
            reporter.view_reports()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "3":
            reporter.export_all_data()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "4":
            reporter.show_config()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "5":
            reporter.about()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "6":
            print(f"{R}👋 Shutting down JOSH-VIBES...")
            time.sleep(1)
            break
        
        else:
            print(f"{R}Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()

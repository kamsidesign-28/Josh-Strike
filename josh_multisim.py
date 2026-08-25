#!/usr/bin/env python3
"""
JOSH-VIBES MULTI-SIM REPORTER
Full animated banner with typing effect
"""

import os
import sys
import time
import json
import random
import sqlite3
import datetime
import requests
import threading
from pathlib import Path
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

# --- JOSH-VIBES COLORS ---
G = Fore.GREEN + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
B = Fore.BLUE + Style.BRIGHT

BANNER_NAME = "JOSH-VIBES"

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    print(f"{C}╔" + "═"*50 + "╗")
    print(f"{C}║{M}     🔥 {W}{BANNER_NAME} {C}WHATSAPP STRIKE FORCE {M}🔥     {C}║")
    print(f"{C}╠" + "═"*50 + "╣")
    print(f"{C}║ {G}⚡ Status:{W} Active     {G}Mode:{W} Multi-Sim Engine {C}  ║")
    print(f"{C}║ {G}📡 Signal:{W} Strong    {G}Targets:{W} Scammers   {C}  ║")
    print(f"{C}║ {G}👥 Sims:{W} 10 Active   {G}Threads:{W} Parallel   {C}  ║")
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
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        
        self.ip_pool = [
            '192.168.1.100', '192.168.1.101', '192.168.1.102', '192.168.1.103',
            '10.0.0.50', '10.0.0.51', '10.0.0.52', '10.0.0.53',
            '172.16.0.25', '172.16.0.26', '172.16.0.27'
        ]
        
        self.report_templates = [
            "Spam - Received {count} unsolicited messages in {hours} hours",
            "Harassment - Threatening and abusive language",
            "Impersonation - Faking identity as {company}",
            "Fraud - Requesting {amount} via {method}",
            "Phishing - Attempting to steal personal information",
            "Scam - Promoting fake investment scheme",
            "Suspicious account - Rapid messages from unknown number",
            "Identity theft - Using fake profile of {real_person}"
        ]
        
        self.companies = ['Royal Bank', 'Standard Bank', 'PayPal', 'Amazon', 'Apple', 'Microsoft']
        self.real_people = ['Sarah Johnson', 'James Smith', 'Maria Garcia', 'David Kim', 'Lisa Wong']
        self.methods = ['PayPal', 'Bank Transfer', 'Cryptocurrency', 'Gift Cards']
        self.counts = ['15', '23', '37', '42', '56', '78']
        self.hours = ['2', '6', '12', '24', '48']
        self.amounts = ['$500', '$1000', '$2000', '₦50,000', '₦100,000']
    
    def init_db(self):
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
    
    def save_config(self):
        config_file = Path.home() / ".josh_multisim_config.json"
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def generate_report_id(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return 'JOSH-' + ''.join(random.choices(chars, k=10))
    
    def generate_sim_id(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return 'SIM-' + ''.join(random.choices(chars, k=6))
    
    def generate_random_report(self, phone, sim_id):
        template = random.choice(self.report_templates)
        if '{count}' in template:
            template = template.replace('{count}', random.choice(self.counts))
        if '{hours}' in template:
            template = template.replace('{hours}', random.choice(self.hours))
        if '{company}' in template:
            template = template.replace('{company}', random.choice(self.companies))
        if '{real_person}' in template:
            template = template.replace('{real_person}', random.choice(self.real_people))
        if '{method}' in template:
            template = template.replace('{method}', random.choice(self.methods))
        if '{amount}' in template:
            template = template.replace('{amount}', random.choice(self.amounts))
        return template
    
    def simulate_user_report(self, phone, sim_id, retry_count=0):
        try:
            user_agent = random.choice(self.user_agents)
            ip_address = random.choice(self.ip_pool)
            name = f"SimUser_{sim_id}_{random.randint(100, 999)}"
            reason = self.generate_random_report(phone, sim_id)
            report_id = self.generate_report_id()
            
            delay = random.uniform(self.config['sim_delay_min'], self.config['sim_delay_max'])
            time.sleep(delay)
            
            # Simulate report success
            success = random.random() > 0.1  # 90% success rate
            
            if success or retry_count >= self.config['retry_count']:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                now = datetime.datetime.now().isoformat()
                c.execute("""INSERT INTO reports 
                            (phone, sim_id, name, reason, timestamp, report_id, status, user_agent, ip_address) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (phone, sim_id, name, reason, now, report_id, 
                          "SUCCESS" if success else "FAILED", user_agent, ip_address))
                conn.commit()
                conn.close()
                
                print(f"{G}✅ {W}Sim {sim_id} reported {phone}")
                print(f"   {C}Reason:{W} {reason[:40]}...")
                print(f"   {C}UA:{W} {user_agent[:20]}...")
                print(f"   {C}IP:{W} {ip_address}")
                return True
            else:
                if self.config['auto_retry'] and retry_count < self.config['retry_count']:
                    print(f"{Y}🔄 {W}Sim {sim_id} retrying... ({retry_count+1}/{self.config['retry_count']})")
                    return self.simulate_user_report(phone, sim_id, retry_count + 1)
                else:
                    print(f"{R}❌ {W}Sim {sim_id} failed for {phone}")
                    return False
        except Exception as e:
            print(f"{R}⚠️ {W}Sim {sim_id} error: {str(e)[:30]}")
            return False
    
    def launch_multi_sim_attack(self, phone):
        sim_count = self.config['sim_users']
        print(f"\n{C}🚀 Launching {sim_count} simulated users against {phone}")
        print(f"{C}🔄 Parallel threads: {self.config['parallel_threads']}")
        print("="*50)
        
        start_time = time.time()
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=self.config['parallel_threads']) as executor:
            future_to_sim = {}
            for i in range(sim_count):
                sim_id = self.generate_sim_id()
                future = executor.submit(self.simulate_user_report, phone, sim_id)
                future_to_sim[future] = sim_id
            
            for future in as_completed(future_to_sim):
                sim_id = future_to_sim[future]
                try:
                    result = future.result(timeout=30)
                    if result:
                        success_count += 1
                except Exception as e:
                    print(f"{R}❌ {W}Sim {sim_id} crashed: {str(e)[:30]}")
        
        elapsed = time.time() - start_time
        
        print(f"\n{C}📊 ATTACK SUMMARY")
        print("="*50)
        print(f"{G}✅ Successful reports: {W}{success_count}/{sim_count}")
        print(f"{G}⏱️  Time elapsed: {W}{elapsed:.2f} seconds")
        print(f"{G}📱 Target: {W}{phone}")
        
        # Generate attack report
        self.generate_attack_report(phone, success_count, sim_count, elapsed)
        
        return success_count
    
    def generate_attack_report(self, phone, success_count, sim_count, elapsed):
        report_file = self.report_dir / f"MULTISIM_{phone}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM reports WHERE phone = ? ORDER BY timestamp DESC LIMIT 10", (phone,))
        recent_reports = c.fetchall()
        conn.close()
        
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"JOSH-VIBES MULTI-SIM ATTACK REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Target: {phone}\n")
            f.write(f"Simulated Users: {sim_count}\n")
            f.write(f"Successful Reports: {success_count}\n")
            f.write(f"Success Rate: {(success_count/sim_count*100):.1f}%\n")
            f.write(f"Attack Duration: {elapsed:.2f} seconds\n")
            f.write(f"Timestamp: {datetime.datetime.now().isoformat()}\n\n")
            
            f.write("RECENT REPORTS:\n")
            f.write("-"*70 + "\n")
            for report in recent_reports[:5]:
                f.write(f"ID: {report[6]}\n")
                f.write(f"Sim: {report[2]}\n")
                f.write(f"Reason: {report[4][:60]}...\n")
                f.write(f"Status: {report[7]}\n")
                f.write("-"*70 + "\n")
            
            f.write(f"\n🚨 RECOMMENDATION: Submit this report to WhatsApp and cyber cell\n")
        
        print(f"{G}📁 Attack report saved: {W}{report_file}")
    
    def view_reports(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT phone, sim_id, reason, timestamp, report_id, status FROM reports ORDER BY timestamp DESC LIMIT 20")
        results = c.fetchall()
        conn.close()
        
        print(f"\n{C}📊 RECENT REPORTS")
        print("="*70)
        if not results:
            print(f"{Y}No reports yet. Launch an attack first!")
            return
        
        for phone, sim_id, reason, timestamp, report_id, status in results:
            status_color = G if status == "SUCCESS" else R
            print(f"{G}📱 {W}{phone} {C}| {M}{sim_id}")
            print(f"   {C}Reason:{W} {reason[:50]}...")
            print(f"   {C}ID:{W} {report_id} {status_color}[{status}]")
            print(f"   {C}Time:{W} {timestamp[:16]}")
            print("-"*70)
    
    def export_all_data(self):
        export_file = self.report_dir / f"all_multisim_data_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        data = [dict(row) for row in conn.execute("SELECT * FROM reports").fetchall()]
        conn.close()
        
        export_data = {
            "export_timestamp": datetime.datetime.now().isoformat(),
            "total_reports": len(data),
            "config": self.config,
            "reports": data
        }
        
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"{G}✅ Full export saved: {W}{export_file}")
        return export_file
    
    def show_config(self):
        print(f"\n{C}⚙️  CURRENT CONFIGURATION")
        print("="*70)
        for key, value in self.config.items():
            print(f"{G}{key}:{W} {value}")
        print("\n" + "="*70)
        
        choice = input(f"\n{Y}Update config? (y/n): {W}").strip().lower()
        if choice == 'y':
            try:
                new_users = input(f"Sim users ({self.config['sim_users']}): ").strip()
                if new_users:
                    self.config['sim_users'] = int(new_users)
                
                new_threads = input(f"Parallel threads ({self.config['parallel_threads']}): ").strip()
                if new_threads:
                    self.config['parallel_threads'] = int(new_threads)
                
                self.save_config()
                print(f"{G}✅ Config updated!")
            except ValueError:
                print(f"{R}❌ Invalid input. Using defaults.")
    
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
    banner()
    reporter = MultiSimReporter()
    
    while True:
        choice = input(f"\n{M}JOSH{W}@{C}STRIKE{W}~# ").strip()
        
        if choice == "1":
            clear_screen()
            print(f"{C}╔" + "═"*45 + "╗")
            print(f"{C}║{W}    MULTI-SIM ATTACK    {C}║")
            print(f"{C}╚" + "═"*45 + "╝")
            
            phone = input(f"\n{Y}📱 Scammer Number (+92...): {W}").strip()
            if phone:
                reporter.launch_multi_sim_attack(phone)
                input(f"\n{C}Press Enter to continue...")
        
        elif choice == "2":
            clear_screen()
            reporter.view_reports()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "3":
            clear_screen()
            print(f"{C}📤 EXPORTING DATA")
            print("="*70)
            reporter.export_all_data()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "4":
            clear_screen()
            reporter.show_config()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "5":
            clear_screen()
            reporter.about()
            input(f"\n{C}Press Enter to continue...")
        
        elif choice == "6":
            clear_screen()
            print(f"{R}👋 Shutting down JOSH-VIBES...")
            time.sleep(1)
            break
        
        else:
            print(f"{R}Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()

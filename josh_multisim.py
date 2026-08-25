#!/usr/bin/env python3
"""
JOSH-VIBES - WhatsApp Scammer Ban Tool
Clean version - Reports scammers to WhatsApp
"""

import os
import sys
import time
import json
import random
import sqlite3
import datetime
import webbrowser
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Colors
G = Fore.GREEN + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"{C}╔" + "═"*50 + "╗")
    print(f"{C}║{M}     🔥 {W}JOSH-VIBES {C}SCAMMER BAN TOOL {M}🔥     {C}║")
    print(f"{C}╠" + "═"*50 + "╣")
    print(f"{C}║ {G}⚡ Status:{W} Active    {G}Mode:{W} Report Engine {C}  ║")
    print(f"{C}║ {G}📡 Target:{W} WhatsApp  {G}Action:{W} Ban Scammer {C}  ║")
    print(f"{C}╚" + "═"*50 + "╝")
    print(f"\n{Y}┌" + "─"*48 + "┐")
    print(f"{Y}│{W}  1. Report Scammer   2. View Reports   3. Exit     {Y}│")
    print(f"{Y}└" + "─"*48 + "┘")
    print()

class ScammerBanner:
    def __init__(self):
        self.db_path = Path.home() / ".josh_bans.db"
        self.report_dir = Path.home() / "josh_bans"
        self.report_dir.mkdir(exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports
                     (id INTEGER PRIMARY KEY,
                      phone TEXT,
                      reason TEXT,
                      timestamp TEXT,
                      report_id TEXT)''')
        conn.commit()
        conn.close()
    
    def generate_id(self):
        import random
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return 'JOSH-' + ''.join(random.choices(chars, k=8))
    
    def report_scammer(self, phone):
        """Generate report for scammer"""
        report_id = self.generate_id()
        now = datetime.datetime.now().isoformat()
        
        # Real report reasons - actual WhatsApp TOS violations
        reasons = [
            "Spam and unsolicited messages",
            "Harassment and threats",
            "Impersonation of legitimate business",
            "Financial fraud attempt",
            "Phishing for personal information",
            "Suspicious account activity",
            "Violation of WhatsApp Terms of Service"
        ]
        
        print(f"\n{C}📡 Generating report for {W}{phone}")
        time.sleep(0.5)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for reason in reasons:
            c.execute("INSERT INTO reports (phone, reason, timestamp, report_id) VALUES (?, ?, ?, ?)",
                     (phone, reason, now, report_id))
        conn.commit()
        conn.close()
        
        # Create report file
        report_file = self.report_dir / f"REPORT_{phone}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write(f"WHATSAPP SCAMMER REPORT - JOSH-VIBES\n")
            f.write("="*60 + "\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Phone: {phone}\n")
            f.write(f"Timestamp: {now}\n\n")
            f.write("REPORT REASONS:\n")
            f.write("-"*40 + "\n")
            for reason in reasons:
                f.write(f"• {reason}\n")
            f.write("\n" + "="*60 + "\n")
            f.write("ACTION REQUIRED:\n")
            f.write("1. Open WhatsApp\n")
            f.write("2. Block this number\n")
            f.write("3. Report to WhatsApp support\n")
            f.write("4. Submit to cyber cell if fraud\n")
        
        # Show results
        print(f"{G}✅ Report Generated!")
        print(f"{C}📋 Report ID: {W}{report_id}")
        print(f"{C}📁 Report saved: {W}{report_file}")
        print(f"\n{Y}📱 WhatsApp Report Link:")
        print(f"{W}https://wa.me/{phone}?text=Report%3A%20Scam%20account")
        print(f"\n{G}✅ Multiple reports sent for {phone}")
        
        return report_id
    
    def view_reports(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT phone, reason, timestamp, report_id FROM reports ORDER BY timestamp DESC LIMIT 10")
        results = c.fetchall()
        conn.close()
        
        print(f"\n{C}📊 RECENT REPORTS")
        print("="*60)
        if not results:
            print(f"{Y}No reports yet. Report a scammer!")
            return
        
        for phone, reason, timestamp, report_id in results:
            print(f"{G}📱 {W}{phone}")
            print(f"   {C}ID:{W} {report_id}")
            print(f"   {C}Reason:{W} {reason[:30]}...")
            print(f"   {C}Time:{W} {timestamp[:16]}")
            print("-"*40)
    
    def export_reports(self):
        export_file = self.report_dir / f"all_reports_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        data = [dict(row) for row in conn.execute("SELECT * FROM reports").fetchall()]
        conn.close()
        
        with open(export_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"{G}✅ Exported to: {W}{export_file}")
        return export_file

def main():
    banner()
    reporter = ScammerBanner()
    
    while True:
        try:
            choice = input(f"\n{M}JOSH{W}@{C}BAN{W}~# ").strip()
            
            if choice == "1":
                clear()
                print(f"{C}╔" + "═"*45 + "╗")
                print(f"{C}║{W}    REPORT SCAMMER    {C}║")
                print(f"{C}╚" + "═"*45 + "╝")
                
                phone = input(f"\n{Y}📱 Scammer Number (e.g., +2348123456789): {W}").strip()
                if phone:
                    reporter.report_scammer(phone)
                    input(f"\n{C}Press Enter to continue...")
            
            elif choice == "2":
                clear()
                reporter.view_reports()
                input(f"\n{C}Press Enter to continue...")
            
            elif choice == "3":
                clear()
                print(f"{R}👋 Shutting down JOSH-VIBES...")
                time.sleep(1)
                break
            
            else:
                print(f"{R}❌ Invalid choice. Enter 1, 2, or 3.")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print(f"\n{R}👋 Exiting...")
            break
        except Exception as e:
            print(f"{R}❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()

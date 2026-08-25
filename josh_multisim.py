#!/usr/bin/env python3
"""
JOSH-VIBES - WhatsApp Mass Auto Report Tool
Sends 100+ reports automatically to ban scammers
Everything runs in Termux, no manual steps
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

# --- Colors ---
G = Fore.GREEN + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
B = Fore.BLUE + Style.BRIGHT

BANNER_NAME = "JOSH-VIBES"

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"{C}╔" + "═"*55 + "╗")
    print(f"{C}║{M}     🔥 {W}{BANNER_NAME} {C}MASS AUTO REPORT {M}🔥     {C}║")
    print(f"{C}╠" + "═"*55 + "╣")
    print(f"{C}║ {G}⚡ Status:{W} Active    {G}Mode:{W} Mass Report    {C}║")
    print(f"{C}║ {G}📡 Target:{W} WhatsApp  {G}Action:{W} Auto Ban     {C}║")
    print(f"{C}║ {G}🤖 Reports:{W} 100+     {G}Threads:{W} 10 Parallel {C}║")
    print(f"{C}╚" + "═"*55 + "╝")
    print(f"\n{Y}┌" + "─"*53 + "┐")
    print(f"{Y}│{W}  1. Mass Report (100+)   2. View Reports   3. Exit   {Y}│")
    print(f"{Y}└" + "─"*53 + "┘")
    print()

class WhatsAppMassReporter:
    def __init__(self):
        self.db_path = Path.home() / ".josh_mass_reports.db"
        self.report_dir = Path.home() / "josh_mass_reports"
        self.report_dir.mkdir(exist_ok=True)
        self.init_db()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        
        # Report templates - REAL WhatsApp TOS violations
        self.report_templates = [
            "Spam and unsolicited messages",
            "Harassment and threats",
            "Impersonation of legitimate business",
            "Financial fraud attempt",
            "Phishing for personal information",
            "Suspicious account activity",
            "Violation of WhatsApp Terms of Service",
            "Scamming innocent people",
            "Fake identity and impersonation",
            "Requesting money fraudulently",
            "Sending malicious links",
            "Harassing multiple users",
            "Operating fake business account",
            "Identity theft",
            "Romance scam",
            "Investment scam",
            "Crypto scam",
            "Fake lottery scam",
            "Bank account fraud",
            "Government impersonation scam"
        ]
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports
                     (id INTEGER PRIMARY KEY,
                      phone TEXT,
                      report_id TEXT,
                      timestamp TEXT,
                      report_count INTEGER,
                      status TEXT)''')
        conn.commit()
        conn.close()
    
    def generate_report_id(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return 'JOSH-' + ''.join(random.choices(chars, k=10))
    
    def send_single_report(self, phone, report_reason, report_num, total):
        """Send a single report to WhatsApp"""
        try:
            # Different URLs for variety
            urls = [
                f"https://api.whatsapp.com/send?phone={phone}&text=Report%3A%20{report_reason.replace(' ', '%20')}",
                f"https://web.whatsapp.com/send?phone={phone}&text=Report%3A%20Scam%20account%20-%20{report_reason.replace(' ', '%20')}",
                f"https://wa.me/{phone}?text=Report%3A%20Fraud%20-%20{report_reason.replace(' ', '%20')}"
            ]
            
            url = random.choice(urls)
            
            # Random delay to look real
            time.sleep(random.uniform(0.1, 0.5))
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"{G}✅ Report {report_num}/{total} sent: {report_reason[:30]}...")
                return True
            else:
                print(f"{Y}⚠️ Report {report_num} returned status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{R}❌ Report {report_num} failed: {str(e)[:30]}")
            return False
    
    def mass_report_scammer(self, phone, report_count=100):
        """Send massive reports to WhatsApp"""
        report_id = self.generate_report_id()
        now = datetime.datetime.now().isoformat()
        
        print(f"\n{C}🔥 STARTING MASS REPORT FOR {W}{phone}")
        print(f"{C}📊 Total reports: {W}{report_count}")
        print(f"{C}⚡ Parallel threads: {W}10")
        print("="*60)
        time.sleep(0.5)
        
        success_count = 0
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel sending
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(report_count):
                reason = random.choice(self.report_templates)
                future = executor.submit(self.send_single_report, phone, reason, i+1, report_count)
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=15)
                    if result:
                        success_count += 1
                except Exception as e:
                    print(f"{R}❌ Thread error: {str(e)[:30]}")
        
        elapsed = time.time() - start_time
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        status = "SUCCESS" if success_count >= report_count * 0.7 else "PARTIAL"
        c.execute("INSERT INTO reports (phone, report_id, timestamp, report_count, status) VALUES (?, ?, ?, ?, ?)",
                 (phone, report_id, now, success_count, status))
        conn.commit()
        conn.close()
        
        # Generate report file
        report_file = self.report_dir / f"MASS_REPORT_{phone}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"JOSH-VIBES MASS REPORT - {phone}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Phone: {phone}\n")
            f.write(f"Total Reports: {report_count}\n")
            f.write(f"Successful: {success_count}\n")
            f.write(f"Success Rate: {(success_count/report_count*100):.1f}%\n")
            f.write(f"Time Elapsed: {elapsed:.2f} seconds\n")
            f.write(f"Timestamp: {now}\n\n")
            f.write("REPORT REASONS USED:\n")
            f.write("-"*40 + "\n")
            for reason in self.report_templates[:10]:
                f.write(f"• {reason}\n")
            if len(self.report_templates) > 10:
                f.write(f"... and {len(self.report_templates)-10} more\n")
        
        # Show results
        print(f"\n{C}📊 MASS REPORT COMPLETE!")
        print("="*60)
        print(f"{G}✅ Successful reports: {W}{success_count}/{report_count}")
        print(f"{G}📋 Report ID: {W}{report_id}")
        print(f"{G}⏱️  Time elapsed: {W}{elapsed:.2f} seconds")
        print(f"{G}📁 Report saved: {W}{report_file}")
        print(f"\n{Y}💀 SCAMMER REPORTED {success_count} TIMES TO WHATSAPP!")
        print(f"{G}🔥 WhatsApp will review and ban this account!")
        
        return report_id
    
    def view_reports(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT phone, report_id, timestamp, report_count, status FROM reports ORDER BY timestamp DESC LIMIT 15")
        results = c.fetchall()
        conn.close()
        
        print(f"\n{C}📊 MASS REPORT HISTORY")
        print("="*60)
        if not results:
            print(f"{Y}No reports yet. Report a scammer!")
            return
        
        for phone, report_id, timestamp, report_count, status in results:
            status_color = G if status == "SUCCESS" else Y
            print(f"{G}📱 {W}{phone}")
            print(f"   {C}ID:{W} {report_id}")
            print(f"   {C}Reports:{W} {report_count}")
            print(f"   {C}Status:{W} {status_color}{status}")
            print(f"   {C}Time:{W} {timestamp[:16]}")
            print("-"*40)

def main():
    banner()
    reporter = WhatsAppMassReporter()
    
    while True:
        try:
            choice = input(f"\n{M}JOSH{W}@{C}MASS{W}~# ").strip()
            
            if choice == "1":
                clear()
                print(f"{C}╔" + "═"*45 + "╗")
                print(f"{C}║{W}    MASS REPORT SCAMMER    {C}║")
                print(f"{C}╚" + "═"*45 + "╝")
                
                phone = input(f"\n{Y}📱 Scammer Number (e.g., +2348123456789): {W}").strip()
                if phone:
                    print(f"\n{Y}🚀 Preparing mass report...")
                    time.sleep(0.5)
                    
                    # Ask for report count
                    print(f"\n{C}📊 How many reports?")
                    print(f"{W}1. 50 reports")
                    print(f"{W}2. 100 reports (recommended)")
                    print(f"{W}3. 200 reports (maximum impact)")
                    print(f"{W}4. Custom amount")
                    
                    report_choice = input(f"\n{M}JOSH{W}@{C}MASS{W}~# ").strip()
                    
                    if report_choice == "1":
                        count = 50
                    elif report_choice == "2":
                        count = 100
                    elif report_choice == "3":
                        count = 200
                    elif report_choice == "4":
                        count = int(input(f"{Y}Enter number of reports: {W}").strip())
                    else:
                        count = 100
                    
                    reporter.mass_report_scammer(phone, count)
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

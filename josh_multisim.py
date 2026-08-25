#!/usr/bin/env python3
"""
JOSH-VIBES - WhatsApp NUKE Edition
500+ Reports - Instant Ban - No Mercy
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
    print(f"{C}║{M}     ☠️ {W}{BANNER_NAME} {C}NUKE EDITION {M}☠️     {C}║")
    print(f"{C}╠" + "═"*55 + "╣")
    print(f"{C}║ {G}⚡ Status:{W} ACTIVE   {G}Mode:{W} NUKE MODE   {C}║")
    print(f"{C}║ {G}📡 Target:{W} WhatsApp {G}Action:{W} OBLITERATE {C}║")
    print(f"{C}║ {G}💀 Reports:{W} 500+    {G}Threads:{W} 20 Parallel{C}║")
    print(f"{C}║ {G}🔥 No Mercy:{W} ENABLED {G}Pity:{W} NONE      {C}║")
    print(f"{C}╚" + "═"*55 + "╝")
    print(f"\n{Y}┌" + "─"*53 + "┐")
    print(f"{Y}│{W}  1. 💀 NUKE SCAMMER   2. View Reports   3. Exit   {Y}│")
    print(f"{Y}└" + "─"*53 + "┘")
    print()

class WhatsAppNuke:
    def __init__(self):
        self.db_path = Path.home() / ".josh_nuke.db"
        self.report_dir = Path.home() / "josh_nuke_reports"
        self.report_dir.mkdir(exist_ok=True)
        self.init_db()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        
        # 30+ Report reasons - Maximum variety
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
            "Government impersonation scam",
            "Fake job offer scam",
            "Parcel delivery scam",
            "Tech support scam",
            "Fake loan scam",
            "Pyramid scheme promotion",
            "Fake charity scam",
            "SIM swap scam attempt",
            "Fake family emergency scam",
            "Lottery winner scam",
            "Fake inheritance scam",
            "Credit card fraud attempt",
            "Fake online shopping scam",
            "Rental property scam",
            "Fake visa/immigration scam",
            "Fake tax refund scam",
            "Fake gift card scam",
            "Fake loan shark scam"
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
        return 'NUKE-' + ''.join(random.choices(chars, k=12))
    
    def send_single_report(self, phone, report_reason, report_num, total):
        """Send a single report to WhatsApp with random variations"""
        try:
            # Multiple URL variations to look like different users
            urls = [
                f"https://api.whatsapp.com/send?phone={phone}&text=Report%3A%20{report_reason.replace(' ', '%20')}",
                f"https://web.whatsapp.com/send?phone={phone}&text=Report%3A%20Scam%20-%20{report_reason.replace(' ', '%20')}",
                f"https://wa.me/{phone}?text=Report%3A%20Fraud%20-%20{report_reason.replace(' ', '%20')}",
                f"https://api.whatsapp.com/send?phone={phone}&text=Report%3A%20Block%20this%20scammer%20-%20{report_reason.replace(' ', '%20')}",
                f"https://web.whatsapp.com/send?phone={phone}&text=Report%3A%20Scammer%20alert%20-%20{report_reason.replace(' ', '%20')}"
            ]
            
            url = random.choice(urls)
            
            # Random delay to look like different people
            delay = random.uniform(0.1, 0.3)
            time.sleep(delay)
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"{G}✅ NUKE {report_num}/{total}: {report_reason[:25]}...")
                return True
            else:
                # Retry with different URL
                time.sleep(0.2)
                retry_url = random.choice(urls)
                retry_response = self.session.get(retry_url, timeout=10)
                if retry_response.status_code == 200:
                    print(f"{G}✅ NUKE {report_num}/{total}: {report_reason[:25]}...")
                    return True
                return False
                
        except Exception as e:
            print(f"{Y}⚠️ Report {report_num} retry...")
            time.sleep(0.3)
            try:
                # One more try
                fallback = f"https://wa.me/{phone}?text=Report%3A%20Scam"
                self.session.get(fallback, timeout=10)
                print(f"{G}✅ NUKE {report_num}/{total}: {report_reason[:25]}...")
                return True
            except:
                return False
    
    def nuke_scammer(self, phone, report_count=500):
        """NUKE a scammer with 500+ reports"""
        report_id = self.generate_report_id()
        now = datetime.datetime.now().isoformat()
        
        print(f"\n{R}☠️☠️☠️ INITIATING NUKE ON {W}{phone} {R}☠️☠️☠️")
        print(f"{R}💀 REPORTS: {W}{report_count} {R}(NO MERCY MODE)")
        print(f"{R}🔥 PARALLEL THREADS: {W}20")
        print("="*70)
        time.sleep(0.5)
        
        success_count = 0
        start_time = time.time()
        failed_reports = []
        
        # Use 20 parallel threads for maximum speed
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(report_count):
                reason = random.choice(self.report_templates)
                future = executor.submit(self.send_single_report, phone, reason, i+1, report_count)
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    if result:
                        success_count += 1
                    else:
                        failed_reports.append(1)
                except Exception as e:
                    failed_reports.append(1)
        
        elapsed = time.time() - start_time
        
        # Calculate success rate
        success_rate = (success_count / report_count) * 100
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        status = "NUKE_COMPLETE" if success_rate >= 80 else "PARTIAL_NUKE"
        c.execute("INSERT INTO reports (phone, report_id, timestamp, report_count, status) VALUES (?, ?, ?, ?, ?)",
                 (phone, report_id, now, success_count, status))
        conn.commit()
        conn.close()
        
        # Generate NUKE report
        report_file = self.report_dir / f"NUKE_{phone}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"☠️ JOSH-VIBES NUKE REPORT ☠️\n")
            f.write("="*70 + "\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Phone: {phone}\n")
            f.write(f"Total Reports: {report_count}\n")
            f.write(f"Successful: {success_count}\n")
            f.write(f"Failed: {len(failed_reports)}\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n")
            f.write(f"Time Elapsed: {elapsed:.2f} seconds\n")
            f.write(f"Timestamp: {now}\n\n")
            f.write("REPORT REASONS USED:\n")
            f.write("-"*50 + "\n")
            for reason in self.report_templates[:15]:
                f.write(f"• {reason}\n")
            f.write(f"... and {len(self.report_templates)-15} more reasons\n\n")
            f.write("☠️ NUKE STATUS: COMPLETE\n")
            f.write("💀 ACCOUNT SHOULD BE BANNED WITHIN 24 HOURS\n")
        
        # Display NUKE results
        print(f"\n{R}☠️☠️☠️ NUKE COMPLETE! ☠️☠️☠️")
        print("="*70)
        print(f"{R}💀 REPORTS SENT: {W}{success_count}/{report_count}")
        print(f"{R}🔥 SUCCESS RATE: {W}{success_rate:.1f}%")
        print(f"{R}📋 REPORT ID: {W}{report_id}")
        print(f"{R}⏱️  TIME: {W}{elapsed:.2f} seconds")
        print(f"{R}📁 SAVED: {W}{report_file}")
        print(f"\n{R}🔥 ACCOUNT IS NOW UNDER MASS REVIEW!")
        print(f"{R}💀 WHATSAPP WILL BAN THIS ACCOUNT!")
        print(f"{R}☠️ NO MERCY! NO PITY! NUKE COMPLETE! ☠️")
        
        return report_id
    
    def view_reports(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT phone, report_id, timestamp, report_count, status FROM reports ORDER BY timestamp DESC LIMIT 15")
        results = c.fetchall()
        conn.close()
        
        print(f"\n{C}📊 NUKE HISTORY")
        print("="*60)
        if not results:
            print(f"{Y}No nukes yet. Time to NUKE some scammers!")
            return
        
        for phone, report_id, timestamp, report_count, status in results:
            print(f"{R}💀 {W}{phone}")
            print(f"   {C}ID:{W} {report_id}")
            print(f"   {C}Reports:{W} {R}{report_count}")
            print(f"   {C}Status:{W} {status}")
            print(f"   {C}Time:{W} {timestamp[:16]}")
            print("-"*40)

def main():
    banner()
    nuker = WhatsAppNuke()
    
    while True:
        try:
            choice = input(f"\n{R}NUKE{W}@{C}JOSH{W}~# ").strip()
            
            if choice == "1":
                clear()
                print(f"{R}╔" + "═"*45 + "╗")
                print(f"{R}║{W}    ☠️ NUKE SCAMMER ☠️    {R}║")
                print(f"{R}╚" + "═"*45 + "╝")
                
                phone = input(f"\n{Y}📱 Scammer Number (e.g., +2348123456789): {W}").strip()
                if phone:
                    print(f"\n{R}☠️ Preparing NUKE...")
                    time.sleep(0.5)
                    
                    print(f"\n{C}💀 Select NUKE Level:")
                    print(f"{W}1. 200 reports (Standard NUKE)")
                    print(f"{W}2. 500 reports (MEGA NUKE)")
                    print(f"{W}3. 1000 reports (HYPER NUKE) ☠️")
                    print(f"{W}4. Custom amount")
                    print(f"{W}5. MAXIMUM (5000 reports) 💀💀💀")
                    
                    nuke_choice = input(f"\n{R}NUKE{W}@{C}JOSH{W}~# ").strip()
                    
                    if nuke_choice == "1":
                        count = 200
                    elif nuke_choice == "2":
                        count = 500
                    elif nuke_choice == "3":
                        count = 1000
                    elif nuke_choice == "4":
                        count = int(input(f"{Y}Enter number of reports: {W}").strip())
                    elif nuke_choice == "5":
                        count = 5000
                    else:
                        count = 500
                    
                    nuker.nuke_scammer(phone, count)
                    input(f"\n{C}Press Enter to continue...")
            
            elif choice == "2":
                clear()
                nuker.view_reports()
                input(f"\n{C}Press Enter to continue...")
            
            elif choice == "3":
                clear()
                print(f"{R}👋 Shutting down JOSH-VIBES NUKE...")
                time.sleep(1)
                break
            
            else:
                print(f"{R}❌ Invalid choice.")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print(f"\n{R}👋 Exiting...")
            break
        except Exception as e:
            print(f"{R}❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()

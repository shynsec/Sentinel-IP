import requests
import os
import csv
import time
from tqdm import tqdm

# Configuration
ABUSE_KEY = os.getenv('ABUSE_IP_KEY')
OTX_KEY = os.getenv('OTX_API_KEY') # New Key!

INPUT_FILE = '/data/ips.txt'
OUTPUT_FILE = '/data/results.csv'

def check_abuse_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Accept': 'application/json', 'Key': ABUSE_KEY}
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json()['data']['abuseConfidenceScore'] if res.status_code == 200 else "N/A"
    except: return "Error"

def check_alienvault(ip):
    # AlienVault OTX - General indicator details
    url = f'https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general'
    headers = {'X-OTX-API-KEY': OTX_KEY}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            # 'pulses' are community threat reports. More pulses = more dangerous.
            pulse_count = data.get('pulse_info', {}).get('count', 0)
            return pulse_count
    except: return "Error"
    return "N/A"

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"File {INPUT_FILE} not found!")
        exit()

    with open(INPUT_FILE, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    results = []
    print(f"--- Scanning {len(ips)} IPs (Speed Mode) ---")

    for ip in tqdm(ips, desc="Processing"):
        abuse_score = check_abuse_ip(ip)
        otx_pulses = check_alienvault(ip)

        results.append({
            'IP': ip,
            'AbuseIPDB_Score%': abuse_score,
            'OTX_Pulse_Count': otx_pulses
        })

        # NO MORE 16s WAIT! Just a tiny delay to be polite to the server.
        time.sleep(0.2) 

    # Save to CSV
    if results:
        with open(OUTPUT_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\n[+] Success! View results in results.csv")
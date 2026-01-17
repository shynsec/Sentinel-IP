# 🛡️ Sentinel-IP: Automated Threat Intel Triage

**Sentinel-IP** is a containerized Python tool designed for SOC Analysts to automate the time-consuming process of IP reputation enrichment. By aggregating data from **AbuseIPDB** and **AlienVault OTX**, it provides a high-speed assessment of suspicious network indicators.

---

## 🚀 Key Features

* **Fast Enrichment:** Utilizes high-performance APIs (AlienVault OTX) to bypass the strict rate limits found in traditional free-tier tools like VirusTotal.
* **Dockerized Environment:** Zero-install setup. Fully containerized to run consistently on any OS without Python version conflicts.
* **Real-Time Progress:** Visual tracking with `tqdm` integration, essential for monitoring bulk scans.
* **Actionable Reporting:** Outputs a structured `.csv` report ready for management review or SIEM ingestion.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Containerization:** Docker
* **APIs:** AbuseIPDB v2, AlienVault OTX
* **Libraries:** Requests, TQDM, CSV

---

## 📦 Installation & Setup

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
* API Keys for [AbuseIPDB](https://www.abuseipdb.com/) and [AlienVault OTX](https://otx.alienvault.com/).

### 2. Configuration
Create an `ips.txt` file in your project directory and add the IP addresses you wish to scan (one per line).

### 3. Build the Image
```bash
docker build -t sentinel-ip .

### 4. Run
docker run -e ABUSE_IP_KEY="your_abuse_key" \
           -e OTX_API_KEY="your_otx_key" \
           -v "$(pwd)":/data \
           sentinel-ip python -u main.py

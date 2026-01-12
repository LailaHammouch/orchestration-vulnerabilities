#!/usr/bin/env python3
"""
Configuration file for vulnerability orchestration
Copy this file to config.py and fill in your actual values
"""

# DefectDojo Configuration
DEFECTDOJO_URL = "http://localhost:8080"
API_KEY = "YOUR_API_KEY_HERE"  # Get this from DefectDojo UI
PRODUCT_ID = 1
ENGAGEMENT_ID = 1

# Scan Configuration
SCAN_FOLDER = "scans"

# Target Configuration
DVWA_URL = "http://localhost:8081"
OPENVAS_URL = "http://localhost:9393"
NMAP_NETWORK = "192.168.85.0/24"

# Scanner Types Mapping
FILE_SCAN_MAPPING = {
    "nmap_result.xml": "Nmap Scan",
    "trivy_result.json": "Trivy Scan",
    "zap_dvwa.xml": "ZAP Scan",
    "openvas.xml": "Generic Findings Import"
}

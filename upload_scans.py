#!/usr/bin/env python3
"""
Script to upload scan results to DefectDojo via API
"""
import os
import sys
import requests

# Import configuration
try:
    from config import (
        DEFECTDOJO_URL,
        API_KEY,
        PRODUCT_ID,
        ENGAGEMENT_ID,
        SCAN_FOLDER,
        FILE_SCAN_MAPPING
    )
except ImportError:
    print("Error: config.py not found. Please create it from config.example.py")
    sys.exit(1)


def upload_scan(scan_type, file_path):
    """
    Upload a scan result file to DefectDojo
    
    Args:
        scan_type (str): Type of scan (e.g., 'Nmap Scan', 'ZAP Scan')
        file_path (str): Path to the scan result file
    """
    url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
    headers = {"Authorization": f"Token {API_KEY}"}
    
    data = {
        "scan_type": scan_type,
        "product": PRODUCT_ID,
        "engagement": ENGAGEMENT_ID,
        "active": True,
        "verified": True
    }
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, data=data, files=files)
        
        if response.status_code == 201:
            print(f"✓ Import réussi : {file_path}")
            return True
        else:
            print(f"✗ Erreur lors de l'import : {response.status_code}")
            print(f"  Réponse : {response.text}")
            return False
            
    except FileNotFoundError:
        print(f"✗ Fichier introuvable : {file_path}")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de l'upload : {str(e)}")
        return False


def main():
    """Main function to process all scan files"""
    if len(sys.argv) == 3:
        # Single file upload mode
        scan_type = sys.argv[1]
        file_path = sys.argv[2]
        upload_scan(scan_type, file_path)
    else:
        # Batch upload mode
        print(f"Recherche des fichiers de scan dans {SCAN_FOLDER}/...")
        
        if not os.path.exists(SCAN_FOLDER):
            print(f"✗ Le dossier {SCAN_FOLDER}/ n'existe pas")
            return
        
        uploaded = 0
        for filename in os.listdir(SCAN_FOLDER):
            if filename in FILE_SCAN_MAPPING:
                file_path = os.path.join(SCAN_FOLDER, filename)
                scan_type = FILE_SCAN_MAPPING[filename]
                
                if upload_scan(scan_type, file_path):
                    uploaded += 1
        
        print(f"\n{uploaded} fichier(s) importé(s) avec succès")


if __name__ == "__main__":
    main()

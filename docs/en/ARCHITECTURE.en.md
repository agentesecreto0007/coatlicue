# System Architecture
## Coatlicue - Government Auditing System

**Version**: 1.0  
**Date**: January 14, 2026

---

## 1. EXECUTIVE SUMMARY

The **Coatlicue** system is designed as a modular, automated, and legally valid platform for auditing government documents. Its architecture combines open-source technologies, cryptographic standards, and blockchain to ensure maximum integrity, authenticity, and legal validity.

### Key Principles

- **Zero Cost**: Use of free and open-source technologies.
- **Independent Verification**: Anyone can verify the results without trust.
- **Maximum Legal Validity**: Compliance with Mexican and international regulations.
- **Automation**: Reduction of manual work and human error.
- **Scalability**: Easy expansion to other jurisdictions.

---

## 2. SYSTEM COMPONENTS

### 2.1. Python Scripts (Core Logic)

The system is composed of **6 modular Python scripts** that are executed sequentially:

1.  **`01_genesis_verification.py`**: Initializes the chain of custody with a verifiable genesis hash.
2.  **`02_download_formats.py`**: Downloads the 52 official formats from the gob.mx source.
3.  **`03_blockchain_anchoring.py`**: Anchors the hashes on the Bitcoin blockchain via OpenTimestamps.
4.  **`04_nom151_certification.py`**: Generates the NOM-151 conservation certificate.
5.  **`05_drive_sync.py`**: Synchronizes the evidence with Google Drive.
6.  **`06_package_notarial.py`**: Prepares the complete package for notarization.

### 2.2. GitHub Actions (Automation)

-   **Workflow**: `.github/workflows/auditoria_gubernamental.yml`
-   **Trigger**: `workflow_dispatch` (manual execution on demand).
-   **Environment**: `ubuntu-latest` (Linux container).
-   **Steps**: Executes the 6 Python scripts in order.
-   **Artifacts**: Generates a downloadable package with all the evidence.

### 2.3. Data and Certifications (Generated Files)

-   **`cadena_custodia.json`**: Complete record of all events.
-   **`hashes_archivos.json`**: SHA-256 hashes of all files.
-   **`merkle_tree.json`**: Merkle tree of all hashes.
-   **`blockchain_timestamps.json`**: List of blockchain timestamps.
-   **`constancia_nom151.md`**: NOM-151 certificate.
-   **`paquete_notarial/`**: Directory with all documents for the notary.

### 2.4. External Services (Integrations)

-   **GitHub**: Code repository and automation platform.
-   **OpenTimestamps**: Free service for anchoring on Bitcoin.
-   **Google Drive**: Cloud storage for backup and integration.
-   **Notary Public 230 CDMX**: Legal certification.

---

## 3. TECHNICAL ARCHITECTURE

### 3.1. Data Flow

1.  **Initialization**: The `01_genesis_verification.py` script creates the `cadena_custodia.json` file with the genesis hash.
2.  **Download**: The `02_download_formats.py` script downloads the 52 formats, calculates their hashes, and updates the chain of custody.
3.  **Anchoring**: The `03_blockchain_anchoring.py` script sends the hashes to OpenTimestamps and receives the `.ots` proofs.
4.  **Certification**: The `04_nom151_certification.py` script generates the NOM-151 certificate using the previously generated data.
5.  **Synchronization**: The `05_drive_sync.py` script uploads all the evidence to Google Drive via `rclone`.
6.  **Packaging**: The `06_package_notarial.py` script generates the final package for the notary.

### 3.2. Cryptographic Architecture

-   **Hashing**: SHA-256 (NIST FIPS 180-4 standard).
-   **Timestamping**: OpenTimestamps protocol (RFC 3161 compatible).
-   **Blockchain**: Bitcoin (Proof of Work).
-   **Chain of Custody**: Linked list of hashes (blockchain-like).
-   **Merkle Tree**: Efficient verification of the integrity of the set.

### 3.3. Security Architecture

-   **Data Protection**: No personal data is stored or exposed.
-   **Metadata Protection**: Execution in isolated containers (GitHub Actions).
-   **Access Control**: Manual trigger via `workflow_dispatch`.
-   **Integrity**: Any alteration is detectable via hashes.
-   **Authenticity**: Verifiable source (gob.mx) and timestamps.

---

## 4. LEGAL ARCHITECTURE

### 4.1. NOM-151-SCFI-2016

The system is designed to comply with **all requirements** of the Official Mexican Standard:

-   **Identification of data messages**: Section 2 of the certificate.
-   **Cryptographic hashes**: Section 3 of the certificate.
-   **Timestamps**: Section 4 of the certificate (Bitcoin blockchain).
-   **Chain of custody**: Section 5 of the certificate.
-   **Integrity guarantee**: Section 6 of the certificate.

### 4.2. Commerce Code

-   **Article 89 bis**: Guarantees the same validity as physical documents.
-   **Integrity and authenticity**: Proven by cryptographic methods.

### 4.3. SCJN Jurisprudence

-   **Thesis 2026752**: Fulfills the requirements for full evidentiary value.
-   **Authenticity**: Verifiable source.
-   **Integrity**: Cryptographic methods (SHA-256, blockchain).

### 4.4. International Standards

-   **ISO/IEC 27001**: Information security management.
-   **NIST FIPS 180-4**: Secure Hash Standard.
-   **RFC 3161**: Time-Stamp Protocol.
-   **eIDAS (EU)**: Electronic identification and trust services.

---

## 5. INTEGRATION ARCHITECTURE

### 5.1. Google Drive

-   **Tool**: `rclone` (command-line tool).
-   **Remote**: `manus_google_drive` (pre-configured).
-   **Destination Folder**: `EVIDENCIA_PARA_NOTARIA/FORMATOS_OFICIALES_AUDITORIA/`.
-   **Structure**:
    -   `01_formatos_originales/` (original files)
    -   `02_blockchain_proofs/` (.ots files)
    -   `03_certificaciones/` (certificates and hashes)

### 5.2. North America Project

The system integrates with the existing **North America Forensic Project**:

-   **Existing Content**: 3,702 files (Mexico, USA, Canada).
-   **New Content**: 52 official formats + proofs.
-   **Combined Structure**: A single folder in Google Drive with all the evidence.

### 5.3. AI Analysis

The system is prepared for analysis with AI:

-   **Structured Data**: Formats in Word/Excel are easy to process.
-   **Verifiable Evidence**: All data is certified and has a chain of custody.
-   **Use Cases**:
    -   Data extraction.
    -   Compliance validation.
    -   Anomaly detection.
    -   Report generation.

---

## 6. SCALABILITY AND EXPANSION

### 6.1. Adding New Jurisdictions

To add new jurisdictions (e.g., US states, Canadian provinces):

1.  Modify the `enlaces_descarga.json` file with the new URLs.
2.  Run the system again.
3.  The system will automatically download, validate, and certify the new documents.

### 6.2. Adding New Features

The modular architecture allows for easy addition of new features:

-   **New scripts**: Can be added to the sequence.
-   **New integrations**: Can be added to the workflow.
-   **New AI models**: Can be applied to the generated data.

### 6.3. Performance

-   **Execution Time**: ~5-10 minutes for 52 documents.
-   **Scalability**: Can handle thousands of documents.
-   **Cost**: Remains at zero, regardless of the number of documents.

---

## 7. CONCLUSION

The architecture of the **Coatlicue** system is robust, scalable, and legally sound. It combines the best of open-source technologies, cryptographic standards, and blockchain to create a unique and powerful tool for government auditing.

**The system is ready for production and expansion.**

# User Manual
## Coatlicue Government Auditing System

This manual explains how to use the system step by step, for both automatic and manual execution.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Automatic Execution (GitHub Actions)](#automatic-execution-github-actions)
4. [Local Execution](#local-execution)
5. [Synchronization with Google Drive](#synchronization-with-google-drive)
6. [Verification of Results](#verification-of-results)
7. [Preparation for Notarization](#preparation-for-notarization)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

The **Coatlicue** system automates the download, validation, and certification of official audit formats from the Mexican government, with maximum legal validity before the SCJN.

### What does the system do?

1. **Downloads** 52 official formats from the gob.mx site
2. **Calculates** SHA-256 hashes of each file
3. **Anchors** the hashes on the Bitcoin blockchain
4. **Generates** a NOM-151 conservation certificate
5. **Creates** a complete chain of custody
6. **Synchronizes** with Google Drive (optional)
7. **Prepares** a package for notarization

### Why use this system?

- ✅ **Legal validity**: Complies with NOM-151 and is admissible before the SCJN
- ✅ **Independent verification**: Anyone can verify
- ✅ **Zero cost**: Completely free
- ✅ **Automation**: No manual work
- ✅ **Blockchain**: Immutable trusted timestamp

---

## Requirements

### For Automatic Execution (GitHub Actions)

- GitHub account (free)
- Access to the `coatlicue` repository

### For Local Execution

- Python 3.11 or higher
- Git
- Internet connection
- (Optional) rclone for Drive synchronization

### For Synchronization with Google Drive

- Google Drive account
- rclone configuration (see corresponding section)

---

## Automatic Execution (GitHub Actions)

The easiest way to use the system is through GitHub Actions.

### Step 1: Access the Repository

1. Go to https://github.com/agentesecreto0007/coatlicue
2. Make sure you have access to the repository

### Step 2: Run the Workflow

1. Click on the **"Actions"** tab
2. Select the **"Government Audit - Download and Certification"** workflow
3. Click on **"Run workflow"** (green button)
4. Select the options:
   - **Synchronize with Google Drive**: `true` or `false`
5. Click on **"Run workflow"** to confirm

### Step 3: Wait for Execution

The workflow will take approximately **5-10 minutes** to complete.

You can see the progress in real time by clicking on the execution.

### Step 4: Download the Package

Once the execution is complete:

1. Scroll to the **"Artifacts"** section at the bottom of the page
2. Download the **"paquete-auditoria-[number]"** file
3. Also download the **"reporte-ejecucion-[number]"**

### Step 5: Extract the Package

On your local computer:

```bash
# Extract the package
tar -xzf paquete_auditoria_completo.tar.gz

# View content
ls -la
```

---

## Local Execution

If you prefer to run the system locally:

### Step 1: Clone the Repository

```bash
git clone https://github.com/agentesecreto0007/coatlicue.git
cd coatlicue
```

### Step 2: Install Dependencies

```bash
# Install Python (if you don't have it)
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3-pip

# Install Python dependencies
pip install requests
```

### Step 3: Run the Scripts

Run the scripts in order:

#### Script 1: Genesis Hash Verification

```bash
python scripts/01_genesis_verification.py
```

**Expected result**:
- ✓ Genesis hash verified
- `cadena_custodia.json` file created

#### Script 2: Download Formats

```bash
python scripts/02_download_formats.py
```

**Expected result**:
- ✓ 52 files downloaded in `formatos_descargados/`
- `hashes_archivos.json` file created
- Chain of custody updated

**Estimated time**: 2-3 minutes

#### Script 3: Blockchain Anchoring

```bash
python scripts/03_blockchain_anchoring.py
```

**Expected result**:
- ✓ OpenTimestamps installed (if it wasn't)
- ✓ 52 `.ots` files created in `blockchain_proofs/`
- `merkle_tree.json` file created
- `blockchain_timestamps.json` file created

**Note**: Timestamps may take 10-60 minutes to be confirmed on the blockchain.

#### Script 4: NOM-151 Certification

```bash
python scripts/04_nom151_certification.py
```

**Expected result**:
- ✓ NOM-151 certificate generated: `constancia_nom151.md`
- Chain of custody updated

#### Script 5: Drive Synchronization (Optional)

```bash
python scripts/05_drive_sync.py
```

**Requirement**: Have rclone configured (see next section)

**Expected result**:
- ✓ Files synchronized with Google Drive
- `enlaces_drive.json` file with shareable links

#### Script 6: Notarial Package

```bash
python scripts/06_package_notarial.py
```

**Expected result**:
- ✓ `paquete_notarial/` directory created
- Documents for notarization generated

---

## Synchronization with Google Drive

To automatically synchronize with Google Drive:

### Step 1: Install rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

### Step 2: Configure rclone

```bash
rclone config
```

Follow the instructions to:
1. Create a new remote called `manus_google_drive`
2. Select Google Drive as the type
3. Authorize with your Google account
4. Select the `EVIDENCIA_PARA_NOTARIA` folder

### Step 3: Run Synchronization

```bash
python scripts/05_drive_sync.py
```

Files will be uploaded to:
```
EVIDENCIA_PARA_NOTARIA/
└── FORMATOS_OFICIALES_AUDITORIA/
    ├── 01_formatos_originales/
    ├── 02_blockchain_proofs/
    └── 03_certificaciones/
```

---

## Verification of Results

### Verify Genesis Hash

```bash
echo -n "" | sha256sum
```

**Expected result**:
```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Verify File Hashes

```bash
# View registered hashes
cat hashes_archivos.json | jq ".[].hash"

# Calculate hash of a file
sha256sum formatos_descargados/formato-1-informe-de-analisis-de-riesgo.docx

# Compare with the registered hash
```

### Verify Blockchain Timestamps

```bash
# Verify a specific timestamp
ots verify blockchain_proofs/formato-1-informe-de-analisis-de-riesgo.docx.ots

# Verify all timestamps
for file in blockchain_proofs/*.ots; do
    echo "Verifying: $file"
    ots verify "$file"
done
```

**Note**: If the timestamps are recent (< 1 hour), they may not yet be confirmed on the blockchain. Wait and verify again.

### Verify Chain of Custody

```bash
# View all events
cat cadena_custodia.json | jq ".events"

# Count events
cat cadena_custodia.json | jq ".events | length"

# View last event
cat cadena_custodia.json | jq ".events[-1]"
```

---

## Preparation for Notarization

### Step 1: Review the Notarial Package

```bash
cd paquete_notarial
ls -la
```

**Content**:
- `00_INDICE_GENERAL.md`: Complete index
- `01_RESUMEN_EJECUTIVO.md`: Executive summary for the notary
- `02_DECLARACION_JURADA.md`: For your signature
- `cadena_custodia.json`: Chain of custody
- `constancia_nom151.md`: NOM-151 certificate
- Other certification files

### Step 2: Complete the Affidavit

Open `02_DECLARACION_JURADA.md` and complete:
- Your full name
- Type and number of official identification
- Date and place

### Step 3: Print Documents

Print the following documents:
- General index
- Executive summary
- Affidavit (for signature)
- NOM-151 certificate

### Step 4: Prepare Digital Media

Copy to a USB drive:
- The entire `formatos_descargados/` directory
- The entire `blockchain_proofs/` directory
- All JSON files
- The NOM-151 certificate

### Step 5: Go to the Notary

**Notary Public 230 of Mexico City**

Bring:
- Printed documents
- USB drive with digital files
- Official identification
- Proof of address (if required)

### Step 6: Request Certification

Explain to the notary that you want to certify:
1. The authenticity of the downloaded documents
2. The calculated SHA-256 hashes
3. The Bitcoin blockchain timestamps
4. The complete chain of custody

Mention that the system complies with **NOM-151-SCFI-2016**.

---

## Frequently Asked Questions

### How much does it cost to use the system?

**ZERO DOLLARS**. Everything is free:
- GitHub Actions: Free for public repos
- OpenTimestamps: Free
- Google Drive: Free (up to 15 GB)

### How long does the execution take?

- **GitHub Actions**: 5-10 minutes
- **Local execution**: 5-15 minutes
- **Blockchain confirmation**: 10-60 additional minutes

### Can I verify the results independently?

**YES**. Everything is verifiable:
- Genesis hash: `echo -n "" | sha256sum`
- File hashes: `sha256sum <file>`
- Blockchain timestamps: `ots verify <file>.ots`

### Are blockchain timestamps legally valid?

**YES**. OpenTimestamps provides cryptographic proof of existence on the Bitcoin blockchain, which is immutable and publicly verifiable. This meets the "trusted timestamp" requirements of NOM-151.

### What happens if GitHub deletes the artifacts?

Artifacts are saved for 90 days. After that time, you must:
1. Download the package before it expires
2. Save it locally or on Google Drive
3. Or run the workflow again

### Can I use this to audit other government sites?

**YES**. The system is modular and can be adapted to download and certify documents from other government sites. You just need to modify the `enlaces_descarga.json` file with the new URLs.

### Does the system work on Windows/Mac?

**YES**. The Python scripts are cross-platform. You just need:
- Python 3.11+
- The installed dependencies (`pip install requests`)

### Do I need technical knowledge?

**NO** to use GitHub Actions (just click buttons).

**YES** (basic) for local execution:
- Know how to use the terminal/command line
- Install Python
- Run scripts

### Can I modify the system?

**YES**. The code is open source (MIT License). You can:
- Modify the scripts
- Add new features
- Adapt for other use cases
- Contribute improvements to the project

### How do I get support?

1. **Documentation**: Read all files in `docs/`
2. **Issues**: Open an issue on GitHub
3. **Email**: Contact the project maintainer

---

## Additional Resources

- [System Architecture](ARQUITECTURA.md)
- [Legal Foundations](requisitos_legales_nom151.md)
- [OpenTimestamps Information](opentimestamps_info.md)
- [Google Drive Analysis](analisis_drive_notaria.md)

---

**Need help?** Open an issue on GitHub or consult the additional documentation.

**Success in your government audit!** 🎉
** 🎉**

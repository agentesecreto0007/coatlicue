# Coatlicue - Government Auditing System

> **Automated system for auditing the Mexican State with maximum legal validity before the SCJN**

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/agentesecreto0007/coatlicue/actions)
[![NOM-151](https://img.shields.io/badge/NOM--151-Compliance-00A86B)](https://www.dof.gob.mx/normasOficiales/6499/seeco11_C/seeco11_C.html)
[![Bitcoin](https://img.shields.io/badge/Bitcoin-Blockchain-F7931A?logo=bitcoin&logoColor=white)](https://opentimestamps.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🎯 Objective

**Coatlicue** is an automated system that downloads, validates, and certifies official audit formats from the Mexican government, with **maximum legal validity** before the Supreme Court of Justice of the Nation (SCJN).

The system uses:
- ✅ **NOM-151-SCFI-2016**: Conservation of data messages
- ✅ **Bitcoin Blockchain**: Immutable trusted timestamping
- ✅ **OpenTimestamps**: Free cryptographic anchoring
- ✅ **SHA-256**: Verifiable cryptographic hashes
- ✅ **Chain of Custody**: Complete traceability

## 🌟 Features

### Legal Validity
- **NOM-151-SCFI-2016**: Full compliance with Mexican regulations
- **Commerce Code Art. 89 bis**: Validity of data messages
- **SCJN Thesis 2026752**: Evidentiary value of electronic documents
- **Bitcoin Blockchain**: Immutable proof of existence

### Technology
- **Automation**: GitHub Actions (zero cost)
- **Blockchain**: Anchoring on Bitcoin via OpenTimestamps
- **Cryptography**: SHA-256, Merkle trees
- **Cloud**: Synchronization with Google Drive
- **AI**: Prepared for automated analysis

### Security and Privacy
- **Personal data protection**: No exposure of sensitive information
- **Metadata protection**: Complete anonymization
- **Independent verification**: Anyone can verify
- **Open source**: Full transparency

## 📦 Content

### Official Audit Formats

The system downloads **52 official formats** from the Secretariat of Anti-Corruption and Good Government:

- General audit formats (1-6)
- Procurement formats (7-13)
- Public works formats (14-20)
- Findings and reports formats (21-25)
- Complementary guides and instructions

**Source**: [gob.mx - Audit Formats](https://www.gob.mx/buengobierno/documentos/formatos-guias-e-instructivos-de-los-terminos-de-referencia-para-auditorias-de-los-estados-y-la-informacion-financiera-contable-y-presupues)

## 🚀 Usage

### Automatic Execution (GitHub Actions)

1. Go to the **Actions** tab of the repository
2. Select the **"Government Audit - Download and Certification"** workflow
3. Click on **"Run workflow"**
4. Wait for the execution to finish (~5-10 minutes)
5. Download the package from **Artifacts**

### Local Execution

```bash
# Clone repository
git clone https://github.com/agentesecreto0007/coatlicue.git
cd coatlicue

# Install dependencies
pip install requests

# Run scripts in order
python scripts/01_genesis_verification.py
python scripts/02_download_formats.py
python scripts/03_blockchain_anchoring.py
python scripts/04_nom151_certification.py
python scripts/05_drive_sync.py
python scripts/06_package_notarial.py
```

## 📁 Project Structure

```
coatlicue/
├── .github/workflows/
│   └── auditoria_gubernamental.yml    # GitHub Actions workflow
├── scripts/
│   ├── 01_genesis_verification.py     # Genesis hash verification
│   ├── 02_download_formats.py         # Download formats
│   ├── 03_blockchain_anchoring.py     # Bitcoin anchoring
│   ├── 04_nom151_certification.py     # NOM-151 certification
│   ├── 05_drive_sync.py               # Drive synchronization
│   └── 06_package_notarial.py         # Notarial package
├── docs/
│   ├── ARQUITECTURA.md                # System architecture
│   ├── FUNDAMENTOS_LEGALES.md         # Legal basis
│   └── MANUAL_USUARIO.md              # User guide
├── templates/
│   ├── constancia_nom151.md           # Certificate template
│   └── certificado_notarial.md        # Notarial template
└── README.md                          # This file
```

## 🔐 Genesis Hash

The system uses a **genesis hash** verifiable by anyone:

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This is the **SHA-256 of an empty string**, verifiable with:

```bash
echo -n "" | sha256sum
```

## 🌎 Integration with North America Project

This system integrates with the **North America Forensic Project**, which contains:

- **3,702 files** of government evidence
- **Coverage**: Mexico, USA (50 states), Canada (13 provinces)
- **Types**: Verification reports, screenshots, HTML, metadata

**Location**: Google Drive - `EVIDENCIA_PARA_NOTARIA/`

## 📋 Chain of Custody

Each execution generates an **impeccable chain of custody** that records:

1. **Genesis Hash**: Verifiable starting point
2. **File Download**: URL, timestamp, hash
3. **Blockchain Anchoring**: Timestamp on Bitcoin
4. **NOM-151 Certification**: Conservation certificate
5. **Drive Sync**: Cloud backup
6. **Notarial Package**: Preparation for certification

## ⚖️ Legal Validity

### NOM-151-SCFI-2016

The system complies with **all requirements** of the Official Mexican Standard:

- ✅ Identification of data messages
- ✅ Cryptographic hashes (SHA-256)
- ✅ Timestamps (Bitcoin blockchain)
- ✅ Complete chain of custody
- ✅ Integrity guarantee
- ✅ Verifiable trusted timestamp

### Commerce Code

**Article 89 bis**: Data messages have the same validity as physical documents when their authenticity and integrity are guaranteed.

### SCJN

**Thesis 2026752**: Electronic documents have **full evidentiary value** when their authenticity and integrity are proven by cryptographic methods.

## 🔍 Independent Verification

Anyone can verify:

### 1. Genesis Hash
```bash
echo -n "" | sha256sum
# Must return: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### 2. File Hashes
```bash
sha256sum formatos_descargados/*
# Compare with hashes_archivos.json
```

### 3. Blockchain Timestamps
```bash
ots verify blockchain_proofs/*.ots
# Or use: https://opentimestamps.org/
```

### 4. Chain of Custody
```bash
cat cadena_custodia.json | jq ".events"
# Review all registered events
```

## 📝 Notarization

The system generates a **complete notarial package** for certification at **Notary Public 230 of Mexico City**:

1. **General index**: Complete catalog
2. **Executive summary**: For the notary
3. **Affidavit**: For signature
4. **Chain of custody**: Traceability
5. **Certifications**: NOM-151 and blockchain
6. **Hashes and Merkle tree**: Verification

## 🤖 AI Analysis

The system is prepared for automated analysis with AI:

- **Data extraction**: Read fields from Word/Excel formats
- **Compliance validation**: Verify legal requirements
- **Anomaly detection**: Identify inconsistencies
- **Report generation**: Automated reports
- **Jurisdictional comparison**: Analysis between countries

## 🌐 International Expansion

Next phases:

1. **Mexico**: ✅ Official formats downloaded
2. **United States**: Download equivalent formats (50 states)
3. **Canada**: Download equivalent formats (13 provinces)
4. **Harmonization**: Comparative analysis and recommendations

## 💰 Cost

**ZERO DOLLARS** 🎉

- GitHub Actions: Free for public repos
- OpenTimestamps: Free (Bitcoin anchoring)
- Google Drive: Free (up to 15 GB)
- Scripts: Open source

## 📚 Documentation

- [System Architecture](ARQUITECTURA.md)
- [Legal Requirements NOM-151](requisitos_legales_nom151.md)
- [OpenTimestamps Information](opentimestamps_info.md)
- [Government Site Analysis](analisis_sitio_gob.md)
- [Google Drive Analysis](analisis_drive_notaria.md)

## 🔗 References

- **NOM-151**: https://www.dof.gob.mx/normasOficiales/6499/seeco11_C/seeco11_C.html
- **OpenTimestamps**: https://opentimestamps.org/
- **Bitcoin Blockchain**: https://blockstream.info/
- **SCJN**: https://www.scjn.gob.mx/
- **Official Formats**: https://www.gob.mx/buengobierno/documentos/...

## 🤝 Contributions

This is a public interest project. Contributions are welcome:

1. Fork the repository
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) for more details.

## ⚠️ Disclaimer

This system is a technical tool to facilitate government auditing. The legal interpretation and use of the results are the user's responsibility. It is recommended to consult with legal professionals for specific cases.

---

**Developed with 💚 for transparency and accountability in Mexico**

*"Technology at the service of justice and democracy"*

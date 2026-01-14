# Coatlicue - Sistema de Auditoría Gubernamental

> **Sistema automatizado para auditoría del Estado Mexicano con validez legal máxima ante la SCJN**

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/agentesecreto0007/coatlicue/actions)
[![NOM-151](https://img.shields.io/badge/NOM--151-Cumplimiento-00A86B)](https://www.dof.gob.mx/normasOficiales/6499/seeco11_C/seeco11_C.html)
[![Bitcoin](https://img.shields.io/badge/Bitcoin-Blockchain-F7931A?logo=bitcoin&logoColor=white)](https://opentimestamps.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🎯 Objetivo

**Coatlicue** es un sistema automatizado que descarga, valida y certifica formatos oficiales de auditoría del gobierno mexicano, con **máxima validez legal** ante la Suprema Corte de Justicia de la Nación (SCJN).

El sistema utiliza:
- ✅ **NOM-151-SCFI-2016**: Conservación de mensajes de datos
- ✅ **Blockchain Bitcoin**: Fecha cierta inmutable
- ✅ **OpenTimestamps**: Anclaje criptográfico gratuito
- ✅ **SHA-256**: Hashes criptográficos verificables
- ✅ **Cadena de custodia**: Trazabilidad completa

## 🌟 Características

### Validez Legal
- **NOM-151-SCFI-2016**: Cumplimiento total de normativa mexicana
- **Código de Comercio Art. 89 bis**: Validez de mensajes de datos
- **SCJN Tesis 2026752**: Valor probatorio de documentos electrónicos
- **Blockchain Bitcoin**: Prueba inmutable de existencia

### Tecnología
- **Automatización**: GitHub Actions (costo cero)
- **Blockchain**: Anclaje en Bitcoin mediante OpenTimestamps
- **Criptografía**: SHA-256, Merkle trees
- **Cloud**: Sincronización con Google Drive
- **IA**: Preparado para análisis automatizado

### Seguridad y Privacidad
- **Protección de datos personales**: Sin exposición de información sensible
- **Protección de metadatos**: Anonimización completa
- **Verificación independiente**: Cualquiera puede verificar
- **Código abierto**: Transparencia total

## 📦 Contenido

### Formatos Oficiales de Auditoría

El sistema descarga **52 formatos oficiales** de la Secretaría Anticorrupción y Buen Gobierno:

- Formatos de auditoría general (1-6)
- Formatos de adquisiciones (7-13)
- Formatos de obras públicas (14-20)
- Formatos de hallazgos y reportes (21-25)
- Guías e instructivos complementarios

**Fuente**: [gob.mx - Formatos de Auditoría](https://www.gob.mx/buengobierno/documentos/formatos-guias-e-instructivos-de-los-terminos-de-referencia-para-auditorias-de-los-estados-y-la-informacion-financiera-contable-y-presupues)

## 🚀 Uso

### Ejecución Automática (GitHub Actions)

1. Ve a la pestaña **Actions** del repositorio
2. Selecciona el workflow **"Auditoría Gubernamental - Descarga y Certificación"**
3. Haz clic en **"Run workflow"**
4. Espera a que termine la ejecución (~5-10 minutos)
5. Descarga el paquete desde **Artifacts**

### Ejecución Local

```bash
# Clonar repositorio
git clone https://github.com/agentesecreto0007/coatlicue.git
cd coatlicue

# Instalar dependencias
pip install requests

# Ejecutar scripts en orden
python scripts/01_genesis_verification.py
python scripts/02_download_formats.py
python scripts/03_blockchain_anchoring.py
python scripts/04_nom151_certification.py
python scripts/05_drive_sync.py
python scripts/06_package_notarial.py
```

## 📁 Estructura del Proyecto

```
coatlicue/
├── .github/workflows/
│   └── auditoria_gubernamental.yml    # GitHub Actions workflow
├── scripts/
│   ├── 01_genesis_verification.py     # Verificación hash genesis
│   ├── 02_download_formats.py         # Descarga de formatos
│   ├── 03_blockchain_anchoring.py     # Anclaje en Bitcoin
│   ├── 04_nom151_certification.py     # Certificación NOM-151
│   ├── 05_drive_sync.py               # Sincronización Drive
│   └── 06_package_notarial.py         # Paquete notarial
├── docs/
│   ├── ARQUITECTURA.md                # Arquitectura del sistema
│   ├── FUNDAMENTOS_LEGALES.md         # Base legal
│   └── MANUAL_USUARIO.md              # Guía de uso
├── templates/
│   ├── constancia_nom151.md           # Template constancia
│   └── certificado_notarial.md        # Template notarial
└── README.md                          # Este archivo
```

## 🔐 Hash Genesis

El sistema utiliza un **hash genesis** verificable por cualquiera:

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Este es el **SHA-256 de una cadena vacía**, verificable con:

```bash
echo -n "" | sha256sum
```

## 🌎 Integración con Proyecto Norteamérica

Este sistema se integra con el **Proyecto Pericial Norteamérica** que contiene:

- **3,702 archivos** de evidencia gubernamental
- **Cobertura**: México, EE.UU. (50 estados), Canadá (13 provincias)
- **Tipos**: Reportes de verificación, capturas, HTML, metadatos

**Ubicación**: Google Drive - `EVIDENCIA_PARA_NOTARIA/`

## 📋 Cadena de Custodia

Cada ejecución genera una **cadena de custodia impecable** que registra:

1. **Hash Genesis**: Punto de partida verificable
2. **Descarga de archivos**: URL, timestamp, hash
3. **Anclaje blockchain**: Timestamp en Bitcoin
4. **Certificación NOM-151**: Constancia de conservación
5. **Sincronización Drive**: Backup en la nube
6. **Paquete notarial**: Preparación para certificación

## ⚖️ Validez Legal

### NOM-151-SCFI-2016

El sistema cumple con **todos los requisitos** de la Norma Oficial Mexicana:

- ✅ Identificación de mensajes de datos
- ✅ Hashes criptográficos (SHA-256)
- ✅ Sellos de tiempo (blockchain Bitcoin)
- ✅ Cadena de custodia completa
- ✅ Garantía de integridad
- ✅ Fecha cierta verificable

### Código de Comercio

**Artículo 89 bis**: Los mensajes de datos tienen la misma validez que los documentos físicos cuando se garantiza su autenticidad e integridad.

### SCJN

**Tesis 2026752**: Los documentos electrónicos tienen **pleno valor probatorio** cuando se acredita su autenticidad e integridad mediante métodos criptográficos.

## 🔍 Verificación Independiente

Cualquier persona puede verificar:

### 1. Hash Genesis
```bash
echo -n "" | sha256sum
# Debe dar: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### 2. Hashes de Archivos
```bash
sha256sum formatos_descargados/*
# Comparar con hashes_archivos.json
```

### 3. Timestamps Blockchain
```bash
ots verify blockchain_proofs/*.ots
# O usar: https://opentimestamps.org/
```

### 4. Cadena de Custodia
```bash
cat cadena_custodia.json | jq '.eventos'
# Revisar todos los eventos registrados
```

## 📝 Notarización

El sistema genera un **paquete notarial completo** para certificación en la **Notaría 230 de la Ciudad de México**:

1. **Índice general**: Catálogo completo
2. **Resumen ejecutivo**: Para el notario
3. **Declaración jurada**: Para firma
4. **Cadena de custodia**: Trazabilidad
5. **Certificaciones**: NOM-151 y blockchain
6. **Hashes y Merkle tree**: Verificación

## 🤖 Análisis con IA

El sistema está preparado para análisis automatizado con IA:

- **Extracción de datos**: Leer campos de formatos Word/Excel
- **Validación de cumplimiento**: Verificar requisitos legales
- **Detección de anomalías**: Identificar inconsistencias
- **Generación de reportes**: Informes automatizados
- **Comparación jurisdiccional**: Análisis entre países

## 🌐 Expansión Internacional

Próximas fases:

1. **México**: ✅ Formatos oficiales descargados
2. **Estados Unidos**: Descarga de formatos equivalentes (50 estados)
3. **Canadá**: Descarga de formatos equivalentes (13 provincias)
4. **Armonización**: Análisis comparativo y recomendaciones

## 💰 Costo

**CERO PESOS** 🎉

- GitHub Actions: Gratuito para repos públicos
- OpenTimestamps: Gratuito (anclaje Bitcoin)
- Google Drive: Gratuito (hasta 15 GB)
- Scripts: Open source

## 📚 Documentación

- [Arquitectura del Sistema](ARQUITECTURA.md)
- [Requisitos Legales NOM-151](requisitos_legales_nom151.md)
- [Información OpenTimestamps](opentimestamps_info.md)
- [Análisis Sitio Gubernamental](analisis_sitio_gob.md)
- [Análisis Google Drive](analisis_drive_notaria.md)

## 🔗 Referencias

- **NOM-151**: https://www.dof.gob.mx/normasOficiales/6499/seeco11_C/seeco11_C.html
- **OpenTimestamps**: https://opentimestamps.org/
- **Bitcoin Blockchain**: https://blockstream.info/
- **SCJN**: https://www.scjn.gob.mx/
- **Formatos Oficiales**: https://www.gob.mx/buengobierno/documentos/...

## 🤝 Contribuciones

Este es un proyecto de interés público. Las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer

Este sistema es una herramienta técnica para facilitar la auditoría gubernamental. La interpretación legal y el uso de los resultados son responsabilidad del usuario. Se recomienda consultar con profesionales legales para casos específicos.

---

**Desarrollado con 💚 para la transparencia y rendición de cuentas en México**

*"La tecnología al servicio de la justicia y la democracia"*

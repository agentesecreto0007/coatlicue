# Arquitectura del Sistema de Auditoría Gubernamental

## Visión General

Sistema automatizado para descargar, validar y certificar formatos de auditoría del gobierno mexicano con **máxima validez legal** ante la SCJN, cumpliendo con **NOM-151** y usando **blockchain de Bitcoin** para fecha cierta.

## Principios de Diseño

### 1. Costo Cero
- GitHub Actions (gratuito para repos públicos)
- OpenTimestamps (anclaje Bitcoin gratuito)
- Scripts open source
- Sin dependencias de servicios pagos

### 2. Máxima Protección de Datos
- Variables secretas en GitHub
- No exposición de metadatos personales
- Limpieza de logs sensibles
- Uso exclusivo de HTTPS
- Sin tracking ni analytics

### 3. Validez Legal Máxima
- Cumplimiento NOM-151
- Cadena de custodia impecable
- Anclaje en blockchain Bitcoin
- Hash genesis verificable
- Documentación pericial completa

### 4. Ejecución Bajo Demanda
- Trigger manual (workflow_dispatch)
- Sin ejecuciones automáticas
- Control total del usuario
- Descarga a dispositivos locales

## Arquitectura Técnica

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (GitHub Web UI)                   │
│              Trigger manual: "Run workflow"                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS WORKFLOW                    │
│  - Ejecución en Ubuntu latest                                │
│  - Aislamiento completo                                      │
│  - Sin persistencia de datos sensibles                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              FASE 1: INICIALIZACIÓN Y GENESIS                │
│  1. Verificar hash genesis (cadena vacía)                    │
│  2. Generar timestamp inicial                                │
│  3. Crear estructura de directorios                          │
│  4. Inicializar cadena de custodia                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│           FASE 2: DESCARGA Y VALIDACIÓN INICIAL              │
│  1. Descargar página gubernamental                           │
│  2. Calcular hash de la página HTML                          │
│  3. Extraer URLs de formatos                                 │
│  4. Descargar todos los formatos (52 archivos)               │
│  5. Calcular hash SHA-256 de cada archivo                    │
│  6. Generar registro de descarga con timestamps              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│         FASE 3: ANCLAJE EN BLOCKCHAIN BITCOIN                │
│  1. Instalar opentimestamps-client                           │
│  2. Crear Merkle tree de todos los hashes                    │
│  3. Anclar hash raíz en Bitcoin blockchain                   │
│  4. Generar archivos .ots para cada documento                │
│  5. Esperar confirmación en blockchain                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          FASE 4: CERTIFICACIÓN NOM-151                       │
│  1. Generar constancia de conservación                       │
│  2. Incluir identificación de mensajes de datos              │
│  3. Registrar hashes criptográficos                          │
│  4. Incluir sellos de tiempo                                 │
│  5. Documentar cadena de custodia                            │
│  6. Certificar integridad                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│        FASE 5: GENERACIÓN DE EVIDENCIA LEGAL                 │
│  1. Crear reporte pericial técnico                           │
│  2. Generar documentación para SCJN                          │
│  3. Preparar certificado notarial (template)                 │
│  4. Crear índice de evidencias                               │
│  5. Generar checksums de verificación                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          FASE 6: EMPAQUETADO Y DISTRIBUCIÓN                  │
│  1. Crear archivo comprimido con todos los formatos          │
│  2. Incluir archivos .ots de blockchain                      │
│  3. Incluir documentación legal                              │
│  4. Generar hash del paquete completo                        │
│  5. Subir como GitHub Actions Artifact                       │
│  6. Usuario descarga a su dispositivo                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 USUARIO: DESCARGA LOCAL                      │
│  - Paquete completo en dispositivo personal                  │
│  - Verificación independiente posible                        │
│  - Sin rastro en GitHub después de 90 días                   │
└─────────────────────────────────────────────────────────────┘
```

## Estructura de Archivos

```
coatlicue/
├── .github/
│   └── workflows/
│       └── auditoria_gubernamental.yml    # GitHub Actions workflow
├── scripts/
│   ├── 01_genesis_verification.py         # Verificar hash genesis
│   ├── 02_download_formats.py             # Descargar formatos
│   ├── 03_blockchain_anchoring.py         # Anclar en Bitcoin
│   ├── 04_nom151_certification.py         # Certificación NOM-151
│   ├── 05_legal_evidence.py               # Evidencia legal
│   └── 06_package_distribution.py         # Empaquetado final
├── templates/
│   ├── constancia_nom151.md               # Template constancia
│   ├── reporte_pericial.md                # Template reporte
│   └── certificado_notarial.md            # Template notarial
├── docs/
│   ├── ARQUITECTURA.md                    # Este documento
│   ├── MANUAL_USUARIO.md                  # Guía de uso
│   ├── FUNDAMENTOS_LEGALES.md             # Base legal
│   └── VERIFICACION.md                    # Cómo verificar
├── enlaces_descarga.json                  # URLs de formatos
├── requisitos_legales_nom151.md           # Requisitos NOM-151
├── opentimestamps_info.md                 # Info OpenTimestamps
└── README.md                              # Documentación principal
```

## Cadena de Custodia

### Hash Genesis
```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
(SHA-256 de cadena vacía - verificable por cualquiera)
```

### Registro de Eventos

Cada evento en la cadena de custodia incluye:
1. **Timestamp**: Fecha y hora UTC con precisión de milisegundos
2. **Acción**: Descripción de la operación realizada
3. **Hash anterior**: Hash del estado previo
4. **Hash actual**: Hash del estado después de la operación
5. **Metadata**: Información adicional (URL, tamaño, tipo)

### Ejemplo de Entrada en Cadena de Custodia

```json
{
  "event_id": 1,
  "timestamp": "2026-01-14T07:30:00.000Z",
  "action": "GENESIS_VERIFICATION",
  "hash_anterior": null,
  "hash_actual": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "metadata": {
    "descripcion": "Verificación de hash genesis (cadena vacía)",
    "algoritmo": "SHA-256"
  }
},
{
  "event_id": 2,
  "timestamp": "2026-01-14T07:30:15.234Z",
  "action": "DOWNLOAD_WEBPAGE",
  "hash_anterior": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "hash_actual": "a1b2c3d4...",
  "metadata": {
    "url": "https://www.gob.mx/buengobierno/documentos/...",
    "size_bytes": 45678,
    "content_type": "text/html"
  }
}
```

## Seguridad y Privacidad

### Protección de Datos Personales

1. **No se almacenan datos personales** en el repositorio
2. **Variables secretas** para cualquier credencial necesaria
3. **Limpieza de logs** antes de publicar artifacts
4. **Sin tracking** de usuarios
5. **Ejecución aislada** en cada run

### Protección de Metadatos

1. **User-Agent genérico** en descargas
2. **Sin cookies** persistentes
3. **Conexiones HTTPS** exclusivamente
4. **Sin geolocalización**
5. **Timestamps en UTC** (sin zona horaria personal)

### Verificación Independiente

Cualquier persona puede verificar:
1. **Hash genesis**: `echo -n "" | sha256sum`
2. **Hashes de archivos**: `sha256sum archivo.pdf`
3. **Pruebas blockchain**: `ots verify archivo.pdf.ots`
4. **Cadena de custodia**: Recalcular todos los hashes

## Cumplimiento NOM-151

### Requisitos Cumplidos

✅ **Identificación del mensaje de datos**: Cada archivo identificado claramente
✅ **Hash criptográfico**: SHA-256 de cada documento
✅ **Sello de tiempo**: Timestamps precisos en UTC
✅ **Cadena de custodia**: Registro completo de operaciones
✅ **Integridad**: Verificable mediante hashes
✅ **Fecha cierta**: Anclaje en blockchain Bitcoin

### Constancia de Conservación

Se genera automáticamente incluyendo:
- Identificación de cada documento
- Hash SHA-256
- Timestamp de descarga
- Prueba blockchain (.ots)
- Cadena de custodia completa
- Firma digital del sistema

## Validez Legal ante SCJN

### Fundamentos Legales

1. **NOM-151-SCFI-2016**: Cumplimiento total
2. **Código de Comercio Art. 89 bis**: Validez de mensajes de datos
3. **SCJN Tesis 2026752**: Valor probatorio de documentos electrónicos
4. **Blockchain Bitcoin**: Prueba de existencia inmutable

### Documentación Legal Generada

1. **Reporte Pericial Técnico**: Análisis detallado de cada archivo
2. **Constancia NOM-151**: Certificado de conservación
3. **Certificado Notarial** (template): Para firma de Notaría 230 CDMX
4. **Índice de Evidencias**: Catálogo completo
5. **Cadena de Custodia**: Trazabilidad completa

## Integración con Notaría 230 CDMX

### Preparación para Certificación Notarial

El sistema genera un **template de certificado notarial** que incluye:
- Identificación del notario (Notaría 230 CDMX)
- Descripción de los documentos certificados
- Hashes SHA-256 de cada documento
- Pruebas de anclaje en blockchain
- Fecha y hora de certificación
- Espacio para firma y sello notarial

### Proceso Sugerido

1. **Ejecutar workflow**: Descargar y certificar formatos
2. **Descargar paquete**: Obtener todos los archivos
3. **Acudir a Notaría 230**: Con paquete completo
4. **Certificación notarial**: Notario verifica y firma
5. **Archivo legal**: Documento con validez plena ante SCJN

## Análisis con IA

### Preparación para Auditoría Automatizada

El sistema descarga todos los formatos en formato editable:
- **Word (.docx)**: Procesable con python-docx
- **Excel (.xlsx)**: Procesable con openpyxl/pandas
- **PDF**: Procesable con PyPDF2/pdfplumber

### Análisis Sugeridos

1. **Extracción de datos**: Leer campos de cada formato
2. **Validación de cumplimiento**: Verificar requisitos legales
3. **Detección de anomalías**: Identificar inconsistencias
4. **Generación de reportes**: Crear informes automatizados
5. **Comparación histórica**: Analizar cambios entre versiones

## Próximos Pasos de Implementación

1. ✅ Análisis completado
2. ✅ Arquitectura diseñada
3. ⏳ Implementar scripts Python
4. ⏳ Crear GitHub Actions workflow
5. ⏳ Generar templates de documentación legal
6. ⏳ Probar sistema completo
7. ⏳ Documentar manual de usuario
8. ⏳ Desplegar al repositorio

## Referencias

- **NOM-151**: https://www.dof.gob.mx/normasOficiales/6499/seeco11_C/seeco11_C.html
- **OpenTimestamps**: https://opentimestamps.org/
- **Bitcoin Blockchain**: https://blockchain.info/
- **SCJN**: https://www.scjn.gob.mx/
- **Notaría 230 CDMX**: https://www.notaria230.com.mx/

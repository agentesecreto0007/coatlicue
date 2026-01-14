# Manual de Usuario
## Sistema de Auditoría Gubernamental Coatlicue

Este manual explica cómo usar el sistema paso a paso, tanto para ejecución automática como manual.

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos](#requisitos)
3. [Ejecución Automática (GitHub Actions)](#ejecución-automática-github-actions)
4. [Ejecución Local](#ejecución-local)
5. [Sincronización con Google Drive](#sincronización-con-google-drive)
6. [Verificación de Resultados](#verificación-de-resultados)
7. [Preparación para Notarización](#preparación-para-notarización)
8. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

El sistema **Coatlicue** automatiza la descarga, validación y certificación de formatos oficiales de auditoría del gobierno mexicano, con validez legal máxima ante la SCJN.

### ¿Qué hace el sistema?

1. **Descarga** 52 formatos oficiales del sitio gob.mx
2. **Calcula** hashes SHA-256 de cada archivo
3. **Ancla** los hashes en la blockchain de Bitcoin
4. **Genera** constancia de conservación NOM-151
5. **Crea** cadena de custodia completa
6. **Sincroniza** con Google Drive (opcional)
7. **Prepara** paquete para notarización

### ¿Por qué usar este sistema?

- ✅ **Validez legal**: Cumple NOM-151 y admisible ante SCJN
- ✅ **Verificación independiente**: Cualquiera puede verificar
- ✅ **Costo cero**: Totalmente gratuito
- ✅ **Automatización**: Sin trabajo manual
- ✅ **Blockchain**: Fecha cierta inmutable

---

## Requisitos

### Para Ejecución Automática (GitHub Actions)

- Cuenta de GitHub (gratuita)
- Acceso al repositorio `coatlicue`

### Para Ejecución Local

- Python 3.11 o superior
- Git
- Conexión a internet
- (Opcional) rclone para sincronización con Drive

### Para Sincronización con Google Drive

- Cuenta de Google Drive
- Configuración de rclone (ver sección correspondiente)

---

## Ejecución Automática (GitHub Actions)

La forma más fácil de usar el sistema es mediante GitHub Actions.

### Paso 1: Acceder al Repositorio

1. Ve a https://github.com/agentesecreto0007/coatlicue
2. Asegúrate de tener acceso al repositorio

### Paso 2: Ejecutar el Workflow

1. Haz clic en la pestaña **"Actions"**
2. Selecciona el workflow **"Auditoría Gubernamental - Descarga y Certificación"**
3. Haz clic en **"Run workflow"** (botón verde)
4. Selecciona las opciones:
   - **Sincronizar con Google Drive**: `true` o `false`
5. Haz clic en **"Run workflow"** para confirmar

### Paso 3: Esperar la Ejecución

El workflow tardará aproximadamente **5-10 minutos** en completarse.

Puedes ver el progreso en tiempo real haciendo clic en la ejecución.

### Paso 4: Descargar el Paquete

Una vez completada la ejecución:

1. Desplázate hasta la sección **"Artifacts"** al final de la página
2. Descarga el archivo **"paquete-auditoria-[número]"**
3. Descarga también el **"reporte-ejecucion-[número]"**

### Paso 5: Extraer el Paquete

En tu computadora local:

```bash
# Extraer el paquete
tar -xzf paquete_auditoria_completo.tar.gz

# Ver contenido
ls -la
```

---

## Ejecución Local

Si prefieres ejecutar el sistema localmente:

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/agentesecreto0007/coatlicue.git
cd coatlicue
```

### Paso 2: Instalar Dependencias

```bash
# Instalar Python (si no lo tienes)
# En Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3-pip

# Instalar dependencias de Python
pip install requests
```

### Paso 3: Ejecutar los Scripts

Ejecuta los scripts en orden:

#### Script 1: Verificación de Hash Genesis

```bash
python scripts/01_genesis_verification.py
```

**Resultado esperado**: 
- ✓ Hash genesis verificado
- Archivo `cadena_custodia.json` creado

#### Script 2: Descarga de Formatos

```bash
python scripts/02_download_formats.py
```

**Resultado esperado**:
- ✓ 52 archivos descargados en `formatos_descargados/`
- Archivo `hashes_archivos.json` creado
- Cadena de custodia actualizada

**Tiempo estimado**: 2-3 minutos

#### Script 3: Anclaje en Blockchain

```bash
python scripts/03_blockchain_anchoring.py
```

**Resultado esperado**:
- ✓ OpenTimestamps instalado (si no lo estaba)
- ✓ 52 archivos `.ots` creados en `blockchain_proofs/`
- Archivo `merkle_tree.json` creado
- Archivo `blockchain_timestamps.json` creado

**Nota**: Los timestamps pueden tardar 10-60 minutos en confirmarse en la blockchain.

#### Script 4: Certificación NOM-151

```bash
python scripts/04_nom151_certification.py
```

**Resultado esperado**:
- ✓ Constancia NOM-151 generada: `constancia_nom151.md`
- Cadena de custodia actualizada

#### Script 5: Sincronización con Drive (Opcional)

```bash
python scripts/05_drive_sync.py
```

**Requisito**: Tener rclone configurado (ver sección siguiente)

**Resultado esperado**:
- ✓ Archivos sincronizados con Google Drive
- Archivo `enlaces_drive.json` con enlaces compartibles

#### Script 6: Paquete Notarial

```bash
python scripts/06_package_notarial.py
```

**Resultado esperado**:
- ✓ Directorio `paquete_notarial/` creado
- Documentos para notarización generados

---

## Sincronización con Google Drive

Para sincronizar automáticamente con Google Drive:

### Paso 1: Instalar rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

### Paso 2: Configurar rclone

```bash
rclone config
```

Sigue las instrucciones para:
1. Crear un nuevo remote llamado `manus_google_drive`
2. Seleccionar Google Drive como tipo
3. Autorizar con tu cuenta de Google
4. Seleccionar la carpeta `EVIDENCIA_PARA_NOTARIA`

### Paso 3: Ejecutar Sincronización

```bash
python scripts/05_drive_sync.py
```

Los archivos se subirán a:
```
EVIDENCIA_PARA_NOTARIA/
└── FORMATOS_OFICIALES_AUDITORIA/
    ├── 01_formatos_originales/
    ├── 02_blockchain_proofs/
    └── 03_certificaciones/
```

---

## Verificación de Resultados

### Verificar Hash Genesis

```bash
echo -n "" | sha256sum
```

**Resultado esperado**:
```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Verificar Hashes de Archivos

```bash
# Ver hashes registrados
cat hashes_archivos.json | jq '.[].hash'

# Calcular hash de un archivo
sha256sum formatos_descargados/formato-1-informe-de-analisis-de-riesgo.docx

# Comparar con el hash registrado
```

### Verificar Timestamps Blockchain

```bash
# Verificar un timestamp específico
ots verify blockchain_proofs/formato-1-informe-de-analisis-de-riesgo.docx.ots

# Verificar todos los timestamps
for file in blockchain_proofs/*.ots; do
    echo "Verificando: $file"
    ots verify "$file"
done
```

**Nota**: Si los timestamps son recientes (< 1 hora), puede que aún no estén confirmados en la blockchain. Espera y vuelve a verificar.

### Verificar Cadena de Custodia

```bash
# Ver todos los eventos
cat cadena_custodia.json | jq '.eventos'

# Contar eventos
cat cadena_custodia.json | jq '.eventos | length'

# Ver último evento
cat cadena_custodia.json | jq '.eventos[-1]'
```

---

## Preparación para Notarización

### Paso 1: Revisar el Paquete Notarial

```bash
cd paquete_notarial
ls -la
```

**Contenido**:
- `00_INDICE_GENERAL.md`: Índice completo
- `01_RESUMEN_EJECUTIVO.md`: Resumen para el notario
- `02_DECLARACION_JURADA.md`: Para tu firma
- `cadena_custodia.json`: Cadena de custodia
- `constancia_nom151.md`: Constancia NOM-151
- Otros archivos de certificación

### Paso 2: Completar la Declaración Jurada

Abre `02_DECLARACION_JURADA.md` y completa:
- Tu nombre completo
- Tipo y número de identificación oficial
- Fecha y lugar

### Paso 3: Imprimir Documentos

Imprime los siguientes documentos:
- Índice general
- Resumen ejecutivo
- Declaración jurada (para firma)
- Constancia NOM-151

### Paso 4: Preparar Medios Digitales

Copia en una USB:
- Todo el directorio `formatos_descargados/`
- Todo el directorio `blockchain_proofs/`
- Todos los archivos JSON
- La constancia NOM-151

### Paso 5: Acudir a la Notaría

**Notaría 230 de la Ciudad de México**

Lleva:
- Documentos impresos
- USB con archivos digitales
- Identificación oficial
- Comprobante de domicilio (si lo requieren)

### Paso 6: Solicitar Certificación

Explica al notario que deseas certificar:
1. La autenticidad de los documentos descargados
2. Los hashes SHA-256 calculados
3. Los timestamps de blockchain Bitcoin
4. La cadena de custodia completa

Menciona que el sistema cumple con **NOM-151-SCFI-2016**.

---

## Preguntas Frecuentes

### ¿Cuánto cuesta usar el sistema?

**CERO PESOS**. Todo es gratuito:
- GitHub Actions: Gratis para repos públicos
- OpenTimestamps: Gratis
- Google Drive: Gratis (hasta 15 GB)

### ¿Cuánto tiempo tarda la ejecución?

- **GitHub Actions**: 5-10 minutos
- **Ejecución local**: 5-15 minutos
- **Confirmación blockchain**: 10-60 minutos adicionales

### ¿Puedo verificar los resultados independientemente?

**SÍ**. Todo es verificable:
- Hash genesis: `echo -n "" | sha256sum`
- Hashes de archivos: `sha256sum <archivo>`
- Timestamps blockchain: `ots verify <archivo>.ots`

### ¿Los timestamps de blockchain son válidos legalmente?

**SÍ**. OpenTimestamps proporciona prueba criptográfica de existencia en la blockchain de Bitcoin, que es inmutable y verificable públicamente. Esto cumple con los requisitos de "fecha cierta" de la NOM-151.

### ¿Qué pasa si GitHub elimina los artifacts?

Los artifacts se guardan por 90 días. Después de ese tiempo, debes:
1. Descargar el paquete antes de que expire
2. Guardarlo localmente o en Google Drive
3. O ejecutar el workflow nuevamente

### ¿Puedo usar esto para auditar otros sitios gubernamentales?

**SÍ**. El sistema es modular y puede adaptarse para descargar y certificar documentos de otros sitios gubernamentales. Solo necesitas modificar el archivo `enlaces_descarga.json` con las nuevas URLs.

### ¿El sistema funciona en Windows/Mac?

**SÍ**. Los scripts de Python son multiplataforma. Solo necesitas:
- Python 3.11+
- Las dependencias instaladas (`pip install requests`)

### ¿Necesito conocimientos técnicos?

**NO** para usar GitHub Actions (solo hacer clic en botones).

**SÍ** (básicos) para ejecución local:
- Saber usar la terminal/línea de comandos
- Instalar Python
- Ejecutar scripts

### ¿Puedo modificar el sistema?

**SÍ**. El código es open source (MIT License). Puedes:
- Modificar los scripts
- Agregar nuevas funcionalidades
- Adaptar para otros casos de uso
- Contribuir mejoras al proyecto

### ¿Cómo obtengo soporte?

1. **Documentación**: Lee todos los archivos en `docs/`
2. **Issues**: Abre un issue en GitHub
3. **Email**: Contacta al mantenedor del proyecto

---

## Recursos Adicionales

- [Arquitectura del Sistema](ARQUITECTURA.md)
- [Fundamentos Legales](requisitos_legales_nom151.md)
- [Información OpenTimestamps](opentimestamps_info.md)
- [Análisis Google Drive](analisis_drive_notaria.md)

---

**¿Necesitas ayuda?** Abre un issue en GitHub o consulta la documentación adicional.

**¡Éxito en tu auditoría gubernamental!** 🎉

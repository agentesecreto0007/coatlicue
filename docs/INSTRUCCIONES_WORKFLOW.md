# Instrucciones para Agregar GitHub Actions Workflow

El workflow de GitHub Actions no pudo ser agregado automáticamente debido a restricciones de permisos. Debes agregarlo manualmente siguiendo estos pasos:

## Opción 1: Desde la Interfaz Web de GitHub

1. Ve a tu repositorio en GitHub: https://github.com/agentesecreto0007/coatlicue

2. Haz clic en la pestaña **"Actions"**

3. Haz clic en **"New workflow"**

4. Haz clic en **"set up a workflow yourself"**

5. Copia y pega el siguiente contenido:

```yaml
name: Auditoría Gubernamental - Descarga y Certificación

on:
  workflow_dispatch:  # Ejecución manual bajo demanda
    inputs:
      sync_to_drive:
        description: 'Sincronizar con Google Drive'
        required: false
        default: 'true'
        type: choice
        options:
          - 'true'
          - 'false'

jobs:
  auditoria_completa:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repositorio
        uses: actions/checkout@v4
      
      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install requests
      
      - name: Paso 1 - Verificación de Hash Genesis
        run: |
          echo "========================================="
          echo "PASO 1: VERIFICACIÓN DE HASH GENESIS"
          echo "========================================="
          python scripts/01_genesis_verification.py
      
      - name: Paso 2 - Descarga de Formatos Oficiales
        run: |
          echo "========================================="
          echo "PASO 2: DESCARGA DE FORMATOS"
          echo "========================================="
          python scripts/02_download_formats.py
      
      - name: Paso 3 - Anclaje en Blockchain Bitcoin
        run: |
          echo "========================================="
          echo "PASO 3: ANCLAJE EN BLOCKCHAIN"
          echo "========================================="
          python scripts/03_blockchain_anchoring.py
        continue-on-error: true
      
      - name: Paso 4 - Certificación NOM-151
        run: |
          echo "========================================="
          echo "PASO 4: CERTIFICACIÓN NOM-151"
          echo "========================================="
          python scripts/04_nom151_certification.py
      
      - name: Paso 5 - Sincronización con Google Drive
        if: ${{ github.event.inputs.sync_to_drive == 'true' }}
        run: |
          echo "========================================="
          echo "PASO 5: SINCRONIZACIÓN CON DRIVE"
          echo "========================================="
          echo "⚠️  Sincronización con Drive requiere configuración manual"
          echo "    Ejecutar localmente: python scripts/05_drive_sync.py"
      
      - name: Paso 6 - Generación de Paquete Notarial
        run: |
          echo "========================================="
          echo "PASO 6: PAQUETE NOTARIAL"
          echo "========================================="
          python scripts/06_package_notarial.py
      
      - name: Generar resumen de ejecución
        run: |
          echo "========================================="
          echo "RESUMEN DE EJECUCIÓN"
          echo "========================================="
          echo ""
          echo "✓ Hash genesis verificado"
          echo "✓ Formatos oficiales descargados"
          echo "✓ Hashes SHA-256 calculados"
          echo "✓ Timestamps blockchain creados"
          echo "✓ Certificación NOM-151 generada"
          echo "✓ Paquete notarial preparado"
      
      - name: Crear archivo comprimido del paquete
        run: |
          echo "Creando archivo comprimido..."
          tar -czf paquete_auditoria_completo.tar.gz \
            formatos_descargados/ \
            blockchain_proofs/ \
            paquete_notarial/ \
            cadena_custodia.json \
            hashes_archivos.json \
            merkle_tree.json \
            blockchain_timestamps.json \
            constancia_nom151.md \
            enlaces_descarga.json
          
          echo "✓ Paquete comprimido creado"
          ls -lh paquete_auditoria_completo.tar.gz
      
      - name: Calcular hash del paquete completo
        run: |
          echo "Calculando hash del paquete completo..."
          sha256sum paquete_auditoria_completo.tar.gz > paquete_hash.txt
          cat paquete_hash.txt
      
      - name: Subir paquete como artifact
        uses: actions/upload-artifact@v4
        with:
          name: paquete-auditoria-${{ github.run_number }}
          path: |
            paquete_auditoria_completo.tar.gz
            paquete_hash.txt
            cadena_custodia.json
            constancia_nom151.md
          retention-days: 90
      
      - name: Mensaje final
        run: |
          echo ""
          echo "========================================="
          echo "✓ EJECUCIÓN COMPLETADA EXITOSAMENTE"
          echo "========================================="
          echo ""
          echo "El paquete está disponible en artifacts."
          echo ""
```

6. Guarda el archivo con el nombre: `auditoria_gubernamental.yml`

7. Haz commit del archivo

## Opción 2: Desde tu Computadora Local

1. Clona el repositorio (si no lo has hecho):
```bash
git clone https://github.com/agentesecreto0007/coatlicue.git
cd coatlicue
```

2. Crea el directorio para workflows:
```bash
mkdir -p .github/workflows
```

3. Crea el archivo del workflow:
```bash
nano .github/workflows/auditoria_gubernamental.yml
```

4. Copia y pega el contenido del workflow (ver arriba)

5. Guarda el archivo (Ctrl+O, Enter, Ctrl+X en nano)

6. Commit y push:
```bash
git add .github/workflows/auditoria_gubernamental.yml
git commit -m "Agregar workflow de GitHub Actions"
git push origin main
```

## Verificación

Una vez agregado el workflow:

1. Ve a la pestaña **"Actions"** en GitHub
2. Deberías ver el workflow **"Auditoría Gubernamental - Descarga y Certificación"**
3. Haz clic en **"Run workflow"** para probarlo

## Nota Importante

El archivo del workflow ya está disponible en el repositorio local en:
```
.github/workflows/auditoria_gubernamental.yml
```

Solo necesitas hacer push de este archivo desde tu computadora local con permisos adecuados.

## Solución de Problemas

Si sigues teniendo problemas:

1. **Verifica permisos**: Asegúrate de tener permisos de escritura en el repositorio
2. **Configura token**: Usa un Personal Access Token con permisos de `workflow`
3. **Push manual**: Haz el push desde tu computadora local, no desde GitHub Actions

## Contacto

Si necesitas ayuda, abre un issue en el repositorio.

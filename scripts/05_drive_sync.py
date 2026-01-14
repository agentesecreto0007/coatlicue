#!/usr/bin/env python3
"""
Script 5: Sincronización con Google Drive
Parte del Sistema de Auditoría Gubernamental con Validez Legal

Este script sincroniza todos los archivos descargados, pruebas blockchain,
y certificaciones con la carpeta de Google Drive para preparación de
paquete notarial.
"""

import subprocess
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Configuración
DRIVE_REMOTE = "manus_google_drive:EVIDENCIA_PARA_NOTARIA/FORMATOS_OFICIALES_AUDITORIA"
RCLONE_CONFIG = "/home/ubuntu/.gdrive-rclone.ini"
CADENA_CUSTODIA_JSON = "cadena_custodia.json"

# Directorios a sincronizar
DIRECTORIOS_SYNC = {
    "formatos_descargados": "01_formatos_originales",
    "blockchain_proofs": "02_blockchain_proofs",
    ".": "03_certificaciones"  # Archivos raíz (constancia, hashes, etc.)
}

def cargar_cadena_custodia():
    """Carga la cadena de custodia existente"""
    with open(CADENA_CUSTODIA_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_cadena_custodia(cadena):
    """Guarda la cadena de custodia actualizada"""
    with open(CADENA_CUSTODIA_JSON, 'w', encoding='utf-8') as f:
        json.dump(cadena, f, indent=2, ensure_ascii=False)

def agregar_evento_cadena(cadena, accion, hash_actual, metadata):
    """Agrega un evento a la cadena de custodia"""
    ultimo_evento = cadena["eventos"][-1]
    nuevo_id = ultimo_evento["event_id"] + 1
    
    evento = {
        "event_id": nuevo_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": accion,
        "hash_anterior": ultimo_evento["hash_actual"],
        "hash_actual": hash_actual,
        "metadata": metadata
    }
    
    cadena["eventos"].append(evento)

def ejecutar_rclone(comando):
    """Ejecuta un comando rclone"""
    cmd_completo = comando + [f"--config={RCLONE_CONFIG}"]
    
    try:
        result = subprocess.run(cmd_completo,
                              capture_output=True,
                              text=True,
                              timeout=300)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout al ejecutar rclone"
    except Exception as e:
        return False, str(e)

def sincronizar_directorio(origen, destino_remoto):
    """Sincroniza un directorio local con Google Drive"""
    print(f"\nSincronizando: {origen} -> {destino_remoto}")
    
    # Crear directorio remoto si no existe
    cmd_mkdir = ['rclone', 'mkdir', f"{DRIVE_REMOTE}/{destino_remoto}"]
    ejecutar_rclone(cmd_mkdir)
    
    # Sincronizar archivos
    if origen == ".":
        # Para archivos raíz, copiar archivos específicos
        archivos_raiz = [
            "cadena_custodia.json",
            "hashes_archivos.json",
            "merkle_tree.json",
            "blockchain_timestamps.json",
            "constancia_nom151.md"
        ]
        
        for archivo in archivos_raiz:
            if os.path.exists(archivo):
                cmd_copy = ['rclone', 'copy', archivo, 
                           f"{DRIVE_REMOTE}/{destino_remoto}/"]
                exito, mensaje = ejecutar_rclone(cmd_copy)
                
                if exito:
                    print(f"  ✓ {archivo}")
                else:
                    print(f"  ✗ {archivo}: {mensaje}")
    else:
        # Para directorios, sincronizar todo el contenido
        cmd_sync = ['rclone', 'sync', origen, 
                   f"{DRIVE_REMOTE}/{destino_remoto}/"]
        exito, mensaje = ejecutar_rclone(cmd_sync)
        
        if exito:
            print(f"  ✓ Sincronización completada")
        else:
            print(f"  ✗ Error: {mensaje}")
            return False
    
    return True

def generar_enlaces_compartibles():
    """Genera enlaces compartibles de los archivos principales"""
    print("\nGenerando enlaces compartibles...")
    
    enlaces = {}
    
    archivos_principales = [
        "03_certificaciones/constancia_nom151.md",
        "03_certificaciones/cadena_custodia.json"
    ]
    
    for archivo in archivos_principales:
        ruta_completa = f"{DRIVE_REMOTE}/{archivo}"
        cmd_link = ['rclone', 'link', ruta_completa]
        exito, enlace = ejecutar_rclone(cmd_link)
        
        if exito:
            enlace_limpio = enlace.strip()
            enlaces[archivo] = enlace_limpio
            print(f"  ✓ {archivo}")
            print(f"    {enlace_limpio}")
        else:
            print(f"  ✗ {archivo}: No se pudo generar enlace")
    
    # Guardar enlaces
    with open("enlaces_drive.json", 'w', encoding='utf-8') as f:
        json.dump(enlaces, f, indent=2, ensure_ascii=False)
    
    return enlaces

def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("SINCRONIZACIÓN CON GOOGLE DRIVE")
    print("Preparación de paquete para Notaría 230 CDMX")
    print("=" * 80)
    
    # Cargar cadena de custodia
    cadena = cargar_cadena_custodia()
    
    # Sincronizar cada directorio
    print("\nIniciando sincronización con Google Drive...")
    print(f"Destino: {DRIVE_REMOTE}")
    
    exitosos = 0
    fallidos = 0
    
    for origen, destino in DIRECTORIOS_SYNC.items():
        if origen != "." and not os.path.exists(origen):
            print(f"\n⚠ Directorio no encontrado: {origen}")
            fallidos += 1
            continue
        
        if sincronizar_directorio(origen, destino):
            exitosos += 1
        else:
            fallidos += 1
    
    # Generar enlaces compartibles
    enlaces = generar_enlaces_compartibles()
    
    # Registrar en cadena de custodia
    import hashlib
    hash_sync = hashlib.sha256(json.dumps(enlaces).encode('utf-8')).hexdigest()
    
    metadata = {
        "descripcion": "Sincronización con Google Drive",
        "destino": DRIVE_REMOTE,
        "directorios_sincronizados": exitosos,
        "directorios_fallidos": fallidos,
        "enlaces_generados": len(enlaces)
    }
    
    agregar_evento_cadena(cadena, "SYNC_GOOGLE_DRIVE", hash_sync, metadata)
    guardar_cadena_custodia(cadena)
    
    # Resumen
    print("\n" + "=" * 80)
    print("SINCRONIZACIÓN COMPLETADA")
    print("=" * 80)
    print(f"\nDirectorios sincronizados: {exitosos}")
    print(f"Directorios con error: {fallidos}")
    print(f"Enlaces compartibles generados: {len(enlaces)}")
    print()
    print(f"Ubicación en Drive: {DRIVE_REMOTE}")
    print(f"Enlaces guardados en: enlaces_drive.json")
    print()
    print("Estructura en Drive:")
    print("  FORMATOS_OFICIALES_AUDITORIA/")
    print("    ├── 01_formatos_originales/      (52 archivos)")
    print("    ├── 02_blockchain_proofs/        (archivos .ots)")
    print("    └── 03_certificaciones/          (constancias y hashes)")
    print()
    print("Próximo paso: Ejecutar 06_package_notarial.py")
    print()

if __name__ == "__main__":
    main()

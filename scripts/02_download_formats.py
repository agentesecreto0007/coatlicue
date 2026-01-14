#!/usr/bin/env python3
"""
Script 2: Descarga de Formatos Oficiales de Auditoría
Parte del Sistema de Auditoría Gubernamental con Validez Legal

Este script descarga todos los formatos oficiales del sitio gob.mx,
calcula hashes SHA-256, y registra todo en la cadena de custodia.
"""

import requests
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# Configuración
ENLACES_JSON = "enlaces_descarga.json"
CADENA_CUSTODIA_JSON = "cadena_custodia.json"
DIR_DESCARGAS = "formatos_descargados"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

def cargar_enlaces():
    """Carga los enlaces de descarga desde el archivo JSON"""
    with open(ENLACES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_cadena_custodia():
    """Carga la cadena de custodia existente"""
    with open(CADENA_CUSTODIA_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_cadena_custodia(cadena):
    """Guarda la cadena de custodia actualizada"""
    with open(CADENA_CUSTODIA_JSON, 'w', encoding='utf-8') as f:
        json.dump(cadena, f, indent=2, ensure_ascii=False)

def calcular_hash_archivo(ruta_archivo):
    """Calcula el hash SHA-256 de un archivo"""
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def obtener_nombre_archivo_limpio(url, texto):
    """Genera un nombre de archivo limpio y descriptivo"""
    # Extraer nombre del archivo de la URL
    parsed = urlparse(url)
    nombre_original = os.path.basename(parsed.path)
    
    # Si el texto es descriptivo, usarlo como prefijo
    if texto and texto not in ["Word", "Excel", "PDF"]:
        # Limpiar el texto para usarlo como nombre
        texto_limpio = texto.replace(" ", "_").replace("/", "_")
        texto_limpio = "".join(c for c in texto_limpio if c.isalnum() or c in "_-")
        
        # Obtener extensión del archivo original
        _, ext = os.path.splitext(nombre_original)
        
        return f"{texto_limpio}{ext}"
    
    return nombre_original

def descargar_archivo(url, ruta_destino):
    """Descarga un archivo desde una URL"""
    headers = {'User-Agent': USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(ruta_destino, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True, response.headers.get('content-type', 'unknown')
    except Exception as e:
        return False, str(e)

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

def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("DESCARGA DE FORMATOS OFICIALES DE AUDITORÍA")
    print("Fuente: gob.mx - Secretaría Anticorrupción y Buen Gobierno")
    print("=" * 80)
    
    # Crear directorio de descargas
    Path(DIR_DESCARGAS).mkdir(exist_ok=True)
    
    # Cargar enlaces y cadena de custodia
    enlaces = cargar_enlaces()
    cadena = cargar_cadena_custodia()
    
    print(f"\nTotal de archivos a descargar: {len(enlaces)}")
    print(f"Directorio de destino: {DIR_DESCARGAS}/")
    print()
    
    # Estadísticas
    exitosos = 0
    fallidos = 0
    hashes_archivos = []
    
    # Descargar cada archivo
    for i, item in enumerate(enlaces, 1):
        url = item['url']
        texto = item['text']
        
        # Generar nombre de archivo
        nombre_archivo = obtener_nombre_archivo_limpio(url, texto)
        ruta_destino = os.path.join(DIR_DESCARGAS, nombre_archivo)
        
        print(f"[{i}/{len(enlaces)}] Descargando: {nombre_archivo}")
        print(f"  URL: {url}")
        
        # Descargar archivo
        exito, info = descargar_archivo(url, ruta_destino)
        
        if exito:
            # Calcular hash
            hash_archivo = calcular_hash_archivo(ruta_destino)
            tamaño = os.path.getsize(ruta_destino)
            
            print(f"  ✓ Descargado: {tamaño:,} bytes")
            print(f"  Hash SHA-256: {hash_archivo}")
            
            # Registrar en cadena de custodia
            metadata = {
                "descripcion": texto,
                "url": url,
                "nombre_archivo": nombre_archivo,
                "tamaño_bytes": tamaño,
                "content_type": info,
                "hash_sha256": hash_archivo
            }
            
            agregar_evento_cadena(cadena, "DOWNLOAD_FILE", hash_archivo, metadata)
            
            hashes_archivos.append({
                "nombre": nombre_archivo,
                "hash": hash_archivo,
                "tamaño": tamaño
            })
            
            exitosos += 1
        else:
            print(f"  ✗ Error: {info}")
            fallidos += 1
        
        print()
        
        # Pequeña pausa para no sobrecargar el servidor
        time.sleep(0.5)
    
    # Guardar cadena de custodia actualizada
    guardar_cadena_custodia(cadena)
    
    # Guardar lista de hashes
    with open("hashes_archivos.json", 'w', encoding='utf-8') as f:
        json.dump(hashes_archivos, f, indent=2, ensure_ascii=False)
    
    # Resumen
    print("=" * 80)
    print("RESUMEN DE DESCARGA")
    print("=" * 80)
    print(f"Archivos descargados exitosamente: {exitosos}")
    print(f"Archivos con error: {fallidos}")
    print(f"Total de eventos en cadena de custodia: {len(cadena['eventos'])}")
    print(f"\nArchivos guardados en: {DIR_DESCARGAS}/")
    print(f"Hashes guardados en: hashes_archivos.json")
    print(f"Cadena de custodia: {CADENA_CUSTODIA_JSON}")
    print()
    print("Próximo paso: Ejecutar 03_blockchain_anchoring.py")
    print()

if __name__ == "__main__":
    main()

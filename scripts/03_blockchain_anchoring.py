#!/usr/bin/env python3
"""
Script 3: Anclaje en Blockchain Bitcoin
Parte del Sistema de Auditoría Gubernamental con Validez Legal

Este script ancla los hashes de todos los archivos descargados en la
blockchain de Bitcoin usando OpenTimestamps, proporcionando fecha cierta
inmutable y verificable independientemente.
"""

import json
import os
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# Configuración
DIR_DESCARGAS = "formatos_descargados"
DIR_BLOCKCHAIN = "blockchain_proofs"
CADENA_CUSTODIA_JSON = "cadena_custodia.json"
HASHES_JSON = "hashes_archivos.json"

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

def verificar_opentimestamps():
    """Verifica si OpenTimestamps está instalado"""
    try:
        result = subprocess.run(['ots', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def instalar_opentimestamps():
    """Instala OpenTimestamps client"""
    print("Instalando OpenTimestamps client...")
    try:
        subprocess.run(['sudo', 'pip3', 'install', 'opentimestamps-client'], 
                      check=True)
        print("✓ OpenTimestamps instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error instalando OpenTimestamps: {e}")
        return False

def crear_timestamp(ruta_archivo):
    """Crea un timestamp de un archivo usando OpenTimestamps"""
    try:
        # Ejecutar ots stamp
        result = subprocess.run(['ots', 'stamp', ruta_archivo],
                              capture_output=True,
                              text=True,
                              timeout=60)
        
        if result.returncode == 0:
            return True, result.stdout + result.stderr
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout al crear timestamp"
    except Exception as e:
        return False, str(e)

def crear_merkle_tree(hashes):
    """Crea un Merkle tree simple de todos los hashes"""
    if not hashes:
        return None
    
    # Ordenar hashes para consistencia
    hashes_ordenados = sorted(hashes)
    
    # Concatenar todos los hashes y calcular hash raíz
    concatenado = "".join(hashes_ordenados).encode('utf-8')
    hash_raiz = hashlib.sha256(concatenado).hexdigest()
    
    return {
        "hash_raiz": hash_raiz,
        "num_hojas": len(hashes),
        "hashes_hojas": hashes_ordenados
    }

def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("ANCLAJE EN BLOCKCHAIN BITCOIN")
    print("Usando OpenTimestamps para fecha cierta inmutable")
    print("=" * 80)
    
    # Crear directorio para pruebas blockchain
    Path(DIR_BLOCKCHAIN).mkdir(exist_ok=True)
    
    # Verificar/instalar OpenTimestamps
    if not verificar_opentimestamps():
        print("\nOpenTimestamps no está instalado.")
        if not instalar_opentimestamps():
            print("\n✗ No se pudo instalar OpenTimestamps")
            print("Instalación manual: sudo pip3 install opentimestamps-client")
            return
    else:
        print("\n✓ OpenTimestamps está instalado")
    
    # Cargar datos
    cadena = cargar_cadena_custodia()
    
    with open(HASHES_JSON, 'r', encoding='utf-8') as f:
        hashes_archivos = json.load(f)
    
    print(f"\nTotal de archivos a anclar: {len(hashes_archivos)}")
    print()
    
    # Crear timestamps para cada archivo
    exitosos = 0
    fallidos = 0
    archivos_ots = []
    
    for i, item in enumerate(hashes_archivos, 1):
        nombre = item['nombre']
        hash_archivo = item['hash']
        ruta_archivo = os.path.join(DIR_DESCARGAS, nombre)
        
        print(f"[{i}/{len(hashes_archivos)}] Anclando: {nombre}")
        
        if not os.path.exists(ruta_archivo):
            print(f"  ✗ Archivo no encontrado: {ruta_archivo}")
            fallidos += 1
            continue
        
        # Crear timestamp
        exito, mensaje = crear_timestamp(ruta_archivo)
        
        if exito:
            archivo_ots = f"{ruta_archivo}.ots"
            
            # Mover archivo .ots a directorio de blockchain
            if os.path.exists(archivo_ots):
                destino_ots = os.path.join(DIR_BLOCKCHAIN, f"{nombre}.ots")
                os.rename(archivo_ots, destino_ots)
                
                print(f"  ✓ Timestamp creado: {nombre}.ots")
                print(f"  Nota: La confirmación en blockchain puede tardar 10-60 minutos")
                
                archivos_ots.append({
                    "nombre": nombre,
                    "hash": hash_archivo,
                    "ots_file": f"{nombre}.ots"
                })
                
                exitosos += 1
            else:
                print(f"  ⚠ Timestamp creado pero archivo .ots no encontrado")
                fallidos += 1
        else:
            print(f"  ✗ Error: {mensaje}")
            fallidos += 1
        
        print()
    
    # Crear Merkle tree de todos los hashes
    print("Creando Merkle tree de todos los hashes...")
    hashes_lista = [item['hash'] for item in hashes_archivos]
    merkle_tree = crear_merkle_tree(hashes_lista)
    
    if merkle_tree:
        print(f"✓ Merkle tree creado")
        print(f"  Hash raíz: {merkle_tree['hash_raiz']}")
        print(f"  Número de hojas: {merkle_tree['num_hojas']}")
        
        # Guardar Merkle tree
        with open("merkle_tree.json", 'w', encoding='utf-8') as f:
            json.dump(merkle_tree, f, indent=2, ensure_ascii=False)
        
        # Registrar en cadena de custodia
        metadata = {
            "descripcion": "Creación de Merkle tree de todos los hashes",
            "hash_raiz": merkle_tree['hash_raiz'],
            "num_archivos": merkle_tree['num_hojas']
        }
        agregar_evento_cadena(cadena, "CREATE_MERKLE_TREE", 
                            merkle_tree['hash_raiz'], metadata)
    
    # Guardar lista de archivos .ots
    with open("blockchain_timestamps.json", 'w', encoding='utf-8') as f:
        json.dump(archivos_ots, f, indent=2, ensure_ascii=False)
    
    # Registrar anclaje en cadena de custodia
    metadata = {
        "descripcion": "Anclaje de archivos en blockchain Bitcoin",
        "archivos_anclados": exitosos,
        "archivos_fallidos": fallidos,
        "protocolo": "OpenTimestamps",
        "blockchain": "Bitcoin"
    }
    agregar_evento_cadena(cadena, "BLOCKCHAIN_ANCHORING", 
                        merkle_tree['hash_raiz'] if merkle_tree else "N/A", 
                        metadata)
    
    # Guardar cadena de custodia
    guardar_cadena_custodia(cadena)
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE ANCLAJE BLOCKCHAIN")
    print("=" * 80)
    print(f"Archivos anclados exitosamente: {exitosos}")
    print(f"Archivos con error: {fallidos}")
    print(f"Archivos .ots generados: {len(archivos_ots)}")
    print(f"\nPruebas blockchain guardadas en: {DIR_BLOCKCHAIN}/")
    print(f"Merkle tree guardado en: merkle_tree.json")
    print(f"Lista de timestamps: blockchain_timestamps.json")
    print()
    print("IMPORTANTE:")
    print("- Los timestamps pueden tardar 10-60 minutos en confirmarse en blockchain")
    print("- Puedes verificar los timestamps con: ots verify <archivo>.ots")
    print("- Puedes actualizar los timestamps con: ots upgrade <archivo>.ots")
    print()
    print("Próximo paso: Ejecutar 04_nom151_certification.py")
    print()

if __name__ == "__main__":
    main()

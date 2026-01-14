#!/usr/bin/env python3
"""
Script 1: Verificación de Hash Genesis
Parte del Sistema de Auditoría Gubernamental con Validez Legal

Este script verifica el hash genesis (SHA-256 de cadena vacía) como punto
de partida verificable e inmutable de la cadena de custodia.

Hash Genesis: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
"""

import hashlib
import json
from datetime import datetime, timezone
import sys

# Hash genesis esperado (SHA-256 de cadena vacía)
HASH_GENESIS_ESPERADO = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

def calcular_hash_genesis():
    """Calcula el hash SHA-256 de una cadena vacía"""
    return hashlib.sha256(b"").hexdigest()

def verificar_hash_genesis():
    """Verifica que el hash genesis sea correcto"""
    hash_calculado = calcular_hash_genesis()
    
    print("=" * 80)
    print("VERIFICACIÓN DE HASH GENESIS")
    print("=" * 80)
    print(f"\nHash Genesis Esperado:")
    print(f"  {HASH_GENESIS_ESPERADO}")
    print(f"\nHash Genesis Calculado:")
    print(f"  {hash_calculado}")
    
    if hash_calculado == HASH_GENESIS_ESPERADO:
        print(f"\n✓ VERIFICACIÓN EXITOSA")
        print(f"  El hash genesis es correcto y verificable por cualquiera.")
        return True
    else:
        print(f"\n✗ ERROR EN VERIFICACIÓN")
        print(f"  El hash genesis no coincide.")
        return False

def inicializar_cadena_custodia():
    """Inicializa la cadena de custodia con el evento genesis"""
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    evento_genesis = {
        "event_id": 1,
        "timestamp": timestamp_utc,
        "action": "GENESIS_VERIFICATION",
        "hash_anterior": None,
        "hash_actual": HASH_GENESIS_ESPERADO,
        "metadata": {
            "descripcion": "Verificación de hash genesis (SHA-256 de cadena vacía)",
            "algoritmo": "SHA-256",
            "verificable": True,
            "comando_verificacion": 'echo -n "" | sha256sum'
        },
        "resultado": "EXITOSO"
    }
    
    cadena_custodia = {
        "version": "1.0",
        "proyecto": "Auditoría Gubernamental México - Sistema Norteamérica",
        "hash_genesis": HASH_GENESIS_ESPERADO,
        "inicio": timestamp_utc,
        "eventos": [evento_genesis]
    }
    
    return cadena_custodia

def guardar_cadena_custodia(cadena_custodia, ruta_salida):
    """Guarda la cadena de custodia en formato JSON"""
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(cadena_custodia, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Cadena de custodia inicializada:")
    print(f"  {ruta_salida}")

def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("SISTEMA DE AUDITORÍA GUBERNAMENTAL")
    print("Validez Legal: NOM-151 + Blockchain Bitcoin + Notaría 230 CDMX")
    print("=" * 80)
    
    # Verificar hash genesis
    if not verificar_hash_genesis():
        print("\n✗ Error: No se pudo verificar el hash genesis")
        sys.exit(1)
    
    # Inicializar cadena de custodia
    cadena_custodia = inicializar_cadena_custodia()
    
    # Guardar cadena de custodia
    guardar_cadena_custodia(cadena_custodia, "cadena_custodia.json")
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN COMPLETADA")
    print("=" * 80)
    print("\nPróximo paso: Ejecutar 02_download_formats.py")
    print()

if __name__ == "__main__":
    main()

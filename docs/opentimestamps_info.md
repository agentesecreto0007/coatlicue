# OpenTimestamps - Implementación

## Información General

**OpenTimestamps** es un protocolo de código abierto para crear pruebas de existencia verificables usando la blockchain de Bitcoin.

### Características
- **Gratuito**: No requiere pago de fees
- **Descentralizado**: No depende de autoridades centrales
- **Verificable**: Cualquiera puede verificar las pruebas
- **Compatible con NOM-151**: Cumple requisitos de fecha cierta

## Instalación

### Python Client
```bash
pip3 install opentimestamps-client
```

### Python Library
```bash
pip3 install opentimestamps
```

## Uso Básico

### Crear Timestamp (Stamp)
```bash
ots stamp archivo.pdf
# Genera: archivo.pdf.ots
```

### Verificar Timestamp
```bash
ots verify archivo.pdf.ots
```

### Información del Timestamp
```bash
ots info archivo.pdf.ots
```

## Proceso de Timestamping

1. **Hash del archivo**: Se calcula SHA-256
2. **Envío a calendarios**: Se envía a servidores públicos
3. **Agregación**: Se agrupa con otros hashes en un Merkle tree
4. **Anclaje en Bitcoin**: Se incluye en una transacción Bitcoin
5. **Confirmación**: Esperar ~10-60 minutos para confirmación en blockchain
6. **Prueba .ots**: Archivo que contiene la prueba verificable

## Integración en Python

```python
from opentimestamps import timestamp, serialize, core
import hashlib

# Calcular hash de archivo
def hash_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.digest()

# Crear timestamp
def create_timestamp(filepath):
    file_hash = hash_file(filepath)
    timestamp_obj = timestamp.Timestamp(file_hash)
    # Enviar a calendarios públicos
    # (requiere implementación completa)
    return timestamp_obj
```

## Calendarios Públicos

OpenTimestamps usa calendarios públicos gratuitos:
- `https://alice.btc.calendar.opentimestamps.org`
- `https://bob.btc.calendar.opentimestamps.org`
- `https://finney.calendar.eternitywall.com`

## Verificación

La verificación es **independiente** y no requiere confianza:
1. Se verifica el hash del archivo
2. Se verifica la cadena de operaciones en el .ots
3. Se verifica la inclusión en la blockchain de Bitcoin
4. Se obtiene el timestamp de la transacción Bitcoin

## Referencias

- **GitHub**: https://github.com/opentimestamps/opentimestamps-client
- **Python Library**: https://github.com/opentimestamps/python-opentimestamps
- **Tutorial**: https://dgi.io/ots-tutorial/
- **Web Interface**: https://dgi.io/ots/
- **Documentación**: https://opentimestamps.org/

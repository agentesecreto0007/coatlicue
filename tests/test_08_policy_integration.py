#!/usr/bin/env python3
"""
Unit Tests for Script 08: Policy Analysis Integration
Tests deterministic hashing, atomic writes, and chain of custody updates.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import the script
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import importlib.util

# Load the script module dynamically
spec = importlib.util.spec_from_file_location(
    "policy_integration",
    str(Path(__file__).parent.parent / "scripts" / "08_policy_analysis_integration.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Import functions
hash_json_canonico = module.hash_json_canonico
guardar_json_atomico = module.guardar_json_atomico
cargar_json = module.cargar_json
verificar_archivos_ots = module.verificar_archivos_ots


class DummyImport:
    pass


if False:  # Keep for type hints
    from dummy import (
        hash_json_canonico,
        guardar_json_atomico,
        cargar_json,
        verificar_archivos_ots
    )


class TestHashingDeterminista(unittest.TestCase):
    """Test that hashing is deterministic and reproducible"""
    
    def test_hash_mismo_objeto_mismo_resultado(self):
        """Same object should always produce same hash"""
        obj = {
            "nombre": "test",
            "valor": 123,
            "lista": [1, 2, 3]
        }
        
        hash1 = hash_json_canonico(obj)
        hash2 = hash_json_canonico(obj)
        
        self.assertEqual(hash1, hash2, "Hash debe ser determinista")
    
    def test_hash_orden_claves_no_importa(self):
        """Hash should be same regardless of key order"""
        obj1 = {"a": 1, "b": 2, "c": 3}
        obj2 = {"c": 3, "a": 1, "b": 2}
        
        hash1 = hash_json_canonico(obj1)
        hash2 = hash_json_canonico(obj2)
        
        self.assertEqual(hash1, hash2, "Orden de claves no debe afectar el hash")
    
    def test_hash_diferente_para_objetos_diferentes(self):
        """Different objects should produce different hashes"""
        obj1 = {"valor": 1}
        obj2 = {"valor": 2}
        
        hash1 = hash_json_canonico(obj1)
        hash2 = hash_json_canonico(obj2)
        
        self.assertNotEqual(hash1, hash2, "Objetos diferentes deben tener hashes diferentes")
    
    def test_hash_formato_hexadecimal(self):
        """Hash should be in hexadecimal format"""
        obj = {"test": "data"}
        hash_result = hash_json_canonico(obj)
        
        self.assertEqual(len(hash_result), 64, "Hash SHA-256 debe tener 64 caracteres")
        self.assertTrue(all(c in "0123456789abcdef" for c in hash_result), 
                       "Hash debe ser hexadecimal")


class TestEscrituraAtomica(unittest.TestCase):
    """Test that atomic writes work correctly"""
    
    def setUp(self):
        """Create temporary directory for tests"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_escritura_atomica_crea_archivo(self):
        """Atomic write should create file"""
        test_file = os.path.join(self.test_dir, "test.json")
        test_data = {"key": "value"}
        
        guardar_json_atomico(test_file, test_data)
        
        self.assertTrue(os.path.exists(test_file), "Archivo debe existir después de escritura atómica")
    
    def test_escritura_atomica_contenido_correcto(self):
        """Atomic write should save correct content"""
        test_file = os.path.join(self.test_dir, "test.json")
        test_data = {"nombre": "test", "valor": 123}
        
        guardar_json_atomico(test_file, test_data)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data, "Contenido guardado debe coincidir con original")
    
    def test_escritura_atomica_no_deja_temporales(self):
        """Atomic write should not leave temporary files"""
        test_file = os.path.join(self.test_dir, "test.json")
        test_data = {"test": "data"}
        
        guardar_json_atomico(test_file, test_data)
        
        # Check for temporary files
        temp_files = [f for f in os.listdir(self.test_dir) if f.startswith("tmp_")]
        
        self.assertEqual(len(temp_files), 0, "No deben quedar archivos temporales")


class TestCargaJSON(unittest.TestCase):
    """Test JSON loading with validation"""
    
    def setUp(self):
        """Create temporary directory for tests"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_cargar_json_existente(self):
        """Should load existing JSON file"""
        test_file = os.path.join(self.test_dir, "test.json")
        test_data = {"key": "value"}
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        loaded = cargar_json(test_file)
        
        self.assertEqual(loaded, test_data, "Datos cargados deben coincidir")
    
    def test_cargar_json_no_existente_lanza_excepcion(self):
        """Should raise FileNotFoundError for non-existent file"""
        test_file = os.path.join(self.test_dir, "no_existe.json")
        
        with self.assertRaises(FileNotFoundError):
            cargar_json(test_file)
    
    def test_cargar_json_invalido_lanza_excepcion(self):
        """Should raise JSONDecodeError for invalid JSON"""
        test_file = os.path.join(self.test_dir, "invalid.json")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        
        with self.assertRaises(json.JSONDecodeError):
            cargar_json(test_file)


class TestVerificacionBlockchain(unittest.TestCase):
    """Test blockchain proof verification"""
    
    def setUp(self):
        """Create temporary directory for tests"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_verificacion_directorio_no_existe(self):
        """Should handle non-existent blockchain directory"""
        blockchain_dir = os.path.join(self.test_dir, "no_existe")
        
        result = verificar_archivos_ots(blockchain_dir)
        
        self.assertFalse(result["blockchain_dir_exists"])
        self.assertEqual(result["ots_files_found"], 0)
    
    def test_verificacion_directorio_vacio(self):
        """Should handle empty blockchain directory"""
        blockchain_dir = os.path.join(self.test_dir, "blockchain")
        os.makedirs(blockchain_dir)
        
        result = verificar_archivos_ots(blockchain_dir)
        
        self.assertTrue(result["blockchain_dir_exists"])
        self.assertEqual(result["ots_files_found"], 0)
    
    def test_verificacion_con_archivos_ots(self):
        """Should count .ots files correctly"""
        blockchain_dir = os.path.join(self.test_dir, "blockchain")
        os.makedirs(blockchain_dir)
        
        # Create test .ots files
        for i in range(3):
            test_file = os.path.join(blockchain_dir, f"test{i}.ots")
            Path(test_file).touch()
        
        result = verificar_archivos_ots(blockchain_dir)
        
        self.assertTrue(result["blockchain_dir_exists"])
        self.assertEqual(result["ots_files_found"], 3)
        self.assertEqual(len(result["ots_files"]), 3)


class TestCadenaCustodia(unittest.TestCase):
    """Test chain of custody updates"""
    
    def setUp(self):
        """Create temporary directory and mock chain of custody"""
        self.test_dir = tempfile.mkdtemp()
        self.cadena_file = os.path.join(self.test_dir, "cadena_custodia.json")
        
        # Create initial chain of custody
        self.cadena_inicial = {
            "hash_genesis": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "eventos": [
                {
                    "event_id": 1,
                    "timestamp": "2026-01-14T00:00:00Z",
                    "action": "GENESIS",
                    "hash_anterior": "",
                    "hash_actual": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "metadata": {}
                }
            ]
        }
        
        guardar_json_atomico(self.cadena_file, self.cadena_inicial)
    
    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_cadena_custodia_se_carga_correctamente(self):
        """Chain of custody should load correctly"""
        cadena = cargar_json(self.cadena_file)
        
        self.assertEqual(len(cadena["eventos"]), 1)
        self.assertEqual(cadena["eventos"][0]["action"], "GENESIS")
    
    def test_nuevo_evento_incrementa_id(self):
        """New event should increment event_id"""
        cadena = cargar_json(self.cadena_file)
        
        ultimo_evento = cadena["eventos"][-1]
        nuevo_id = ultimo_evento["event_id"] + 1
        
        self.assertEqual(nuevo_id, 2, "Nuevo ID debe ser 2")
    
    def test_hash_evento_es_determinista(self):
        """Event hash should be deterministic"""
        evento_data = {
            "action": "TEST",
            "timestamp": "2026-01-14T00:00:00Z",
            "metadata": {"test": "data"}
        }
        
        hash1 = hash_json_canonico(evento_data)
        hash2 = hash_json_canonico(evento_data)
        
        self.assertEqual(hash1, hash2, "Hash de evento debe ser determinista")


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHashingDeterminista))
    suite.addTests(loader.loadTestsFromTestCase(TestEscrituraAtomica))
    suite.addTests(loader.loadTestsFromTestCase(TestCargaJSON))
    suite.addTests(loader.loadTestsFromTestCase(TestVerificacionBlockchain))
    suite.addTests(loader.loadTestsFromTestCase(TestCadenaCustodia))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())

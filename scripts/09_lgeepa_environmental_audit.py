#!/usr/bin/env python3
"""
LGEEPA Environmental Audit Integration
Integración de auditoría ambiental LGEEPA con Sistema Coatlicue v3.0

Author: Manus AI
Date: 2026-01-14
Version: 1.0
"""

import sys
import os
import hashlib
import json
import logging
import argparse
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
logger = logging.getLogger("lgeepa_audit")

# Constants
FORMATOS_DIR = "formatos_descargados"
CADENA_CUSTODIA_JSON = "cadena_custodia.json"
LGEEPA_ANALYSIS_JSON = "lgeepa_analysis.json"
LGEEPA_REPORT_MD = "lgeepa_environmental_report.md"
BLOCKCHAIN_DIR = "blockchain_proofs"


# Data structures
@dataclass
class ProcessedDocument:
    """Representa un documento procesado."""
    id: str
    name: str
    content_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    original_path: Optional[str] = None


@dataclass
class AnalysisFinding:
    """Representa un hallazgo del análisis."""
    rule_id: str
    description: str
    status: str  # "Cumple", "No Cumple", "Advertencia", "No Aplica"
    severity: str  # "Critico", "Alto", "Medio", "Bajo"
    context: Optional[str] = None
    recommendation: Optional[str] = None


@dataclass
class AnalysisResult:
    """Resultado completo del análisis."""
    regulation_name: str
    jurisdiction: str
    summary: str
    findings: List[AnalysisFinding] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# Functions from v3.0
def hash_json_canonico(obj: Any) -> str:
    """
    Calculate SHA-256 hash of JSON object using canonical serialization.
    This ensures reproducible hashes across executions.
    """
    canonical = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def cargar_json(ruta: str) -> Any:
    """Load a JSON file with validation"""
    p = Path(ruta)
    
    if not p.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Archivo cargado exitosamente: {ruta}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON en {ruta}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error al cargar {ruta}: {e}")
        raise


# LGEEPA Adapter Implementation
class LGEEPAAdapter:
    """
    Adaptador para auditoría de cumplimiento de LGEEPA y NOMs ambientales mexicanas.
    """
    
    def __init__(self):
        """Inicializa el adaptador LGEEPA."""
        self._initialize_rules()
        
    def get_name(self) -> str:
        """Retorna el nombre de la regulación."""
        return "LGEEPA (Ley General del Equilibrio Ecológico y la Protección al Ambiente)"
    
    def get_jurisdiction(self) -> str:
        """Retorna la jurisdicción aplicable."""
        return "México"
    
    def _initialize_rules(self):
        """Inicializa las reglas y principios de LGEEPA y NOMs ambientales."""
        self.lgeepa_principles = [
            {
                "id": "LGEEPA-Art15-I",
                "description": "Los ecosistemas son patrimonio común de la sociedad",
                "category": "Principios Generales"
            },
            {
                "id": "LGEEPA-Art15-IV",
                "description": "Quien realice obras o actividades que afecten el ambiente debe prevenir, minimizar o reparar los daños",
                "category": "Responsabilidad Ambiental"
            },
            {
                "id": "LGEEPA-Art28",
                "description": "Evaluación del impacto ambiental",
                "category": "Evaluación de Impacto"
            },
            {
                "id": "LGEEPA-Art35",
                "description": "Manifestación de Impacto Ambiental (MIA)",
                "category": "Evaluación de Impacto"
            },
        ]
        
        self.noms_ambientales = [
            {
                "id": "NOM-001-SEMARNAT-2021",
                "description": "Límites máximos permisibles de contaminantes en descargas de aguas residuales",
                "category": "Agua",
                "severity": "Critico"
            },
            {
                "id": "NOM-052-SEMARNAT-2005",
                "description": "Características, identificación, clasificación y listados de residuos peligrosos",
                "category": "Residuos Peligrosos",
                "severity": "Critico"
            },
            {
                "id": "NOM-059-SEMARNAT-2010",
                "description": "Protección ambiental - Especies nativas de México de flora y fauna silvestres",
                "category": "Biodiversidad",
                "severity": "Alto"
            },
            {
                "id": "NOM-081-SEMARNAT-1994",
                "description": "Límites máximos permisibles de emisión de ruido",
                "category": "Contaminación Acústica",
                "severity": "Medio"
            },
            {
                "id": "NOM-120-SEMARNAT-2020",
                "description": "Criterios y especificaciones técnicas para el manejo de residuos de manejo especial",
                "category": "Residuos",
                "severity": "Alto"
            },
            {
                "id": "NOM-161-SEMARNAT-2011",
                "description": "Clasificación de los residuos de manejo especial",
                "category": "Residuos",
                "severity": "Alto"
            },
        ]
        
        logger.info(f"[{self.get_name()}] Inicializadas {len(self.lgeepa_principles)} principios LGEEPA y {len(self.noms_ambientales)} NOMs ambientales")
    
    def ingest_documents(self, doc_paths: List[str]) -> List[ProcessedDocument]:
        """Procesa documentos ambientales."""
        processed_docs: List[ProcessedDocument] = []
        
        for path in doc_paths:
            logger.info(f"[{self.get_name()}] Procesando documento: {path}")
            
            try:
                if not os.path.exists(path):
                    logger.warning(f"Archivo no encontrado: {path}")
                    continue
                
                with open(path, 'rb') as f:
                    content = f.read()
                
                content_hash = hashlib.sha256(content).hexdigest()
                
                filename = os.path.basename(path)
                metadata = {
                    "filename": filename,
                    "size_bytes": len(content),
                    "extension": os.path.splitext(filename)[1],
                    "processed_at": datetime.now().isoformat()
                }
                
                extracted_data = self._extract_environmental_data(path, content, filename)
                
                processed_doc = ProcessedDocument(
                    id=f"doc-{len(processed_docs) + 1}",
                    name=filename,
                    content_hash=content_hash,
                    metadata=metadata,
                    extracted_data=extracted_data,
                    original_path=path
                )
                
                processed_docs.append(processed_doc)
                logger.info(f"Documento procesado: {filename} (hash: {content_hash[:16]}...)")
                
            except Exception as e:
                logger.error(f"Error procesando {path}: {e}")
                continue
        
        logger.info(f"[{self.get_name()}] Total de documentos procesados: {len(processed_docs)}")
        return processed_docs
    
    def _extract_environmental_data(self, path: str, content: bytes, filename: str) -> Dict[str, Any]:
        """Extrae datos ambientales estructurados del documento."""
        extracted = {
            "document_type": "unknown",
            "noms_mentioned": [],
            "has_mia": False,
            "has_environmental_license": False,
            "mentions_semarnat": False,
            "mentions_profepa": False,
        }
        
        try:
            text_content = content.decode('utf-8', errors='ignore').lower()
        except:
            text_content = str(content).lower()
        
        # Detectar tipo de documento
        if "mia" in filename.lower() or "manifestacion" in text_content:
            extracted["document_type"] = "Manifestación de Impacto Ambiental (MIA)"
            extracted["has_mia"] = True
        elif "licencia" in filename.lower() or "autorizacion" in text_content:
            extracted["document_type"] = "Licencia/Autorización Ambiental"
            extracted["has_environmental_license"] = True
        elif "formato" in filename.lower():
            extracted["document_type"] = "Formato SEMARNAT"
        
        # Detectar menciones de NOMs
        for nom in self.noms_ambientales:
            nom_id = nom["id"].lower()
            if nom_id in text_content or nom_id.replace("-", "") in text_content:
                extracted["noms_mentioned"].append(nom["id"])
        
        # Detectar menciones de agencias
        if "semarnat" in text_content:
            extracted["mentions_semarnat"] = True
        if "profepa" in text_content:
            extracted["mentions_profepa"] = True
        
        return extracted
    
    def analyze(self, processed_docs: List[ProcessedDocument]) -> AnalysisResult:
        """Realiza análisis de cumplimiento de LGEEPA y NOMs ambientales."""
        findings: List[AnalysisFinding] = []
        summary_notes: List[str] = []
        
        logger.info(f"[{self.get_name()}] Iniciando análisis de {len(processed_docs)} documentos")
        
        # Verificar presencia de MIA
        has_mia = any(doc.extracted_data.get("has_mia", False) for doc in processed_docs)
        
        if has_mia:
            findings.append(AnalysisFinding(
                rule_id="LGEEPA-Art35",
                description="Se identificó Manifestación de Impacto Ambiental (MIA)",
                status="Cumple",
                severity="Bajo",
                context="Documento MIA presente en el expediente"
            ))
            summary_notes.append("MIA detectada")
        else:
            findings.append(AnalysisFinding(
                rule_id="LGEEPA-Art35",
                description="No se encontró Manifestación de Impacto Ambiental (MIA)",
                status="No Cumple",
                severity="Critico",
                recommendation="Elaborar y presentar MIA ante SEMARNAT según Art. 35 LGEEPA",
                context="Requisito obligatorio para proyectos con impacto ambiental significativo"
            ))
            summary_notes.append("MIA faltante - CRÍTICO")
        
        # Verificar presencia de licencias
        has_license = any(doc.extracted_data.get("has_environmental_license", False) for doc in processed_docs)
        
        if has_license:
            findings.append(AnalysisFinding(
                rule_id="LGEEPA-Art28",
                description="Se identificó licencia o autorización ambiental",
                status="Cumple",
                severity="Bajo"
            ))
        else:
            findings.append(AnalysisFinding(
                rule_id="LGEEPA-Art28",
                description="No se encontró licencia o autorización ambiental",
                status="Advertencia",
                severity="Alto",
                recommendation="Verificar si el proyecto requiere autorización ambiental de SEMARNAT"
            ))
        
        # Analizar cumplimiento de NOMs
        all_noms_mentioned = set()
        for doc in processed_docs:
            noms = doc.extracted_data.get("noms_mentioned", [])
            all_noms_mentioned.update(noms)
        
        if all_noms_mentioned:
            findings.append(AnalysisFinding(
                rule_id="NOMs-SEMARNAT",
                description=f"Se identificaron referencias a {len(all_noms_mentioned)} NOMs ambientales",
                status="Cumple",
                severity="Bajo",
                context=f"NOMs mencionadas: {', '.join(sorted(all_noms_mentioned))}"
            ))
            summary_notes.append(f"{len(all_noms_mentioned)} NOMs identificadas")
        else:
            findings.append(AnalysisFinding(
                rule_id="NOMs-SEMARNAT",
                description="No se identificaron referencias a NOMs ambientales específicas",
                status="Advertencia",
                severity="Medio",
                recommendation="Verificar cumplimiento de NOMs aplicables según el tipo de proyecto"
            ))
        
        # Generar resumen
        critical_findings = [f for f in findings if f.severity == "Critico"]
        high_findings = [f for f in findings if f.severity == "Alto"]
        
        if critical_findings:
            overall_summary = f"Se encontraron {len(critical_findings)} hallazgo(s) CRÍTICO(S) de incumplimiento LGEEPA/NOMs"
        elif high_findings:
            overall_summary = f"Se identificaron {len(high_findings)} advertencia(s) de ALTA severidad"
        else:
            overall_summary = "Cumplimiento preliminar aparente de LGEEPA y NOMs ambientales"
        
        logger.info(f"[{self.get_name()}] Análisis completado: {len(findings)} hallazgos")
        
        return AnalysisResult(
            regulation_name=self.get_name(),
            jurisdiction=self.get_jurisdiction(),
            summary=overall_summary,
            findings=findings,
            timestamp=datetime.now().isoformat()
        )


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="LGEEPA Environmental Audit for Coatlicue System"
    )
    parser.add_argument("--verify-only", action="store_true", help="Only verify files")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing")
    
    args = parser.parse_args()
    
    logger.info("=== LGEEPA Environmental Audit ===")
    logger.info(f"Regulación: LGEEPA + NOMs Ambientales")
    logger.info(f"Jurisdicción: México")
    logger.info(f"Agencias: SEMARNAT, PROFEPA\n")
    
    # Crear adaptador
    adapter = LGEEPAAdapter()
    
    # Buscar formatos ambientales
    if os.path.exists(FORMATOS_DIR):
        all_files = list(Path(FORMATOS_DIR).glob("*"))
        logger.info(f"Encontrados {len(all_files)} archivos en {FORMATOS_DIR}")
        
        # Filtrar formatos ambientales (simplificado)
        environmental_files = [str(f) for f in all_files if "14" in f.name or "15" in f.name or "17" in f.name]
        
        if environmental_files:
            logger.info(f"Identificados {len(environmental_files)} formatos potencialmente ambientales")
            
            if not args.verify_only:
                # Procesar documentos
                processed_docs = adapter.ingest_documents(environmental_files)
                
                # Analizar
                result = adapter.analyze(processed_docs)
                
                # Generar reporte
                logger.info(f"\n{'='*60}")
                logger.info(f"RESUMEN: {result.summary}")
                logger.info(f"Total de hallazgos: {len(result.findings)}")
                logger.info(f"{'='*60}\n")
                
                if not args.dry_run:
                    # Guardar resultados
                    with open(LGEEPA_ANALYSIS_JSON, 'w', encoding='utf-8') as f:
                        json.dump(asdict(result), f, indent=2, ensure_ascii=False, default=str)
                    logger.info(f"✅ Análisis guardado en: {LGEEPA_ANALYSIS_JSON}")
                    
                    # Generar reporte markdown
                    report = f"# Reporte de Auditoría Ambiental LGEEPA\n\n"
                    report += f"**Regulación**: {result.regulation_name}\n"
                    report += f"**Jurisdicción**: {result.jurisdiction}\n"
                    report += f"**Fecha**: {result.timestamp}\n\n"
                    report += f"## Resumen Ejecutivo\n\n{result.summary}\n\n"
                    report += f"## Hallazgos ({len(result.findings)})\n\n"
                    
                    for finding in result.findings:
                        report += f"### [{finding.status}] {finding.rule_id}\n\n"
                        report += f"**Descripción**: {finding.description}\n\n"
                        report += f"**Severidad**: {finding.severity}\n\n"
                        if finding.context:
                            report += f"**Contexto**: {finding.context}\n\n"
                        if finding.recommendation:
                            report += f"**Recomendación**: {finding.recommendation}\n\n"
                        report += "---\n\n"
                    
                    with open(LGEEPA_REPORT_MD, 'w', encoding='utf-8') as f:
                        f.write(report)
                    logger.info(f"✅ Reporte guardado en: {LGEEPA_REPORT_MD}")
                else:
                    logger.info("Modo dry-run: No se guardaron archivos")
        else:
            logger.warning("No se encontraron formatos ambientales")
    else:
        logger.warning(f"Directorio no encontrado: {FORMATOS_DIR}")
    
    logger.info("\n✅ Auditoría ambiental LGEEPA completada")


if __name__ == "__main__":
    main()

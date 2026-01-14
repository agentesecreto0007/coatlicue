import hashlib
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Importar las clases base del framework
from .regulatory_adapter import RegulatoryAdapter, AdapterConfig
from .data_structures import ProcessedDocument, AnalysisFinding, AnalysisResult


class GDPRAdapter(RegulatoryAdapter):
    """
    Adaptador de ejemplo para el Reglamento General de Protección de Datos (GDPR).
    Este prototipo simula el análisis de documentos clave de privacidad.
    """

    def get_name(self) -> str:
        return "GDPR (General Data Protection Regulation)"

    def get_jurisdiction(self) -> str:
        return "European Union"

    def _initialize_rules(self):
        # En un adaptador real, aquí se cargarían las reglas/principios del GDPR
        # desde un archivo JSON, base de datos o API.
        # Para el prototipo, definimos algunos principios clave hardcodeados.
        self.gdpr_principles = [
            {"id": "GDPR-5.1.a", "description": "Licitud, lealtad y transparencia"},
            {"id": "GDPR-5.1.b", "description": "Limitación de la finalidad"},
            {"id": "GDPR-6", "description": "Licitud del tratamiento"},
            {"id": "GDPR-13/14", "description": "Información a los interesados"},
            {"id": "GDPR-15-22", "description": "Derechos del interesado (ARCO)"},
            {"id": "GDPR-35", "description": "Evaluación de Impacto en la Protección de Datos (DPIA)"},
            {"id": "GDPR-37", "description": "Delegado de Protección de Datos (DPO)"},
        ]
        print(f"[{self.get_name()}] Reglas GDPR inicializadas.")

    def ingest_documents(self, doc_paths: List[str]) -> List[ProcessedDocument]:
        processed_docs: List[ProcessedDocument] = []
        for path in doc_paths:
            print(f"[{self.get_name()}] Simulando ingesta y procesamiento de: {path}")
            # Simulamos leer el contenido y generar un hash determinista
            # En un caso real, se usaría Coatlicue.core.hash_deterministic(content)
            mock_content = f"Simulated content for {path} related to GDPR."
            content_hash = hashlib.sha256(mock_content.encode('utf-8')).hexdigest()

            # Extraemos datos simulados (e.g., presencia de palabras clave)
            extracted_data = {}
            if "privacy_policy" in path.lower():
                extracted_data["has_privacy_policy"] = True
                if "right to erasure" in mock_content.lower() or "derecho al olvido" in mock_content.lower():
                    extracted_data["mentions_erasure_right"] = True
            if "dpia" in path.lower():
                extracted_data["has_dpia"] = True
                if "legal basis" in mock_content.lower():
                    extracted_data["mentions_legal_basis"] = True

            processed_docs.append(
                ProcessedDocument(
                    id=f"doc-{len(processed_docs) + 1}",
                    name=path.split('/')[-1],
                    content_hash=content_hash,
                    original_path=path,
                    extracted_data=extracted_data
                )
            )
        return processed_docs

    def analyze(self, processed_docs: List[ProcessedDocument]) -> AnalysisResult:
        findings: List[AnalysisFinding] = []
        summary_notes: List[str] = []

        # Simulamos la verificación de principios GDPR
        has_privacy_policy = any("has_privacy_policy" in d.extracted_data for d in processed_docs)
        mentions_erasure_right = any(d.extracted_data.get("mentions_erasure_right", False) for d in processed_docs)
        has_dpia = any("has_dpia" in d.extracted_data for d in processed_docs)
        mentions_legal_basis = any(d.extracted_data.get("mentions_legal_basis", False) for d in processed_docs)

        # GDPR-13/14: Información a los interesados (Privacy Policy)
        if has_privacy_policy:
            findings.append(AnalysisFinding(
                rule_id="GDPR-13/14",
                description="Se identificó un documento de política de privacidad.",
                status="Cumple",
                severity="Bajo"
            ))
            summary_notes.append("Política de privacidad detectada.")
        else:
            findings.append(AnalysisFinding(
                rule_id="GDPR-13/14",
                description="No se encontró un documento de política de privacidad.",
                status="No Cumple",
                severity="Critico",
                recommendation="Proporcionar una política de privacidad clara y accesible."
            ))
            summary_notes.append("Falta política de privacidad.")

        # GDPR-15-22: Derechos del interesado (Derecho al olvido como ejemplo)
        if mentions_erasure_right:
            findings.append(AnalysisFinding(
                rule_id="GDPR-15-22",
                description="La política de privacidad menciona el derecho de supresión (olvido).",
                status="Cumple",
                severity="Bajo"
            ))
        else:
            findings.append(AnalysisFinding(
                rule_id="GDPR-15-22",
                description="La política de privacidad no menciona explícitamente el derecho de supresión.",
                status="Advertencia",
                severity="Alto",
                recommendation="Asegurarse de que todos los derechos de los interesados estén claramente articulados."
            ))

        # GDPR-35: Evaluación de Impacto en la Protección de Datos (DPIA)
        if has_dpia:
            findings.append(AnalysisFinding(
                rule_id="GDPR-35",
                description="Se identificó una Evaluación de Impacto en la Protección de Datos (DPIA).",
                status="Cumple",
                severity="Bajo"
            ))
            if not mentions_legal_basis:
                 findings.append(AnalysisFinding(
                    rule_id="GDPR-6/35",
                    description="La DPIA no menciona la base legal para el tratamiento de datos.",
                    status="Advertencia",
                    severity="Alto",
                    recommendation="Revisar la DPIA para incluir la base legal explícita (Art. 6 GDPR)."
                ))
        else:
            # Esta regla es más compleja, solo se requiere si el tratamiento es de alto riesgo
            findings.append(AnalysisFinding(
                rule_id="GDPR-35",
                description="No se encontró una DPIA. Evaluar si es necesaria para el tratamiento de datos.",
                status="Advertencia",
                severity="Medio",
                recommendation="Realizar una evaluación para determinar si se requiere una DPIA (Art. 35 GDPR)."
            ))
            summary_notes.append("DPIA no detectada, posible requisito.")


        overall_summary = "Análisis preliminar de documentos de privacidad."
        if any(f.status == "No Cumple" for f in findings):
            overall_summary = "Se encontraron fallos críticos de cumplimiento."
        elif any(f.status == "Advertencia" for f in findings):
            overall_summary = "Se identificaron advertencias que requieren atención."
        else:
            overall_summary = "Cumplimiento preliminar aparente."

        return AnalysisResult(
            regulation_name=self.get_name(),
            jurisdiction=self.get_jurisdiction(),
            summary=overall_summary,
            findings=findings
        )

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional

# Importar las dataclasses auxiliares definidas arriba
from .data_structures import ProcessedDocument, AnalysisFinding, AnalysisResult, AdapterConfig

class RegulatoryAdapter(ABC):
    """
    Clase Base Abstracta para todos los adaptadores regulatorios de Coatlicue.
    Define la interfaz que cada adaptador debe implementar para interactuar
    con el núcleo del sistema Coatlicue.
    """

    def __init__(self, config: AdapterConfig):
        """
        Inicializa el adaptador con su configuración específica.
        """
        self.config = config
        self._initialize_rules() # Método interno para cargar reglas/principios

    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre de la regulación que maneja este adaptador."""
        pass

    @abstractmethod
    def get_jurisdiction(self) -> str:
        """Retorna la jurisdicción a la que aplica esta regulación."""
        pass

    @abstractmethod
    def _initialize_rules(self):
        """
        Método interno para cargar los principios o reglas específicas
        de la regulación que el adaptador va a auditar.
        """
        pass

    @abstractmethod
    def ingest_documents(self, doc_paths: List[str]) -> List[ProcessedDocument]:
        """
        Procesa una lista de rutas de documentos, extrayendo información relevante
        y generando un hash determinista para cada uno.
        Debe retornar una lista de objetos ProcessedDocument.
        """
        pass

    @abstractmethod
    def analyze(self, processed_docs: List[ProcessedDocument]) -> AnalysisResult:
        """
        Realiza el análisis de cumplimiento contra la regulación, utilizando
        los documentos ya procesados.
        Debe retornar un objeto AnalysisResult con los hallazgos.
        """
        pass

    def render_report_summary(self, analysis_result: AnalysisResult) -> str:
        """
        Genera un resumen legible del AnalysisResult. Puede ser sobrescrito
        por adaptadores específicos para un formato de reporte más complejo.
        """
        summary_str = f"## Reporte de Cumplimiento: {analysis_result.regulation_name} ({analysis_result.jurisdiction})\n"
        summary_str += f"Fecha del Análisis: {analysis_result.timestamp}\n\n"
        summary_str += f"**Resumen General:** {analysis_result.summary}\n\n"
        summary_str += "**Hallazgos Clave:**\n"
        for finding in analysis_result.findings:
            summary_str += f"- [{finding.status}] {finding.description} (Severidad: {finding.severity})\n"
            if finding.recommendation:
                summary_str += f"  * Recomendación: {finding.recommendation}\n"
        return summary_str

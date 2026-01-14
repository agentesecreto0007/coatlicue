from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class ProcessedDocument:
    """Representa un documento procesado por el adaptador."""
    id: str
    name: str
    content_hash: str # Hash determinista del contenido
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_data: Dict[str, Any] = field(default_factory=dict) # Datos estructurados extraídos
    original_path: Optional[str] = None

@dataclass
class AnalysisFinding:
    """Representa un hallazgo específico del análisis."""
    rule_id: str # ID de la regla o principio de la regulación
    description: str
    status: str # "Cumple", "No Cumple", "Advertencia", "No Aplica"
    severity: str # "Critico", "Alto", "Medio", "Bajo"
    context: Optional[str] = None # Fragmento de texto o dato relevante
    recommendation: Optional[str] = None

@dataclass
class AnalysisResult:
    """Contiene el resultado completo del análisis de un adaptador."""
    regulation_name: str
    jurisdiction: str
    summary: str
    findings: List[AnalysisFinding] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class AdapterConfig:
    """Configuración específica para un adaptador."""
    rules_path: Optional[str] = None
    language: str = "es"

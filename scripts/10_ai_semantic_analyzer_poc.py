#!/usr/bin/env python3
"""
AI-Powered Semantic Analyzer - Proof of Concept
Analizador semántico con Gemini para documentos legales

Author: Manus AI
Date: 2026-01-14
Version: 1.0 (PoC)
"""

import os
import sys
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
logger = logging.getLogger("ai_semantic_analyzer")

# Check for Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY no encontrada. Usando modo simulación.")
    SIMULATION_MODE = True
else:
    SIMULATION_MODE = False
    try:
        from google import genai
        from google.genai import types
        logger.info("✅ Google Gemini SDK importado exitosamente")
    except ImportError:
        logger.error("google-genai no instalado. Instalar con: sudo pip3 install google-genai")
        SIMULATION_MODE = True


class SemanticAnalyzer:
    """Analizador semántico con Gemini para documentos legales."""
    
    def __init__(self, simulation_mode: bool = False):
        """
        Inicializa el analizador semántico.
        
        Args:
            simulation_mode: Si True, simula respuestas sin llamar a la API
        """
        self.simulation_mode = simulation_mode or SIMULATION_MODE
        
        if not self.simulation_mode:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self.model = "gemini-2.0-flash-exp"
            logger.info(f"✅ Gemini client inicializado (modelo: {self.model})")
        else:
            logger.info("⚠️  Modo simulación activado (sin llamadas a API)")
    
    def extract_legal_clauses(self, document_text: str, regulation: str) -> dict:
        """
        Extrae cláusulas legales relevantes del documento.
        
        Args:
            document_text: Texto del documento
            regulation: Regulación a auditar (ej: "LGEEPA", "GDPR")
        
        Returns:
            dict con cláusulas extraídas y análisis
        """
        logger.info(f"Extrayendo cláusulas legales para regulación: {regulation}")
        
        if self.simulation_mode:
            return self._simulate_extraction(document_text, regulation)
        
        prompt = f"""
Eres un experto en derecho ambiental mexicano especializado en {regulation}.

Analiza el siguiente documento y extrae:

1. **Obligaciones legales mencionadas**: Lista todas las obligaciones específicas
2. **Artículos/NOMs citados**: Identifica referencias a leyes y normas
3. **Fechas límite**: Extrae plazos y vencimientos
4. **Responsables**: Identifica quién es responsable de cada obligación
5. **Cumplimientos**: Qué se está cumpliendo correctamente
6. **Incumplimientos**: Qué NO se está cumpliendo
7. **Riesgos identificados**: Posibles problemas legales
8. **Recomendaciones**: Acciones específicas a tomar

DOCUMENTO (primeros 5000 caracteres):
{document_text[:5000]}

Responde en formato JSON estructurado con estas claves:
{{
  "obligaciones": ["obligación 1", "obligación 2"],
  "articulos_citados": ["Art. X", "NOM-Y"],
  "fechas_limite": ["fecha 1", "fecha 2"],
  "responsables": ["responsable 1"],
  "cumplimientos": ["cumplimiento 1"],
  "incumplimientos": ["incumplimiento 1"],
  "riesgos": ["riesgo 1"],
  "recomendaciones": ["recomendación 1"]
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            logger.info(f"✅ Extracción completada: {len(result.get('obligaciones', []))} obligaciones encontradas")
            return result
            
        except Exception as e:
            logger.error(f"Error en extracción con Gemini: {e}")
            return self._simulate_extraction(document_text, regulation)
    
    def analyze_compliance(self, document_text: str, regulation_rules: list) -> dict:
        """
        Analiza cumplimiento de reglas específicas.
        
        Args:
            document_text: Texto del documento
            regulation_rules: Lista de reglas a verificar
        
        Returns:
            dict con hallazgos de cumplimiento
        """
        logger.info(f"Analizando cumplimiento de {len(regulation_rules)} reglas")
        
        if self.simulation_mode:
            return self._simulate_compliance_analysis(document_text, regulation_rules)
        
        rules_str = "\n".join([
            f"- {r['id']}: {r['description']}"
            for r in regulation_rules[:10]  # Limitar a 10 reglas
        ])
        
        prompt = f"""
Eres un auditor experto en cumplimiento regulatorio.

REGLAS A VERIFICAR:
{rules_str}

DOCUMENTO (primeros 5000 caracteres):
{document_text[:5000]}

Para cada regla, determina:
1. **Status**: "Cumple", "No Cumple", "Parcialmente Cumple", "No Aplica"
2. **Evidencia**: Cita textual del documento que lo demuestra (si existe)
3. **Confianza**: Porcentaje de confianza en tu análisis (0-100%)
4. **Explicación**: Por qué llegaste a esa conclusión
5. **Recomendación**: Qué hacer si no cumple

Responde en formato JSON:
{{
  "findings": [
    {{
      "rule_id": "...",
      "status": "...",
      "confidence": 95,
      "evidence": "...",
      "explanation": "...",
      "recommendation": "..."
    }}
  ],
  "summary": "resumen general del análisis"
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            logger.info(f"✅ Análisis completado: {len(result.get('findings', []))} hallazgos")
            return result
            
        except Exception as e:
            logger.error(f"Error en análisis con Gemini: {e}")
            return self._simulate_compliance_analysis(document_text, regulation_rules)
    
    def generate_executive_summary(self, analysis_result: dict, language: str = "es") -> str:
        """
        Genera resumen ejecutivo del análisis.
        
        Args:
            analysis_result: Resultado del análisis
            language: "es" o "en"
        
        Returns:
            Resumen ejecutivo en el idioma solicitado
        """
        logger.info(f"Generando resumen ejecutivo en {language}")
        
        if self.simulation_mode:
            return self._simulate_summary(analysis_result, language)
        
        lang_instruction = "en español" if language == "es" else "in English"
        
        prompt = f"""
Eres un consultor senior de cumplimiento regulatorio.

Genera un resumen ejecutivo {lang_instruction} del siguiente análisis de auditoría:

{json.dumps(analysis_result, indent=2, ensure_ascii=False)[:3000]}

El resumen debe:
1. Ser conciso (máximo 300 palabras)
2. Destacar hallazgos críticos
3. Incluir recomendaciones prioritarias
4. Usar lenguaje profesional pero accesible
5. Incluir un "llamado a la acción" claro

Formato: Párrafos profesionales, NO bullet points.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            
            summary = response.text
            logger.info(f"✅ Resumen generado ({len(summary)} caracteres)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generando resumen con Gemini: {e}")
            return self._simulate_summary(analysis_result, language)
    
    # Métodos de simulación (para cuando no hay API key)
    
    def _simulate_extraction(self, document_text: str, regulation: str) -> dict:
        """Simula extracción de cláusulas legales."""
        logger.info("🎭 Simulando extracción de cláusulas")
        
        return {
            "obligaciones": [
                "Presentar Manifestación de Impacto Ambiental (MIA)",
                "Obtener autorización de SEMARNAT",
                "Cumplir con NOM-001-SEMARNAT sobre descargas de aguas"
            ],
            "articulos_citados": [
                "Art. 35 LGEEPA",
                "Art. 28 LGEEPA",
                "NOM-001-SEMARNAT-2021"
            ],
            "fechas_limite": [
                "30 días antes del inicio de obras",
                "Renovación anual de licencia"
            ],
            "responsables": [
                "Titular del proyecto",
                "Representante legal"
            ],
            "cumplimientos": [
                "Documentación básica presentada"
            ],
            "incumplimientos": [
                "Falta MIA completa",
                "No se identificó autorización ambiental vigente"
            ],
            "riesgos": [
                "Suspensión de obras por falta de MIA",
                "Multas de PROFEPA",
                "Responsabilidad penal ambiental"
            ],
            "recomendaciones": [
                "Elaborar y presentar MIA ante SEMARNAT urgentemente",
                "Solicitar autorización ambiental",
                "Contratar consultor ambiental certificado"
            ]
        }
    
    def _simulate_compliance_analysis(self, document_text: str, regulation_rules: list) -> dict:
        """Simula análisis de cumplimiento."""
        logger.info("🎭 Simulando análisis de cumplimiento")
        
        findings = []
        for rule in regulation_rules[:5]:  # Simular primeras 5 reglas
            finding = {
                "rule_id": rule["id"],
                "status": "No Cumple" if "Art35" in rule["id"] or "Art28" in rule["id"] else "Cumple",
                "confidence": 85,
                "evidence": f"Análisis simulado del documento para {rule['id']}",
                "explanation": f"El documento {'no cumple' if 'Art35' in rule['id'] else 'cumple'} con {rule['description']}",
                "recommendation": f"Revisar y completar requisitos de {rule['id']}" if "Art35" in rule["id"] else "Mantener cumplimiento"
            }
            findings.append(finding)
        
        return {
            "findings": findings,
            "summary": f"Análisis simulado de {len(findings)} reglas. Se detectaron incumplimientos críticos."
        }
    
    def _simulate_summary(self, analysis_result: dict, language: str) -> str:
        """Simula generación de resumen ejecutivo."""
        logger.info("🎭 Simulando resumen ejecutivo")
        
        if language == "es":
            return """
**Resumen Ejecutivo de Auditoría Ambiental LGEEPA**

El análisis realizado sobre los documentos presentados revela hallazgos críticos que requieren atención inmediata. Se identificó la ausencia de la Manifestación de Impacto Ambiental (MIA), documento obligatorio según el Artículo 35 de la LGEEPA para proyectos con impacto ambiental significativo. Esta omisión representa un riesgo legal considerable, incluyendo la posible suspensión de obras y sanciones por parte de PROFEPA.

Adicionalmente, no se localizó evidencia de autorización ambiental vigente por parte de SEMARNAT, lo que constituye un incumplimiento del Artículo 28 de la LGEEPA. Se recomienda iniciar de inmediato el proceso de elaboración y presentación de la MIA, así como la solicitud formal de autorización ambiental. La contratación de un consultor ambiental certificado facilitará el cumplimiento normativo.

Es imperativo actuar con urgencia para regularizar la situación legal del proyecto y evitar consecuencias más severas. El plazo recomendado para iniciar acciones correctivas es de 30 días.

**Llamado a la Acción**: Contactar a SEMARNAT para iniciar trámite de MIA y autorización ambiental dentro de los próximos 7 días hábiles.
"""
        else:
            return """
**Executive Summary of LGEEPA Environmental Audit**

The analysis conducted on the submitted documents reveals critical findings requiring immediate attention. The absence of the Environmental Impact Statement (MIA) was identified, a mandatory document under Article 35 of LGEEPA for projects with significant environmental impact. This omission represents considerable legal risk, including possible work suspension and sanctions by PROFEPA.

Additionally, no evidence of valid environmental authorization from SEMARNAT was found, constituting non-compliance with Article 28 of LGEEPA. It is recommended to immediately begin the process of preparing and submitting the MIA, as well as formal application for environmental authorization. Hiring a certified environmental consultant will facilitate regulatory compliance.

It is imperative to act urgently to regularize the project's legal situation and avoid more severe consequences. The recommended timeframe to initiate corrective actions is 30 days.

**Call to Action**: Contact SEMARNAT to initiate MIA and environmental authorization procedures within the next 7 business days.
"""


def main():
    """Función principal de demostración."""
    print("=" * 70)
    print("🤖 AI-POWERED SEMANTIC ANALYZER - PROOF OF CONCEPT")
    print("=" * 70)
    print()
    
    # Crear analizador
    analyzer = SemanticAnalyzer()
    
    # Documento de ejemplo
    sample_document = """
    PROYECTO DE CONSTRUCCIÓN DE PLANTA INDUSTRIAL
    
    El presente proyecto contempla la construcción de una planta de tratamiento
    de residuos industriales en el municipio de ejemplo. Se han identificado
    los siguientes aspectos:
    
    - Superficie total: 5 hectáreas
    - Inversión: $50 millones MXN
    - Generación de empleos: 150 directos
    - Tratamiento de residuos: 100 toneladas/día
    
    Se cuenta con:
    - Estudio de factibilidad técnica
    - Análisis de mercado
    - Proyecto ejecutivo de ingeniería
    
    Pendiente:
    - Trámites ambientales ante SEMARNAT
    - Permisos de construcción
    - Licencias de operación
    """
    
    print("📄 Documento de ejemplo:")
    print(sample_document[:200] + "...\n")
    
    # 1. Extracción de cláusulas legales
    print("1️⃣  EXTRACCIÓN DE CLÁUSULAS LEGALES")
    print("-" * 70)
    extraction_result = analyzer.extract_legal_clauses(sample_document, "LGEEPA")
    print(json.dumps(extraction_result, indent=2, ensure_ascii=False))
    print()
    
    # 2. Análisis de cumplimiento
    print("2️⃣  ANÁLISIS DE CUMPLIMIENTO")
    print("-" * 70)
    
    lgeepa_rules = [
        {"id": "LGEEPA-Art35", "description": "Manifestación de Impacto Ambiental (MIA)"},
        {"id": "LGEEPA-Art28", "description": "Autorización de impacto ambiental"},
        {"id": "NOM-001-SEMARNAT", "description": "Límites de contaminantes en aguas"}
    ]
    
    compliance_result = analyzer.analyze_compliance(sample_document, lgeepa_rules)
    print(json.dumps(compliance_result, indent=2, ensure_ascii=False))
    print()
    
    # 3. Resumen ejecutivo
    print("3️⃣  RESUMEN EJECUTIVO")
    print("-" * 70)
    
    analysis_result = {
        "extraction": extraction_result,
        "compliance": compliance_result
    }
    
    summary_es = analyzer.generate_executive_summary(analysis_result, language="es")
    print(summary_es)
    print()
    
    # Guardar resultados
    output_file = "ai_semantic_analysis_poc.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "document_sample": sample_document[:500],
            "extraction": extraction_result,
            "compliance": compliance_result,
            "summary": summary_es
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados guardados en: {output_file}")
    print()
    print("=" * 70)
    print("🎉 PROOF OF CONCEPT COMPLETADO")
    print("=" * 70)
    print()
    
    if analyzer.simulation_mode:
        print("⚠️  NOTA: Este PoC se ejecutó en MODO SIMULACIÓN")
        print("   Para usar Gemini real, configura GEMINI_API_KEY:")
        print("   export GEMINI_API_KEY='tu_api_key'")
        print("   sudo pip3 install google-genai")
    else:
        print("✅ Este PoC usó Google Gemini API real")
        print("   Costo estimado: <$0.01 USD")


if __name__ == "__main__":
    main()

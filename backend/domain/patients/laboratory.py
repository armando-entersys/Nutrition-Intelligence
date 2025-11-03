"""
Laboratory Data Models - Complete implementation based on PLAN_MEXICO_DEFINITIVO.md
"""
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
from sqlalchemy import JSON


class LabTestType(str, Enum):
    """Types of laboratory tests"""
    BLOOD_CHEMISTRY = "blood_chemistry"
    LIPID_PROFILE = "lipid_profile"
    RENAL_FUNCTION = "renal_function"
    LIVER_FUNCTION = "liver_function"
    THYROID_PROFILE = "thyroid_profile"
    COMPLETE_BLOOD_COUNT = "complete_blood_count"
    VITAMINS_MINERALS = "vitamins_minerals"
    OTHER = "other"


class Severity(str, Enum):
    """Severity level for out-of-range values"""
    NORMAL = "normal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Trend(str, Enum):
    """Trend direction for lab values over time"""
    IMPROVING = "improving"
    WORSENING = "worsening"
    STABLE = "stable"


class LaboratoryData(SQLModel, table=True):
    """
    Complete laboratory data model based on Mexican clinical standards
    Follows NOM-004-SSA3-2012 requirements
    """
    __tablename__ = "laboratory_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)

    # Study metadata
    study_date: date
    test_type: LabTestType
    laboratory_name: str = Field(max_length=200)
    ordering_physician: Optional[str] = Field(default=None, max_length=200)

    # Glycemic profile
    fasting_glucose_mgdl: Optional[float] = Field(default=None)
    postprandial_glucose_mgdl: Optional[float] = Field(default=None)
    hemoglobin_a1c_pct: Optional[float] = Field(default=None)
    fasting_insulin_uUI_ml: Optional[float] = Field(default=None)
    homa_ir: Optional[float] = Field(default=None)  # Calculated: (glucose * insulin) / 405

    # Lipid profile
    total_cholesterol_mgdl: Optional[float] = Field(default=None)
    ldl_cholesterol_mgdl: Optional[float] = Field(default=None)
    hdl_cholesterol_mgdl: Optional[float] = Field(default=None)
    triglycerides_mgdl: Optional[float] = Field(default=None)
    atherogenic_index: Optional[float] = Field(default=None)  # Calculated: TC/HDL

    # Renal function
    creatinine_mgdl: Optional[float] = Field(default=None)
    urea_mgdl: Optional[float] = Field(default=None)
    uric_acid_mgdl: Optional[float] = Field(default=None)
    gfr_ml_min: Optional[float] = Field(default=None)  # Glomerular filtration rate

    # Liver function
    alt_tgp_UI_l: Optional[float] = Field(default=None)  # ALT / TGP
    ast_tgo_UI_l: Optional[float] = Field(default=None)  # AST / TGO
    total_bilirubin_mgdl: Optional[float] = Field(default=None)
    alkaline_phosphatase_UI_l: Optional[float] = Field(default=None)
    albumin_g_dl: Optional[float] = Field(default=None)

    # Thyroid profile
    tsh_uUI_ml: Optional[float] = Field(default=None)
    t3_ng_dl: Optional[float] = Field(default=None)
    free_t4_ng_dl: Optional[float] = Field(default=None)

    # Electrolytes
    sodium_mEq_l: Optional[float] = Field(default=None)
    potassium_mEq_l: Optional[float] = Field(default=None)
    calcium_mg_dl: Optional[float] = Field(default=None)
    magnesium_mg_dl: Optional[float] = Field(default=None)

    # Complete blood count
    hemoglobin_g_dl: Optional[float] = Field(default=None)
    hematocrit_pct: Optional[float] = Field(default=None)
    white_blood_cells_mm3: Optional[float] = Field(default=None)
    platelets_mm3: Optional[float] = Field(default=None)

    # Vitamins and minerals
    vitamin_d_ng_ml: Optional[float] = Field(default=None)
    vitamin_b12_pg_ml: Optional[float] = Field(default=None)
    folic_acid_ng_ml: Optional[float] = Field(default=None)
    serum_iron_mcg_dl: Optional[float] = Field(default=None)
    ferritin_ng_ml: Optional[float] = Field(default=None)

    # Other markers
    c_reactive_protein_mg_dl: Optional[float] = Field(default=None)

    # PDF file upload
    pdf_file_url: Optional[str] = Field(default=None, max_length=500)

    # AI Analysis (stored as JSON)
    ai_interpretation: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    uploaded_by_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationships
    patient: "Patient" = Relationship(back_populates="laboratory_records")
    trends: List["LabTrend"] = Relationship(back_populates="lab_data")

    def calculate_derived_values(self):
        """Calculate derived values from basic measurements"""
        # Calculate HOMA-IR
        if self.fasting_glucose_mgdl and self.fasting_insulin_uUI_ml:
            self.homa_ir = (self.fasting_glucose_mgdl * self.fasting_insulin_uUI_ml) / 405

        # Calculate Atherogenic Index
        if self.total_cholesterol_mgdl and self.hdl_cholesterol_mgdl and self.hdl_cholesterol_mgdl > 0:
            self.atherogenic_index = self.total_cholesterol_mgdl / self.hdl_cholesterol_mgdl

    def generate_ai_interpretation(self) -> Dict[str, Any]:
        """
        Generate AI interpretation of lab results
        This would call an AI service in production
        """
        interpretation = {
            "out_of_range_values": [],
            "suggested_diagnoses": [],
            "diet_adjustments": [],
            "additional_tests": [],
            "critical_alerts": []
        }

        # Check glycemic values
        if self.fasting_glucose_mgdl:
            if self.fasting_glucose_mgdl >= 126:
                interpretation["out_of_range_values"].append({
                    "parameter": "Glucosa en ayunas",
                    "value": self.fasting_glucose_mgdl,
                    "normal_range": "70-99 mg/dL",
                    "severity": Severity.SEVERE.value,
                    "clinical_meaning": "Posible diabetes mellitus"
                })
                interpretation["suggested_diagnoses"].append("Diabetes mellitus tipo 2")
                interpretation["diet_adjustments"].append("Reducir consumo de carbohidratos simples")
                interpretation["diet_adjustments"].append("Aumentar fibra soluble")
            elif self.fasting_glucose_mgdl >= 100:
                interpretation["out_of_range_values"].append({
                    "parameter": "Glucosa en ayunas",
                    "value": self.fasting_glucose_mgdl,
                    "normal_range": "70-99 mg/dL",
                    "severity": Severity.MILD.value,
                    "clinical_meaning": "Prediabetes - Glucosa alterada en ayunas"
                })
                interpretation["suggested_diagnoses"].append("Prediabetes")
                interpretation["additional_tests"].append("Hemoglobina glucosilada (HbA1c)")

        # Check HbA1c
        if self.hemoglobin_a1c_pct:
            if self.hemoglobin_a1c_pct >= 6.5:
                interpretation["out_of_range_values"].append({
                    "parameter": "Hemoglobina A1c",
                    "value": self.hemoglobin_a1c_pct,
                    "normal_range": "<5.7%",
                    "severity": Severity.SEVERE.value,
                    "clinical_meaning": "Diabetes mellitus establecida"
                })
                interpretation["critical_alerts"].append("HbA1c elevada - Requiere manejo médico urgente")

        # Check lipid profile
        if self.total_cholesterol_mgdl and self.total_cholesterol_mgdl >= 240:
            interpretation["out_of_range_values"].append({
                "parameter": "Colesterol total",
                "value": self.total_cholesterol_mgdl,
                "normal_range": "<200 mg/dL",
                "severity": Severity.MODERATE.value,
                "clinical_meaning": "Hipercolesterolemia"
            })
            interpretation["diet_adjustments"].append("Reducir grasas saturadas y trans")
            interpretation["diet_adjustments"].append("Aumentar omega-3 (pescado, nueces)")

        if self.ldl_cholesterol_mgdl and self.ldl_cholesterol_mgdl >= 160:
            interpretation["out_of_range_values"].append({
                "parameter": "LDL (colesterol malo)",
                "value": self.ldl_cholesterol_mgdl,
                "normal_range": "<100 mg/dL",
                "severity": Severity.MODERATE.value,
                "clinical_meaning": "LDL elevado - Riesgo cardiovascular"
            })

        if self.triglycerides_mgdl and self.triglycerides_mgdl >= 200:
            interpretation["out_of_range_values"].append({
                "parameter": "Triglicéridos",
                "value": self.triglycerides_mgdl,
                "normal_range": "<150 mg/dL",
                "severity": Severity.MODERATE.value,
                "clinical_meaning": "Hipertrigliceridemia"
            })
            interpretation["diet_adjustments"].append("Reducir azúcares simples y alcohol")
            interpretation["diet_adjustments"].append("Aumentar ejercicio aeróbico")

        # Check renal function
        if self.creatinine_mgdl and self.creatinine_mgdl >= 1.5:
            interpretation["out_of_range_values"].append({
                "parameter": "Creatinina",
                "value": self.creatinine_mgdl,
                "normal_range": "0.6-1.2 mg/dL",
                "severity": Severity.MODERATE.value,
                "clinical_meaning": "Posible deterioro de función renal"
            })
            interpretation["critical_alerts"].append("Creatinina elevada - Evaluar función renal")
            interpretation["additional_tests"].append("Depuración de creatinina en orina de 24h")

        # Check liver function
        if self.alt_tgp_UI_l and self.alt_tgp_UI_l > 40:
            interpretation["out_of_range_values"].append({
                "parameter": "ALT/TGP",
                "value": self.alt_tgp_UI_l,
                "normal_range": "7-40 UI/L",
                "severity": Severity.MILD.value if self.alt_tgp_UI_l < 80 else Severity.MODERATE.value,
                "clinical_meaning": "Posible daño hepático o hígado graso"
            })
            interpretation["diet_adjustments"].append("Evitar alcohol completamente")
            interpretation["diet_adjustments"].append("Reducir grasas saturadas")

        # Check anemia
        if self.hemoglobin_g_dl:
            if self.hemoglobin_g_dl < 12:  # For women
                interpretation["out_of_range_values"].append({
                    "parameter": "Hemoglobina",
                    "value": self.hemoglobin_g_dl,
                    "normal_range": "12-16 g/dL (mujeres), 14-18 g/dL (hombres)",
                    "severity": Severity.MODERATE.value,
                    "clinical_meaning": "Anemia"
                })
                interpretation["diet_adjustments"].append("Aumentar hierro (carnes rojas magras, legumbres)")
                interpretation["diet_adjustments"].append("Vitamina C para mejorar absorción de hierro")
                interpretation["additional_tests"].append("Perfil de hierro sérico")

        # Check vitamin D
        if self.vitamin_d_ng_ml and self.vitamin_d_ng_ml < 20:
            interpretation["out_of_range_values"].append({
                "parameter": "Vitamina D",
                "value": self.vitamin_d_ng_ml,
                "normal_range": "30-100 ng/mL",
                "severity": Severity.MILD.value,
                "clinical_meaning": "Deficiencia de vitamina D"
            })
            interpretation["diet_adjustments"].append("Aumentar exposición solar 15-20 min diarios")
            interpretation["diet_adjustments"].append("Alimentos fortificados con vitamina D")

        self.ai_interpretation = interpretation
        return interpretation


class LabTrend(SQLModel, table=True):
    """
    Tracks trends of laboratory values over time
    Automatically calculated when multiple lab results exist
    """
    __tablename__ = "lab_trends"

    id: Optional[int] = Field(default=None, primary_key=True)
    lab_data_id: int = Field(foreign_key="laboratory_data.id", index=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)

    parameter_name: str = Field(max_length=100)
    current_value: float
    previous_value: Optional[float] = Field(default=None)
    direction: Trend
    percent_change: Optional[float] = Field(default=None)

    # Metadata
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    lab_data: LaboratoryData = Relationship(back_populates="trends")


class ClinicalFile(SQLModel, table=True):
    """
    Clinical files with OCR capability
    Stores PDFs, images, and other clinical documents
    """
    __tablename__ = "clinical_files"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id", index=True)

    # File metadata
    file_type: str = Field(max_length=50)  # 'laboratory', 'radiology', 'ultrasound', 'prescription', 'consent', 'other'
    file_name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    document_date: Optional[date] = Field(default=None)

    # File storage
    file_url: str = Field(max_length=500)
    file_format: str = Field(max_length=10)  # 'pdf', 'jpg', 'png', 'doc'
    file_size_mb: Optional[float] = Field(default=None)

    # OCR & AI extraction
    ocr_processed: bool = Field(default=False)
    extracted_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    # Tagging for quick search
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Metadata
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploaded_by: str = Field(max_length=50)  # 'nutritionist' or 'patient'
    uploaded_by_id: int = Field(foreign_key="users.id")

    # Relationships
    patient: "Patient" = Relationship(back_populates="clinical_files")

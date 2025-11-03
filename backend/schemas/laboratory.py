"""
Pydantic schemas for Laboratory Data API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


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


# Request schemas
class LaboratoryDataCreate(BaseModel):
    """Schema for creating new laboratory data"""
    patient_id: int
    study_date: date
    test_type: LabTestType
    laboratory_name: str = Field(max_length=200)
    ordering_physician: Optional[str] = None

    # Glycemic profile
    fasting_glucose_mgdl: Optional[float] = None
    postprandial_glucose_mgdl: Optional[float] = None
    hemoglobin_a1c_pct: Optional[float] = None
    fasting_insulin_uUI_ml: Optional[float] = None
    homa_ir: Optional[float] = None

    # Lipid profile
    total_cholesterol_mgdl: Optional[float] = None
    ldl_cholesterol_mgdl: Optional[float] = None
    hdl_cholesterol_mgdl: Optional[float] = None
    triglycerides_mgdl: Optional[float] = None
    atherogenic_index: Optional[float] = None

    # Renal function
    creatinine_mgdl: Optional[float] = None
    urea_mgdl: Optional[float] = None
    uric_acid_mgdl: Optional[float] = None
    gfr_ml_min: Optional[float] = None

    # Liver function
    alt_tgp_UI_l: Optional[float] = None
    ast_tgo_UI_l: Optional[float] = None
    total_bilirubin_mgdl: Optional[float] = None
    alkaline_phosphatase_UI_l: Optional[float] = None
    albumin_g_dl: Optional[float] = None

    # Thyroid profile
    tsh_uUI_ml: Optional[float] = None
    t3_ng_dl: Optional[float] = None
    free_t4_ng_dl: Optional[float] = None

    # Electrolytes
    sodium_mEq_l: Optional[float] = None
    potassium_mEq_l: Optional[float] = None
    calcium_mg_dl: Optional[float] = None
    magnesium_mg_dl: Optional[float] = None

    # Complete blood count
    hemoglobin_g_dl: Optional[float] = None
    hematocrit_pct: Optional[float] = None
    white_blood_cells_mm3: Optional[float] = None
    platelets_mm3: Optional[float] = None

    # Vitamins and minerals
    vitamin_d_ng_ml: Optional[float] = None
    vitamin_b12_pg_ml: Optional[float] = None
    folic_acid_ng_ml: Optional[float] = None
    serum_iron_mcg_dl: Optional[float] = None
    ferritin_ng_ml: Optional[float] = None

    # Other markers
    c_reactive_protein_mg_dl: Optional[float] = None

    # PDF file upload
    pdf_file_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": 1,
                "study_date": "2025-01-15",
                "test_type": "blood_chemistry",
                "laboratory_name": "Laboratorio Chopo",
                "ordering_physician": "Dr. Juan Pérez",
                "fasting_glucose_mgdl": 95.0,
                "hemoglobin_a1c_pct": 5.5,
                "total_cholesterol_mgdl": 180.0,
                "ldl_cholesterol_mgdl": 100.0,
                "hdl_cholesterol_mgdl": 55.0,
                "triglycerides_mgdl": 125.0
            }
        }


class LaboratoryDataUpdate(BaseModel):
    """Schema for updating laboratory data"""
    study_date: Optional[date] = None
    test_type: Optional[LabTestType] = None
    laboratory_name: Optional[str] = None
    ordering_physician: Optional[str] = None

    # All lab values optional for partial updates
    fasting_glucose_mgdl: Optional[float] = None
    postprandial_glucose_mgdl: Optional[float] = None
    hemoglobin_a1c_pct: Optional[float] = None
    # ... (other fields)


# Response schemas
class OutOfRangeValue(BaseModel):
    """Schema for out-of-range laboratory value"""
    parameter: str
    value: float
    normal_range: str
    severity: Severity
    clinical_meaning: str


class AIInterpretation(BaseModel):
    """Schema for AI interpretation of lab results"""
    out_of_range_values: List[OutOfRangeValue]
    suggested_diagnoses: List[str]
    diet_adjustments: List[str]
    additional_tests: List[str]
    critical_alerts: List[str]


class LabTrendResponse(BaseModel):
    """Schema for laboratory trend response"""
    id: int
    parameter_name: str
    current_value: float
    previous_value: Optional[float]
    direction: Trend
    percent_change: Optional[float]
    calculated_at: datetime

    class Config:
        from_attributes = True


class LaboratoryDataResponse(BaseModel):
    """Schema for laboratory data response"""
    id: int
    patient_id: int
    study_date: date
    test_type: LabTestType
    laboratory_name: str
    ordering_physician: Optional[str]

    # All lab values
    fasting_glucose_mgdl: Optional[float]
    postprandial_glucose_mgdl: Optional[float]
    hemoglobin_a1c_pct: Optional[float]
    fasting_insulin_uUI_ml: Optional[float]
    homa_ir: Optional[float]

    total_cholesterol_mgdl: Optional[float]
    ldl_cholesterol_mgdl: Optional[float]
    hdl_cholesterol_mgdl: Optional[float]
    triglycerides_mgdl: Optional[float]
    atherogenic_index: Optional[float]

    creatinine_mgdl: Optional[float]
    urea_mgdl: Optional[float]
    uric_acid_mgdl: Optional[float]
    gfr_ml_min: Optional[float]

    alt_tgp_UI_l: Optional[float]
    ast_tgo_UI_l: Optional[float]
    total_bilirubin_mgdl: Optional[float]
    alkaline_phosphatase_UI_l: Optional[float]
    albumin_g_dl: Optional[float]

    tsh_uUI_ml: Optional[float]
    t3_ng_dl: Optional[float]
    free_t4_ng_dl: Optional[float]

    sodium_mEq_l: Optional[float]
    potassium_mEq_l: Optional[float]
    calcium_mg_dl: Optional[float]
    magnesium_mg_dl: Optional[float]

    hemoglobin_g_dl: Optional[float]
    hematocrit_pct: Optional[float]
    white_blood_cells_mm3: Optional[float]
    platelets_mm3: Optional[float]

    vitamin_d_ng_ml: Optional[float]
    vitamin_b12_pg_ml: Optional[float]
    folic_acid_ng_ml: Optional[float]
    serum_iron_mcg_dl: Optional[float]
    ferritin_ng_ml: Optional[float]

    c_reactive_protein_mg_dl: Optional[float]

    pdf_file_url: Optional[str]
    ai_interpretation: Optional[Dict[str, Any]]

    created_at: datetime
    updated_at: Optional[datetime]
    uploaded_by_id: Optional[int]

    # Include trends if requested
    trends: Optional[List[LabTrendResponse]] = None

    class Config:
        from_attributes = True


class ClinicalFileCreate(BaseModel):
    """Schema for creating clinical file"""
    patient_id: int
    file_type: str
    file_name: str
    description: Optional[str] = None
    document_date: Optional[date] = None
    file_url: str
    file_format: str
    file_size_mb: Optional[float] = None
    tags: Optional[List[str]] = None
    uploaded_by: str  # 'nutritionist' or 'patient'


class ClinicalFileResponse(BaseModel):
    """Schema for clinical file response"""
    id: int
    patient_id: int
    file_type: str
    file_name: str
    description: Optional[str]
    document_date: Optional[date]
    file_url: str
    file_format: str
    file_size_mb: Optional[float]
    ocr_processed: bool
    extracted_data: Optional[Dict[str, Any]]
    tags: Optional[List[str]]
    uploaded_at: datetime
    uploaded_by: str
    uploaded_by_id: int

    class Config:
        from_attributes = True


class LaboratoryDataListResponse(BaseModel):
    """Schema for paginated list of laboratory data"""
    total: int
    page: int
    page_size: int
    items: List[LaboratoryDataResponse]


class LabComparison(BaseModel):
    """Schema for comparing lab results over time"""
    parameter_name: str
    values: List[Dict[str, Any]]  # [{date: ..., value: ...}, ...]
    trend: Trend
    normal_range: str
    interpretation: str

"""
Laboratory Data API Routes
Complete implementation for managing laboratory results with AI interpretation
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlmodel import Session, select, and_, or_, func, desc
from typing import List, Optional
from datetime import date, datetime, timedelta
import os
import shutil
from pathlib import Path
import uuid

from core.database import get_session
from domain.patients.laboratory import LaboratoryData, LabTrend, ClinicalFile
from domain.patients.models import Patient
from schemas.laboratory import (
    LaboratoryDataCreate,
    LaboratoryDataUpdate,
    LaboratoryDataResponse,
    LaboratoryDataListResponse,
    LabTrendResponse,
    ClinicalFileCreate,
    ClinicalFileResponse,
    LabComparison,
    Trend
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/laboratory", tags=["Laboratory Data"])


# ============================================================================
# LABORATORY DATA CRUD ENDPOINTS
# ============================================================================

@router.post("/", response_model=LaboratoryDataResponse, status_code=status.HTTP_201_CREATED)
async def create_laboratory_data(
    lab_data: LaboratoryDataCreate,
    session: Session = Depends(get_session)
):
    """
    Create new laboratory data record with AI interpretation

    Automatically calculates derived values (HOMA-IR, atherogenic index)
    and generates AI interpretation of results
    """
    try:
        # Verify patient exists
        patient = session.get(Patient, lab_data.patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with id {lab_data.patient_id} not found"
            )

        # Create laboratory data record
        db_lab_data = LaboratoryData(**lab_data.model_dump())

        # Calculate derived values
        db_lab_data.calculate_derived_values()

        # Generate AI interpretation
        db_lab_data.generate_ai_interpretation()

        session.add(db_lab_data)
        session.commit()
        session.refresh(db_lab_data)

        # Calculate trends if previous data exists
        await _calculate_trends(session, db_lab_data)

        logger.info(f"Created laboratory data record {db_lab_data.id} for patient {lab_data.patient_id}")

        return db_lab_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error creating laboratory data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating laboratory data: {str(e)}"
        )


@router.get("/{lab_id}", response_model=LaboratoryDataResponse)
async def get_laboratory_data(
    lab_id: int,
    include_trends: bool = Query(default=False),
    session: Session = Depends(get_session)
):
    """
    Get specific laboratory data record by ID

    Args:
        lab_id: Laboratory data record ID
        include_trends: Whether to include trend analysis
    """
    lab_data = session.get(LaboratoryData, lab_id)

    if not lab_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laboratory data with id {lab_id} not found"
        )

    if include_trends:
        # Load trends
        trends = session.exec(
            select(LabTrend).where(LabTrend.lab_data_id == lab_id)
        ).all()
        lab_data.trends = trends

    return lab_data


@router.get("/patient/{patient_id}", response_model=LaboratoryDataListResponse)
async def get_patient_laboratory_data(
    patient_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    test_type: Optional[str] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    session: Session = Depends(get_session)
):
    """
    Get all laboratory data for a specific patient with filters

    Args:
        patient_id: Patient ID
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        test_type: Filter by test type
        date_from: Filter from date
        date_to: Filter to date
    """
    # Verify patient exists
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )

    # Build query
    query = select(LaboratoryData).where(LaboratoryData.patient_id == patient_id)

    if test_type:
        query = query.where(LaboratoryData.test_type == test_type)

    if date_from:
        query = query.where(LaboratoryData.study_date >= date_from)

    if date_to:
        query = query.where(LaboratoryData.study_date <= date_to)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Execute paginated query
    query = query.order_by(desc(LaboratoryData.study_date))
    query = query.offset(skip).limit(limit)
    items = session.exec(query).all()

    return LaboratoryDataListResponse(
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


@router.put("/{lab_id}", response_model=LaboratoryDataResponse)
async def update_laboratory_data(
    lab_id: int,
    lab_update: LaboratoryDataUpdate,
    session: Session = Depends(get_session)
):
    """
    Update laboratory data record

    Recalculates derived values and AI interpretation after update
    """
    db_lab_data = session.get(LaboratoryData, lab_id)

    if not db_lab_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laboratory data with id {lab_id} not found"
        )

    try:
        # Update fields
        update_data = lab_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lab_data, key, value)

        # Recalculate derived values
        db_lab_data.calculate_derived_values()

        # Regenerate AI interpretation
        db_lab_data.generate_ai_interpretation()

        db_lab_data.updated_at = datetime.utcnow()

        session.add(db_lab_data)
        session.commit()
        session.refresh(db_lab_data)

        # Recalculate trends
        await _calculate_trends(session, db_lab_data)

        logger.info(f"Updated laboratory data record {lab_id}")

        return db_lab_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error updating laboratory data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating laboratory data: {str(e)}"
        )


@router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_laboratory_data(
    lab_id: int,
    session: Session = Depends(get_session)
):
    """Delete laboratory data record"""
    db_lab_data = session.get(LaboratoryData, lab_id)

    if not db_lab_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laboratory data with id {lab_id} not found"
        )

    try:
        # Delete associated trends first
        trends = session.exec(
            select(LabTrend).where(LabTrend.lab_data_id == lab_id)
        ).all()
        for trend in trends:
            session.delete(trend)

        session.delete(db_lab_data)
        session.commit()

        logger.info(f"Deleted laboratory data record {lab_id}")

    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting laboratory data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting laboratory data: {str(e)}"
        )


# ============================================================================
# TREND ANALYSIS ENDPOINTS
# ============================================================================

@router.get("/trends/patient/{patient_id}", response_model=List[LabComparison])
async def get_patient_lab_trends(
    patient_id: int,
    parameters: Optional[str] = Query(
        default=None,
        description="Comma-separated list of parameters to analyze (e.g., 'fasting_glucose_mgdl,hemoglobin_a1c_pct')"
    ),
    months_back: int = Query(default=6, ge=1, le=24),
    session: Session = Depends(get_session)
):
    """
    Get laboratory trends for specific parameters over time

    Shows how lab values have changed and their interpretation
    """
    # Verify patient exists
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )

    # Calculate date range
    date_from = datetime.now().date() - timedelta(days=months_back * 30)

    # Get all lab data in range
    query = select(LaboratoryData).where(
        and_(
            LaboratoryData.patient_id == patient_id,
            LaboratoryData.study_date >= date_from
        )
    ).order_by(LaboratoryData.study_date)

    lab_records = session.exec(query).all()

    if not lab_records:
        return []

    # Define parameters to analyze
    if parameters:
        param_list = [p.strip() for p in parameters.split(',')]
    else:
        # Default important parameters
        param_list = [
            'fasting_glucose_mgdl',
            'hemoglobin_a1c_pct',
            'total_cholesterol_mgdl',
            'ldl_cholesterol_mgdl',
            'hdl_cholesterol_mgdl',
            'triglycerides_mgdl',
            'creatinine_mgdl',
            'alt_tgp_UI_l'
        ]

    comparisons = []

    for param in param_list:
        values = []
        for record in lab_records:
            value = getattr(record, param, None)
            if value is not None:
                values.append({
                    "date": record.study_date.isoformat(),
                    "value": value
                })

        if len(values) >= 2:
            # Calculate trend
            first_value = values[0]['value']
            last_value = values[-1]['value']

            if last_value < first_value:
                trend = Trend.IMPROVING if _is_lower_better(param) else Trend.WORSENING
            elif last_value > first_value:
                trend = Trend.WORSENING if _is_lower_better(param) else Trend.IMPROVING
            else:
                trend = Trend.STABLE

            comparison = LabComparison(
                parameter_name=_format_parameter_name(param),
                values=values,
                trend=trend,
                normal_range=_get_normal_range(param),
                interpretation=_get_trend_interpretation(param, trend, first_value, last_value)
            )
            comparisons.append(comparison)

    return comparisons


# ============================================================================
# AI ANALYSIS ENDPOINTS
# ============================================================================

@router.post("/{lab_id}/reanalyze", response_model=LaboratoryDataResponse)
async def reanalyze_laboratory_data(
    lab_id: int,
    session: Session = Depends(get_session)
):
    """
    Regenerate AI interpretation for laboratory data

    Useful after updating reference ranges or AI algorithms
    """
    db_lab_data = session.get(LaboratoryData, lab_id)

    if not db_lab_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laboratory data with id {lab_id} not found"
        )

    try:
        # Recalculate derived values
        db_lab_data.calculate_derived_values()

        # Regenerate AI interpretation
        db_lab_data.generate_ai_interpretation()

        db_lab_data.updated_at = datetime.utcnow()

        session.add(db_lab_data)
        session.commit()
        session.refresh(db_lab_data)

        logger.info(f"Reanalyzed laboratory data record {lab_id}")

        return db_lab_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error reanalyzing laboratory data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reanalyzing laboratory data: {str(e)}"
        )


# ============================================================================
# CLINICAL FILES ENDPOINTS
# ============================================================================

@router.post("/files/", response_model=ClinicalFileResponse, status_code=status.HTTP_201_CREATED)
async def create_clinical_file(
    file_data: ClinicalFileCreate,
    session: Session = Depends(get_session)
):
    """
    Create clinical file record

    Note: File upload should be done separately, this endpoint just stores metadata
    """
    try:
        # Verify patient exists
        patient = session.get(Patient, file_data.patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with id {file_data.patient_id} not found"
            )

        db_file = ClinicalFile(**file_data.model_dump())

        session.add(db_file)
        session.commit()
        session.refresh(db_file)

        logger.info(f"Created clinical file {db_file.id} for patient {file_data.patient_id}")

        return db_file

    except Exception as e:
        session.rollback()
        logger.error(f"Error creating clinical file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating clinical file: {str(e)}"
        )


@router.get("/files/patient/{patient_id}", response_model=List[ClinicalFileResponse])
async def get_patient_clinical_files(
    patient_id: int,
    file_type: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    """Get all clinical files for a patient"""
    # Verify patient exists
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )

    query = select(ClinicalFile).where(ClinicalFile.patient_id == patient_id)

    if file_type:
        query = query.where(ClinicalFile.file_type == file_type)

    query = query.order_by(desc(ClinicalFile.uploaded_at))
    files = session.exec(query).all()

    return files


@router.post("/files/upload", response_model=ClinicalFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_clinical_file(
    patient_id: int,
    file: UploadFile = File(...),
    file_type: str = "other",
    description: Optional[str] = None,
    document_date: Optional[str] = None,
    uploaded_by: str = "nutritionist",
    uploaded_by_id: int = 1,
    session: Session = Depends(get_session)
):
    """
    Upload clinical file with OCR processing

    Supported formats: PDF, JPG, PNG, JPEG
    File types: laboratory, radiology, ultrasound, prescription, consent, other
    """
    try:
        # Verify patient exists
        patient = session.get(Patient, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with id {patient_id} not found"
            )

        # Validate file type
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not supported. Allowed: {', '.join(allowed_extensions)}"
            )

        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads") / "clinical_files" / str(patient_id)
        uploads_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        safe_filename = f"{unique_id}_{file.filename}"
        file_path = uploads_dir / safe_filename

        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)

        # Process OCR
        extracted_data = await _process_ocr(file_path, file_extension)

        # Create database record
        db_file = ClinicalFile(
            patient_id=patient_id,
            file_type=file_type,
            file_name=file.filename,
            description=description,
            document_date=datetime.strptime(document_date, "%Y-%m-%d").date() if document_date else None,
            file_url=str(file_path),
            file_format=file_extension.replace('.', ''),
            file_size_mb=round(file_size_mb, 2),
            ocr_processed=extracted_data is not None,
            extracted_data=extracted_data,
            uploaded_by=uploaded_by,
            uploaded_by_id=uploaded_by_id
        )

        session.add(db_file)
        session.commit()
        session.refresh(db_file)

        logger.info(f"Uploaded clinical file {db_file.id} for patient {patient_id}")
        return db_file

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading clinical file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
    finally:
        file.file.close()


@router.get("/files/{file_id}", response_model=ClinicalFileResponse)
async def get_clinical_file(
    file_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific clinical file"""
    db_file = session.get(ClinicalFile, file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clinical file with id {file_id} not found"
        )
    return db_file


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clinical_file(
    file_id: int,
    session: Session = Depends(get_session)
):
    """Delete a clinical file"""
    db_file = session.get(ClinicalFile, file_id)
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clinical file with id {file_id} not found"
        )

    # Delete physical file
    try:
        file_path = Path(db_file.file_url)
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        logger.warning(f"Could not delete physical file: {e}")

    # Delete database record
    session.delete(db_file)
    session.commit()

    logger.info(f"Deleted clinical file {file_id}")
    return None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def _calculate_trends(session: Session, lab_data: LaboratoryData):
    """Calculate trends by comparing with previous lab data"""
    # Get previous lab data for this patient
    previous_lab = session.exec(
        select(LaboratoryData)
        .where(
            and_(
                LaboratoryData.patient_id == lab_data.patient_id,
                LaboratoryData.study_date < lab_data.study_date
            )
        )
        .order_by(desc(LaboratoryData.study_date))
        .limit(1)
    ).first()

    if not previous_lab:
        return

    # Define parameters to track
    parameters = [
        ('fasting_glucose_mgdl', 'Glucosa en ayunas'),
        ('hemoglobin_a1c_pct', 'Hemoglobina A1c'),
        ('total_cholesterol_mgdl', 'Colesterol total'),
        ('ldl_cholesterol_mgdl', 'LDL'),
        ('hdl_cholesterol_mgdl', 'HDL'),
        ('triglycerides_mgdl', 'Triglicéridos'),
        ('creatinine_mgdl', 'Creatinina'),
        ('alt_tgp_UI_l', 'ALT/TGP')
    ]

    for param_key, param_name in parameters:
        current_value = getattr(lab_data, param_key, None)
        previous_value = getattr(previous_lab, param_key, None)

        if current_value is not None and previous_value is not None:
            # Calculate trend
            if current_value < previous_value:
                direction = Trend.IMPROVING if _is_lower_better(param_key) else Trend.WORSENING
            elif current_value > previous_value:
                direction = Trend.WORSENING if _is_lower_better(param_key) else Trend.IMPROVING
            else:
                direction = Trend.STABLE

            percent_change = ((current_value - previous_value) / previous_value) * 100 if previous_value != 0 else 0

            trend = LabTrend(
                lab_data_id=lab_data.id,
                patient_id=lab_data.patient_id,
                parameter_name=param_name,
                current_value=current_value,
                previous_value=previous_value,
                direction=direction,
                percent_change=round(percent_change, 2)
            )

            session.add(trend)

    session.commit()


def _is_lower_better(parameter: str) -> bool:
    """Determine if lower values are better for this parameter"""
    lower_is_better = [
        'fasting_glucose_mgdl',
        'postprandial_glucose_mgdl',
        'hemoglobin_a1c_pct',
        'total_cholesterol_mgdl',
        'ldl_cholesterol_mgdl',
        'triglycerides_mgdl',
        'creatinine_mgdl',
        'uric_acid_mgdl',
        'alt_tgp_UI_l',
        'ast_tgo_UI_l'
    ]
    return parameter in lower_is_better


def _format_parameter_name(param: str) -> str:
    """Format parameter name for display"""
    names = {
        'fasting_glucose_mgdl': 'Glucosa en ayunas (mg/dL)',
        'hemoglobin_a1c_pct': 'Hemoglobina A1c (%)',
        'total_cholesterol_mgdl': 'Colesterol total (mg/dL)',
        'ldl_cholesterol_mgdl': 'LDL (mg/dL)',
        'hdl_cholesterol_mgdl': 'HDL (mg/dL)',
        'triglycerides_mgdl': 'Triglicéridos (mg/dL)',
        'creatinine_mgdl': 'Creatinina (mg/dL)',
        'alt_tgp_UI_l': 'ALT/TGP (UI/L)'
    }
    return names.get(param, param)


def _get_normal_range(param: str) -> str:
    """Get normal range for parameter"""
    ranges = {
        'fasting_glucose_mgdl': '70-99 mg/dL',
        'hemoglobin_a1c_pct': '<5.7%',
        'total_cholesterol_mgdl': '<200 mg/dL',
        'ldl_cholesterol_mgdl': '<100 mg/dL',
        'hdl_cholesterol_mgdl': '>40 mg/dL (H), >50 mg/dL (M)',
        'triglycerides_mgdl': '<150 mg/dL',
        'creatinine_mgdl': '0.6-1.2 mg/dL',
        'alt_tgp_UI_l': '7-40 UI/L'
    }
    return ranges.get(param, 'Ver referencia de laboratorio')


def _get_trend_interpretation(param: str, trend: Trend, first_value: float, last_value: float) -> str:
    """Generate interpretation of trend"""
    change = last_value - first_value
    percent = (change / first_value * 100) if first_value != 0 else 0

    if trend == Trend.IMPROVING:
        return f"Mejorando: {abs(percent):.1f}% {'reducción' if change < 0 else 'aumento'} respecto al valor anterior"
    elif trend == Trend.WORSENING:
        return f"Empeorando: {abs(percent):.1f}% {'aumento' if change > 0 else 'reducción'} respecto al valor anterior"
    else:
        return "Estable: Sin cambios significativos"


async def _process_ocr(file_path: Path, file_extension: str) -> Optional[dict]:
    """
    Process OCR on uploaded file

    For PDFs: Extract embedded text
    For Images: Use OCR (placeholder for now, can integrate Tesseract later)
    """
    try:
        extracted_text = ""

        if file_extension == '.pdf':
            # For PDFs, try to extract embedded text using PyMuPDF
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                for page in doc:
                    extracted_text += page.get_text()
                doc.close()
            except ImportError:
                logger.warning("PyMuPDF (fitz) not installed. PDF text extraction disabled.")
                return None
            except Exception as e:
                logger.error(f"Error extracting text from PDF: {e}")
                return None

        elif file_extension in {'.jpg', '.jpeg', '.png'}:
            # For images, use OCR (placeholder - can integrate Tesseract)
            try:
                # Placeholder for OCR
                # In production, integrate pytesseract or cloud OCR service
                logger.info("Image OCR processing - placeholder (install pytesseract for actual OCR)")

                # Try tesseract if available
                try:
                    import pytesseract
                    from PIL import Image

                    image = Image.open(file_path)
                    extracted_text = pytesseract.image_to_string(image, lang='spa')
                except ImportError:
                    logger.warning("pytesseract not installed. Image OCR disabled.")
                    return None

            except Exception as e:
                logger.error(f"Error processing image OCR: {e}")
                return None

        if extracted_text.strip():
            # Analyze extracted text for clinical data
            analysis = _analyze_clinical_text(extracted_text)

            return {
                "raw_text": extracted_text[:5000],  # Limit to 5000 chars
                "text_length": len(extracted_text),
                "analysis": analysis,
                "processing_date": datetime.utcnow().isoformat()
            }

        return None

    except Exception as e:
        logger.error(f"Unexpected error in OCR processing: {e}")
        return None


def _analyze_clinical_text(text: str) -> dict:
    """
    Analyze extracted text for clinical data
    Uses simple keyword matching - can be enhanced with NLP/AI
    """
    analysis = {
        "detected_values": [],
        "keywords_found": [],
        "document_type": "unknown"
    }

    text_lower = text.lower()

    # Detect document type
    if any(word in text_lower for word in ['glucosa', 'hemoglobina', 'colesterol', 'triglicéridos']):
        analysis["document_type"] = "laboratory"
        analysis["keywords_found"].extend(['resultados de laboratorio'])

    if any(word in text_lower for word in ['ultrasonido', 'ecografía', 'radiografía']):
        analysis["document_type"] = "radiology"
        analysis["keywords_found"].extend(['estudio de imagen'])

    if any(word in text_lower for word in ['receta', 'medicamento', 'tratamiento']):
        analysis["document_type"] = "prescription"
        analysis["keywords_found"].extend(['receta médica'])

    # Extract simple numeric values (very basic - can be enhanced)
    import re

    # Look for glucose values
    glucose_pattern = r'glucosa[:\s]+(\d+\.?\d*)\s*mg/dl'
    glucose_match = re.search(glucose_pattern, text_lower)
    if glucose_match:
        analysis["detected_values"].append({
            "parameter": "Glucosa",
            "value": float(glucose_match.group(1)),
            "unit": "mg/dL"
        })

    # Look for cholesterol
    cholesterol_pattern = r'colesterol\s+total[:\s]+(\d+\.?\d*)\s*mg/dl'
    cholesterol_match = re.search(cholesterol_pattern, text_lower)
    if cholesterol_match:
        analysis["detected_values"].append({
            "parameter": "Colesterol Total",
            "value": float(cholesterol_match.group(1)),
            "unit": "mg/dL"
        })

    return analysis

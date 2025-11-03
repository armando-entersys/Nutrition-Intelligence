"""
Unit Tests for Laboratory Data Models
Tests cover the test cases defined in TESTING_PLAN.md

Test IDs covered:
- UT-LAB-001: Valid laboratory data creation
- UT-LAB-002: Validation of out-of-range values
- UT-LAB-003: Automatic HOMA-IR calculation
- UT-LAB-004: Diabetes detection via HbA1c
- UT-LAB-005: High atherogenic index detection
"""
import pytest
from datetime import date
from domain.patients.laboratory import (
    LaboratoryData,
    LabTestType,
    Severity,
    Trend
)


@pytest.mark.unit
class TestLaboratoryDataModels:
    """Unit tests for Laboratory Data Models"""

    def test_create_valid_laboratory_data(self, sample_lab_data_dict):
        """
        UT-LAB-001: Creación de laboratorio válido

        Test that a LaboratoryData object can be created with complete valid data.
        Verifies all required fields are properly set.
        """
        # Arrange & Act
        lab_data = LaboratoryData(**sample_lab_data_dict)

        # Assert
        assert lab_data.patient_id == 1
        assert lab_data.study_date == date(2025, 1, 15)
        assert lab_data.test_type == LabTestType.BLOOD_CHEMISTRY
        assert lab_data.laboratory_name == "Laboratorio Chopo"
        assert lab_data.fasting_glucose_mgdl == 95.0
        assert lab_data.hemoglobin_a1c_pct == 5.5
        assert lab_data.total_cholesterol_mgdl == 180.0
        assert lab_data.hdl_cholesterol_mgdl == 55.0

        # Verify object is properly instantiated
        assert isinstance(lab_data, LaboratoryData)

    def test_out_of_range_glucose_value_alert(self, sample_lab_data_high_values):
        """
        UT-LAB-002: Validación de valores fuera de rango

        Test that glucose values outside normal range (300 mg/dL) trigger
        appropriate alerts in AI interpretation with correct severity level.
        """
        # Arrange
        lab_data = LaboratoryData(**sample_lab_data_high_values)

        # Act
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        assert len(interpretation["out_of_range_values"]) > 0

        # Find glucose entry in out-of-range values
        glucose_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if "glucosa" in alert["parameter"].lower()
        ]

        assert len(glucose_alerts) > 0
        glucose_alert = glucose_alerts[0]

        assert glucose_alert["value"] == 300.0
        assert glucose_alert["severity"] == Severity.SEVERE.value
        assert "diabetes" in glucose_alert["clinical_meaning"].lower()

        # Verify critical alerts are generated
        assert len(interpretation["critical_alerts"]) > 0 or \
               len(interpretation["suggested_diagnoses"]) > 0

    def test_automatic_homa_ir_calculation(self):
        """
        UT-LAB-003: Cálculo automático HOMA-IR

        Test that HOMA-IR is automatically calculated correctly using the formula:
        HOMA-IR = (Glucose × Insulin) / 405

        Example: Glucose=100 mg/dL, Insulin=10 µUI/mL
        Expected HOMA-IR = (100 × 10) / 405 = 2.47
        """
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Test Lab",
            fasting_glucose_mgdl=100.0,
            fasting_insulin_uUI_ml=10.0
        )

        # Act
        lab_data.calculate_derived_values()

        # Assert
        expected_homa_ir = (100.0 * 10.0) / 405
        assert lab_data.homa_ir is not None
        assert abs(lab_data.homa_ir - expected_homa_ir) < 0.01
        assert abs(lab_data.homa_ir - 2.47) < 0.01

    def test_diabetes_detection_by_hba1c(self):
        """
        UT-LAB-004: Detección diabetes por HbA1c

        Test that HbA1c values >= 6.5% correctly trigger diabetes diagnosis
        and generate appropriate critical alerts.

        According to ADA guidelines:
        - Normal: < 5.7%
        - Prediabetes: 5.7% - 6.4%
        - Diabetes: >= 6.5%
        """
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Test Lab",
            hemoglobin_a1c_pct=6.8  # Diabetes range
        )

        # Act
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        # Check that HbA1c is flagged as out of range
        hba1c_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if "hemoglobina" in alert["parameter"].lower()
        ]

        assert len(hba1c_alerts) > 0
        hba1c_alert = hba1c_alerts[0]

        assert hba1c_alert["value"] == 6.8
        assert hba1c_alert["severity"] == Severity.SEVERE.value
        assert "diabetes" in hba1c_alert["clinical_meaning"].lower()

        # Check critical alerts
        critical_alerts = interpretation["critical_alerts"]
        assert len(critical_alerts) > 0

        # Verify at least one alert mentions HbA1c
        hba1c_critical = any(
            "hba1c" in alert.lower() or "hemoglobina" in alert.lower()
            for alert in critical_alerts
        )
        assert hba1c_critical

    def test_high_atherogenic_index_detection(self):
        """
        UT-LAB-005: Índice aterogénico alto

        Test that high atherogenic index (Total Cholesterol / HDL > 5.0)
        is correctly calculated and generates cardiovascular risk alert.

        Atherogenic Index interpretation:
        - Optimal: < 3.0
        - Low risk: 3.0 - 4.0
        - Moderate risk: 4.0 - 5.0
        - High risk: > 5.0

        Example: TC=250 mg/dL, HDL=30 mg/dL
        Atherogenic Index = 250/30 = 8.33 (Very High Risk)
        """
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.LIPID_PROFILE,
            laboratory_name="Test Lab",
            total_cholesterol_mgdl=250.0,
            hdl_cholesterol_mgdl=30.0
        )

        # Act
        lab_data.calculate_derived_values()
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        # Check atherogenic index calculation
        expected_index = 250.0 / 30.0
        assert lab_data.atherogenic_index is not None
        assert abs(lab_data.atherogenic_index - expected_index) < 0.01
        assert lab_data.atherogenic_index > 8.0  # Very high

        # Check that both cholesterol and HDL are flagged
        cholesterol_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if "colesterol" in alert["parameter"].lower()
        ]

        assert len(cholesterol_alerts) > 0

        # Verify cardiovascular risk is mentioned
        diet_adjustments = interpretation.get("diet_adjustments", [])
        has_lipid_recommendations = any(
            "grasa" in adj.lower() or "omega" in adj.lower()
            for adj in diet_adjustments
        )
        assert has_lipid_recommendations


@pytest.mark.unit
class TestLaboratoryDataDerivedCalculations:
    """Additional tests for derived calculations and edge cases"""

    def test_homa_ir_not_calculated_without_insulin(self):
        """Test that HOMA-IR is not calculated if insulin is missing"""
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Test Lab",
            fasting_glucose_mgdl=100.0
            # No insulin value
        )

        # Act
        lab_data.calculate_derived_values()

        # Assert
        assert lab_data.homa_ir is None

    def test_atherogenic_index_handles_zero_hdl(self):
        """Test that atherogenic index handles zero HDL gracefully"""
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.LIPID_PROFILE,
            laboratory_name="Test Lab",
            total_cholesterol_mgdl=200.0,
            hdl_cholesterol_mgdl=0.0  # Edge case
        )

        # Act
        lab_data.calculate_derived_values()

        # Assert
        # Should not crash, atherogenic index should remain None or not divide by zero
        # Based on the code, it checks hdl > 0
        assert lab_data.atherogenic_index is None

    def test_prediabetes_detection(self):
        """Test detection of prediabetes (glucose 100-125 mg/dL)"""
        # Arrange
        lab_data = LaboratoryData(
            patient_id=1,
            study_date=date(2025, 1, 15),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Test Lab",
            fasting_glucose_mgdl=110.0  # Prediabetes range
        )

        # Act
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        glucose_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if "glucosa" in alert["parameter"].lower()
        ]

        assert len(glucose_alerts) > 0
        assert glucose_alerts[0]["severity"] == Severity.MILD.value

        # Check for prediabetes diagnosis
        diagnoses = interpretation["suggested_diagnoses"]
        has_prediabetes = any("prediabetes" in diag.lower() for diag in diagnoses)
        assert has_prediabetes

    def test_multiple_out_of_range_values(self, sample_lab_data_high_values):
        """Test that multiple out-of-range values are all detected"""
        # Arrange
        lab_data = LaboratoryData(**sample_lab_data_high_values)

        # Act
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        # Should detect multiple issues
        assert len(interpretation["out_of_range_values"]) >= 4

        # Check for various parameters
        parameter_names = [
            alert["parameter"].lower()
            for alert in interpretation["out_of_range_values"]
        ]

        # Should include glucose, cholesterol, triglycerides, creatinine
        assert any("glucosa" in name for name in parameter_names)
        assert any("colesterol" in name or "hdl" in name for name in parameter_names)
        assert any("triglicéridos" in name for name in parameter_names)
        assert any("creatinina" in name for name in parameter_names)

    def test_normal_values_generate_no_alerts(self, sample_lab_data_dict):
        """Test that normal laboratory values generate no critical alerts"""
        # Arrange
        lab_data = LaboratoryData(**sample_lab_data_dict)

        # Act
        interpretation = lab_data.generate_ai_interpretation()

        # Assert
        # Normal values should have minimal or no out-of-range alerts
        # All values in sample_lab_data_dict are within normal range
        assert len(interpretation["critical_alerts"]) == 0

        # There might be mild alerts, but no severe ones
        severe_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if alert["severity"] == Severity.SEVERE.value
        ]
        assert len(severe_alerts) == 0

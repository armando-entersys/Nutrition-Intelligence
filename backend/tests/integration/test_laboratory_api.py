"""
Integration Tests for Laboratory API Endpoints
Tests cover the integration test cases defined in TESTING_PLAN.md

Test IDs covered:
- IT-LAB-001: Create complete laboratory record
- IT-LAB-002: Get laboratory records for patient with pagination
- IT-LAB-003: Update laboratory values
- IT-LAB-004: Get laboratory trends analysis
- IT-LAB-005: Delete laboratory record
"""
import pytest
from httpx import AsyncClient
from datetime import date, datetime, timedelta
from sqlmodel import Session, select

from domain.patients.laboratory import LaboratoryData, LabTrend, LabTestType
from domain.patients.models import Patient


@pytest.mark.integration
@pytest.mark.asyncio
class TestLaboratoryAPI:
    """Integration tests for Laboratory API endpoints"""

    async def test_create_laboratory_data_complete(
        self,
        client: AsyncClient,
        sample_patient: Patient,
        sample_lab_data_dict: dict
    ):
        """
        IT-LAB-001: Crear laboratorio completo

        Test POST /api/v1/laboratory/
        - Status 201
        - Data saved to database
        - AI interpretation generated
        - Derived values calculated (HOMA-IR, atherogenic index)
        """
        # Arrange
        lab_data_payload = {
            **sample_lab_data_dict,
            "study_date": "2025-01-15",
            "fasting_insulin_uUI_ml": 10.0  # Add insulin for HOMA-IR calculation
        }

        # Act
        response = await client.post(
            "/api/v1/laboratory/",
            json=lab_data_payload
        )

        # Assert
        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["patient_id"] == sample_patient.id
        assert data["study_date"] == "2025-01-15"
        assert data["laboratory_name"] == "Laboratorio Chopo"

        # Verify derived values were calculated
        assert data["homa_ir"] is not None
        expected_homa_ir = (95.0 * 10.0) / 405
        assert abs(data["homa_ir"] - expected_homa_ir) < 0.01

        assert data["atherogenic_index"] is not None
        expected_atherogenic = 180.0 / 55.0
        assert abs(data["atherogenic_index"] - expected_atherogenic) < 0.01

        # Verify AI interpretation was generated
        assert data["ai_interpretation"] is not None
        interpretation = data["ai_interpretation"]
        assert "out_of_range_values" in interpretation
        assert "suggested_diagnoses" in interpretation
        assert "diet_adjustments" in interpretation
        assert "critical_alerts" in interpretation

        # Verify timestamps
        assert data["created_at"] is not None

    async def test_get_patient_laboratory_data_with_pagination(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient
    ):
        """
        IT-LAB-002: Obtener labs de paciente

        Test GET /api/v1/laboratory/patient/{patient_id}
        - Returns list with pagination
        - Supports filtering by test_type and date range
        - Ordered by date (newest first)
        """
        # Arrange - Create multiple lab records
        lab_records = []
        for i in range(5):
            lab_data = LaboratoryData(
                patient_id=sample_patient.id,
                study_date=date(2025, 1, 10 + i),
                test_type=LabTestType.BLOOD_CHEMISTRY if i % 2 == 0 else LabTestType.LIPID_PROFILE,
                laboratory_name=f"Lab Test {i}",
                fasting_glucose_mgdl=90.0 + i * 5
            )
            test_session.add(lab_data)
            lab_records.append(lab_data)

        await test_session.commit()

        # Act - Get all records
        response = await client.get(
            f"/api/v1/laboratory/patient/{sample_patient.id}",
            params={"skip": 0, "limit": 10}
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["items"]) == 5

        # Verify ordering (newest first)
        dates = [item["study_date"] for item in data["items"]]
        assert dates == sorted(dates, reverse=True)

        # Act - Test pagination
        response_page2 = await client.get(
            f"/api/v1/laboratory/patient/{sample_patient.id}",
            params={"skip": 3, "limit": 2}
        )

        # Assert pagination
        assert response_page2.status_code == 200
        page2_data = response_page2.json()
        assert len(page2_data["items"]) == 2
        assert page2_data["total"] == 5

        # Act - Test filtering by test type
        response_filtered = await client.get(
            f"/api/v1/laboratory/patient/{sample_patient.id}",
            params={"test_type": "blood_chemistry"}
        )

        # Assert filtering
        assert response_filtered.status_code == 200
        filtered_data = response_filtered.json()
        assert filtered_data["total"] == 3  # 3 blood_chemistry records
        for item in filtered_data["items"]:
            assert item["test_type"] == "blood_chemistry"

    async def test_update_laboratory_values(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient,
        sample_lab_data_dict: dict
    ):
        """
        IT-LAB-003: Actualizar valores lab

        Test PUT /api/v1/laboratory/{id}
        - Status 200
        - Data updated in database
        - AI interpretation recalculated
        - Updated timestamp set
        """
        # Arrange - Create initial lab record
        lab_data = LaboratoryData(**sample_lab_data_dict)
        test_session.add(lab_data)
        await test_session.commit()
        await test_session.refresh(lab_data)

        initial_glucose = lab_data.fasting_glucose_mgdl

        # Act - Update glucose value
        update_payload = {
            "fasting_glucose_mgdl": 150.0,  # Elevated glucose
            "hemoglobin_a1c_pct": 6.2  # Prediabetes range
        }

        response = await client.put(
            f"/api/v1/laboratory/{lab_data.id}",
            json=update_payload
        )

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == lab_data.id
        assert data["fasting_glucose_mgdl"] == 150.0
        assert data["hemoglobin_a1c_pct"] == 6.2

        # Verify update timestamp was set
        assert data["updated_at"] is not None

        # Verify AI interpretation was regenerated
        interpretation = data["ai_interpretation"]
        assert interpretation is not None

        # Should now have alerts for elevated glucose
        glucose_alerts = [
            alert for alert in interpretation["out_of_range_values"]
            if "glucosa" in alert["parameter"].lower()
        ]
        assert len(glucose_alerts) > 0
        assert glucose_alerts[0]["value"] == 150.0

    async def test_get_laboratory_trends_analysis(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient
    ):
        """
        IT-LAB-004: Análisis de tendencias

        Test GET /api/v1/laboratory/trends/patient/{patient_id}
        - Returns trend comparison with previous labs
        - Shows direction (improving/worsening/stable)
        - Includes percent change
        - Provides interpretation
        """
        # Arrange - Create sequential lab records
        lab_data_1 = LaboratoryData(
            patient_id=sample_patient.id,
            study_date=date(2025, 1, 1),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Lab 1",
            fasting_glucose_mgdl=110.0,  # Elevated
            total_cholesterol_mgdl=220.0,  # High
            hdl_cholesterol_mgdl=45.0
        )
        test_session.add(lab_data_1)
        await test_session.commit()

        lab_data_2 = LaboratoryData(
            patient_id=sample_patient.id,
            study_date=date(2025, 2, 1),
            test_type=LabTestType.BLOOD_CHEMISTRY,
            laboratory_name="Lab 2",
            fasting_glucose_mgdl=95.0,  # Improved
            total_cholesterol_mgdl=190.0,  # Improved
            hdl_cholesterol_mgdl=50.0  # Improved
        )
        test_session.add(lab_data_2)
        await test_session.commit()

        # Act
        response = await client.get(
            f"/api/v1/laboratory/trends/patient/{sample_patient.id}",
            params={"months_back": 6}
        )

        # Assert
        assert response.status_code == 200

        trends = response.json()
        assert isinstance(trends, list)
        assert len(trends) > 0

        # Find glucose trend
        glucose_trend = next(
            (t for t in trends if "glucosa" in t["parameter_name"].lower()),
            None
        )

        assert glucose_trend is not None
        assert len(glucose_trend["values"]) == 2

        # Verify trend direction (glucose went down - should be improving)
        assert glucose_trend["trend"] == "improving"
        assert glucose_trend["normal_range"] is not None
        assert glucose_trend["interpretation"] is not None

        # Verify values are in chronological order
        first_value = glucose_trend["values"][0]["value"]
        last_value = glucose_trend["values"][1]["value"]
        assert first_value == 110.0
        assert last_value == 95.0

    async def test_delete_laboratory_record(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient,
        sample_lab_data_dict: dict
    ):
        """
        IT-LAB-005: Eliminar laboratorio

        Test DELETE /api/v1/laboratory/{id}
        - Status 204
        - Record deleted from database
        - Associated trends also deleted (cascade)
        """
        # Arrange - Create lab record
        lab_data = LaboratoryData(**sample_lab_data_dict)
        test_session.add(lab_data)
        await test_session.commit()
        await test_session.refresh(lab_data)

        lab_id = lab_data.id

        # Create associated trend (if any)
        trend = LabTrend(
            lab_data_id=lab_id,
            patient_id=sample_patient.id,
            parameter_name="Glucosa en ayunas",
            current_value=95.0,
            previous_value=110.0,
            direction="improving",
            percent_change=-13.64
        )
        test_session.add(trend)
        await test_session.commit()

        # Act - Delete lab record
        response = await client.delete(f"/api/v1/laboratory/{lab_id}")

        # Assert
        assert response.status_code == 204

        # Verify record was deleted from database
        deleted_lab = await test_session.get(LaboratoryData, lab_id)
        assert deleted_lab is None

        # Verify associated trends were also deleted
        trend_query = select(LabTrend).where(LabTrend.lab_data_id == lab_id)
        result = await test_session.execute(trend_query)
        remaining_trends = result.scalars().all()
        assert len(remaining_trends) == 0


@pytest.mark.integration
@pytest.mark.asyncio
class TestLaboratoryAPIEdgeCases:
    """Additional integration tests for edge cases and error handling"""

    async def test_get_laboratory_for_nonexistent_patient(
        self,
        client: AsyncClient
    ):
        """Test that requesting labs for non-existent patient returns 404"""
        # Act
        response = await client.get("/api/v1/laboratory/patient/99999")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_update_nonexistent_laboratory(
        self,
        client: AsyncClient
    ):
        """Test that updating non-existent lab record returns 404"""
        # Act
        response = await client.put(
            "/api/v1/laboratory/99999",
            json={"fasting_glucose_mgdl": 100.0}
        )

        # Assert
        assert response.status_code == 404

    async def test_delete_nonexistent_laboratory(
        self,
        client: AsyncClient
    ):
        """Test that deleting non-existent lab record returns 404"""
        # Act
        response = await client.delete("/api/v1/laboratory/99999")

        # Assert
        assert response.status_code == 404

    async def test_create_laboratory_with_invalid_patient_id(
        self,
        client: AsyncClient,
        sample_lab_data_dict: dict
    ):
        """Test that creating lab with invalid patient_id returns 404"""
        # Arrange
        invalid_payload = {
            **sample_lab_data_dict,
            "patient_id": 99999,
            "study_date": "2025-01-15"
        }

        # Act
        response = await client.post(
            "/api/v1/laboratory/",
            json=invalid_payload
        )

        # Assert
        assert response.status_code == 404
        assert "patient" in response.json()["detail"].lower()

    async def test_get_laboratory_by_id(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient,
        sample_lab_data_dict: dict
    ):
        """Test GET /api/v1/laboratory/{lab_id}"""
        # Arrange
        lab_data = LaboratoryData(**sample_lab_data_dict)
        test_session.add(lab_data)
        await test_session.commit()
        await test_session.refresh(lab_data)

        # Act
        response = await client.get(f"/api/v1/laboratory/{lab_data.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == lab_data.id
        assert data["patient_id"] == sample_patient.id

    async def test_reanalyze_laboratory_data(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient,
        sample_lab_data_dict: dict
    ):
        """Test POST /api/v1/laboratory/{lab_id}/reanalyze"""
        # Arrange
        lab_data = LaboratoryData(**sample_lab_data_dict)
        test_session.add(lab_data)
        await test_session.commit()
        await test_session.refresh(lab_data)

        # Act
        response = await client.post(f"/api/v1/laboratory/{lab_data.id}/reanalyze")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["ai_interpretation"] is not None
        assert data["updated_at"] is not None

    async def test_laboratory_date_range_filtering(
        self,
        client: AsyncClient,
        test_session: Session,
        sample_patient: Patient
    ):
        """Test date range filtering for laboratory data"""
        # Arrange - Create records with different dates
        for i in range(5):
            lab_data = LaboratoryData(
                patient_id=sample_patient.id,
                study_date=date(2025, 1, 1) + timedelta(days=i * 30),
                test_type=LabTestType.BLOOD_CHEMISTRY,
                laboratory_name=f"Lab {i}",
                fasting_glucose_mgdl=90.0 + i
            )
            test_session.add(lab_data)
        await test_session.commit()

        # Act - Filter by date range
        response = await client.get(
            f"/api/v1/laboratory/patient/{sample_patient.id}",
            params={
                "date_from": "2025-01-15",
                "date_to": "2025-03-15"
            }
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] <= 3  # Should be filtered

        # Verify all returned items are within date range
        for item in data["items"]:
            study_date = datetime.strptime(item["study_date"], "%Y-%m-%d").date()
            assert date(2025, 1, 15) <= study_date <= date(2025, 3, 15)

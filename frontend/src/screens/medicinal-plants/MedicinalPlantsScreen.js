import React, { useState } from 'react';
import MedicinalPlantsExplorer from '../../components/medicinal-plants/MedicinalPlantsExplorer';
import PlantDetail from '../../components/medicinal-plants/PlantDetail';

/**
 * MedicinalPlantsScreen
 * Main screen for the Mexican Medicinal Plants module
 * Integrates the plant explorer and detail view
 */
const MedicinalPlantsScreen = () => {
  const [selectedPlantId, setSelectedPlantId] = useState(null);

  const handlePlantClick = (plant) => {
    setSelectedPlantId(plant.id);
  };

  const handleClosePlantDetail = () => {
    setSelectedPlantId(null);
  };

  return (
    <div>
      <MedicinalPlantsExplorer onPlantClick={handlePlantClick} />

      {selectedPlantId && (
        <PlantDetail
          plantId={selectedPlantId}
          onClose={handleClosePlantDetail}
        />
      )}
    </div>
  );
};

export default MedicinalPlantsScreen;

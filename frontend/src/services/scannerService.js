import { API_BASE_URL } from '../config/api';

/**
 * Scanner Service - Servicio para Escáner NOM-051
 *
 * Interactúa con el backend para escanear productos y obtener
 * información sobre sellos de advertencia NOM-051
 */

/**
 * Escanear producto por código de barras
 * @param {string} barcode - Código de barras del producto
 * @param {string} token - Token de autenticación del usuario
 * @returns {Promise<Object>} Información del producto con sellos NOM-051
 */
export const scanBarcode = async (barcode, token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/scanner/barcode/${barcode}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Producto no encontrado en la base de datos');
      }
      throw new Error(`Error al escanear producto: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en scanBarcode:', error);
    throw error;
  }
};

/**
 * Obtener historial de escaneos del usuario
 * @param {string} token - Token de autenticación del usuario
 * @param {number} limit - Número de resultados a devolver (default: 20)
 * @returns {Promise<Array>} Lista de escaneos realizados
 */
export const getScanHistory = async (token, limit = 20) => {
  try {
    const response = await fetch(`${API_BASE_URL}/scanner/history?limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Error al obtener historial: ${response.statusText}`);
    }

    const data = await response.json();
    return data.history || [];
  } catch (error) {
    console.error('Error en getScanHistory:', error);
    throw error;
  }
};

/**
 * Obtener estadísticas de escaneos del usuario
 * @param {string} token - Token de autenticación del usuario
 * @returns {Promise<Object>} Estadísticas de escaneos
 */
export const getScanStats = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/scanner/stats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Error al obtener estadísticas: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en getScanStats:', error);
    throw error;
  }
};

/**
 * Verificar estado del servicio de scanner
 * @param {string} token - Token de autenticación del usuario
 * @returns {Promise<Object>} Estado del servicio
 */
export const getServiceHealth = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/scanner/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Error al verificar servicio: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en getServiceHealth:', error);
    throw error;
  }
};

/**
 * Escanear etiqueta de producto mediante foto
 * @param {File} imageFile - Archivo de imagen de la etiqueta
 * @param {string} token - Token de autenticación del usuario
 * @returns {Promise<Object>} Información del producto con sellos NOM-051
 */
export const scanLabel = async (imageFile, token) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${API_BASE_URL}/scanner/label`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      if (response.status === 422) {
        throw new Error('No se pudo leer la información nutricional de la imagen. Asegúrate de que la foto muestre claramente la tabla nutricional.');
      }
      if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Formato de archivo inválido');
      }
      throw new Error(`Error al escanear etiqueta: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en scanLabel:', error);
    throw error;
  }
};

/**
 * Convertir datos de la API al formato del componente
 * @param {Object} apiData - Datos del producto desde la API
 * @returns {Object} Datos formateados para el componente
 */
export const formatProductData = (apiData) => {
  return {
    id: apiData.codigo_barras,
    nombre: apiData.nombre,
    marca: apiData.marca || 'Marca no disponible',
    codigo_barras: apiData.codigo_barras,
    informacion_nutricional: {
      porcion: `${apiData.porcion_gramos || 100}g`,
      calorias: apiData.calorias || 0,
      azucares_g: apiData.azucares || 0,
      grasas_saturadas_g: apiData.grasas_saturadas || 0,
      grasas_trans_g: apiData.grasas_trans || 0,
      sodio_mg: apiData.sodio || 0,
      proteinas_g: apiData.proteinas || 0,
      carbohidratos_g: apiData.carbohidratos || 0,
      fibra_g: apiData.fibra || 0,
    },
    sellos_advertencia: [
      { tipo: 'exceso_calorias', activo: apiData.exceso_calorias || false },
      { tipo: 'exceso_azucares', activo: apiData.exceso_azucares || false },
      { tipo: 'exceso_grasas_saturadas', activo: apiData.exceso_grasas_saturadas || false },
      { tipo: 'exceso_grasas_trans', activo: apiData.exceso_grasas_trans || false },
      { tipo: 'exceso_sodio', activo: apiData.exceso_sodio || false },
    ],
    tiene_edulcorantes: apiData.contiene_edulcorantes || false,
    tiene_cafeina: apiData.contiene_cafeina || false,
    fuente: apiData.fuente || 'unknown',
    health_score: apiData.health_score || 50,
    health_level: apiData.health_level || 'Regular',
    health_color: apiData.health_color || '#FFC107',
    ingredientes: apiData.ingredientes || '',
    imagen_url: apiData.imagen_url || null,
    // Nuevos campos para el sistema global de productos
    is_duplicate: apiData.is_duplicate || false,
    scan_count: apiData.scan_count || 1,
    verified: apiData.verified || false,
    verified_by_user_id: apiData.verified_by_user_id || null,
    is_global: apiData.is_global !== undefined ? apiData.is_global : true,
    confidence_score: apiData.confidence_score || null,
    created_by_user_id: apiData.created_by_user_id || null,
  };
};

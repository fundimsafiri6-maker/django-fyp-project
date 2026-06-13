"""
Model Loader Utility for 3-Class Ensemble Complaint Classifier

This module loads trained ML models from the external model/ folder
and provides a clean interface for Django to use them.

Models are stored in: C:\Users\AUDITORIUM\Desktop\Shle\Semester 3.2\fyp system 50%\model\models\
"""

import os
import pickle
import logging
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class ModelLoader:
    """Load and manage trained complaint classification models."""
    
    # Path to external model directory
    MODEL_BASE_PATH = Path(r"C:\Users\AUDITORIUM\Pictures\model\models")
    
    # Model file names
    ENSEMBLE_CLASSIFIER = "ensemble_classifier.pkl"
    PRIORITY_CLASSIFIER = "priority_classifier.pkl"
    TFIDF_VECTORIZER = "tfidf_vectorizer.pkl"
    ENCODER_CATEGORY = "label_encoder_category.pkl"
    ENCODER_PRIORITY = "label_encoder_priority.pkl"
    
    _ensemble_model = None
    _priority_model = None
    _vectorizer = None
    _encoder_category = None
    _encoder_priority = None
    
    @classmethod
    def _load_model(cls, filename: str) -> Optional[object]:
        """
        Load a pickle model file.
        
        Args:
            filename: Name of the model file
            
        Returns:
            Loaded model object or None if loading fails
        """
        try:
            model_path = cls.MODEL_BASE_PATH / filename
            
            if not model_path.exists():
                logger.warning(f"Model file not found: {model_path}")
                return None
            
            with open(str(model_path), 'rb') as f:
                model = pickle.load(f)
            
            logger.info(f"✓ Loaded model: {filename}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading model {filename}: {str(e)}")
            return None
    
    @classmethod
    def load_all_models(cls) -> bool:
        """
        Load all required models for complaint classification.
        
        Returns:
            True if all models loaded successfully, False otherwise
        """
        try:
            cls._ensemble_model = cls._load_model(cls.ENSEMBLE_CLASSIFIER)
            cls._priority_model = cls._load_model(cls.PRIORITY_CLASSIFIER)
            cls._vectorizer = cls._load_model(cls.TFIDF_VECTORIZER)
            cls._encoder_category = cls._load_model(cls.ENCODER_CATEGORY)
            cls._encoder_priority = cls._load_model(cls.ENCODER_PRIORITY)
            
            # Check if all models loaded successfully
            if all([cls._ensemble_model, cls._priority_model, cls._vectorizer, 
                   cls._encoder_category, cls._encoder_priority]):
                logger.info("✓ All models loaded successfully")
                return True
            else:
                logger.error("Some models failed to load")
                return False
                
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False
    
    @classmethod
    def get_ensemble_classifier(cls):
        """Get the ensemble category classifier model."""
        if cls._ensemble_model is None:
            cls.load_all_models()
        return cls._ensemble_model
    
    @classmethod
    def get_priority_classifier(cls):
        """Get the priority classifier model."""
        if cls._priority_model is None:
            cls.load_all_models()
        return cls._priority_model
    
    @classmethod
    def get_vectorizer(cls):
        """Get the TF-IDF vectorizer."""
        if cls._vectorizer is None:
            cls.load_all_models()
        return cls._vectorizer
    
    @classmethod
    def get_category_encoder(cls):
        """Get the category label encoder."""
        if cls._encoder_category is None:
            cls.load_all_models()
        return cls._encoder_category
    
    @classmethod
    def get_priority_encoder(cls):
        """Get the priority label encoder."""
        if cls._encoder_priority is None:
            cls.load_all_models()
        return cls._encoder_priority
    
    @classmethod
    def predict(cls, text: str) -> Tuple[str, str, float]:
        """
        Predict department and priority for a given complaint text.
        
        Args:
            text: Complaint text
            
        Returns:
            Tuple of (department, priority, confidence_score)
            Example: ('ICT', 'high', 92.5)
        """
        try:
            # Ensure models are loaded
            if not all([cls._ensemble_model, cls._vectorizer, cls._encoder_category, cls._encoder_priority]):
                if not cls.load_all_models():
                    return ('OTHER', 'Medium', 0.0)
            
            # Vectorize text
            vec = cls._vectorizer.transform([text])
            
            # Predict category
            cat_pred_encoded = cls._ensemble_model.predict(vec)[0]
            cat_proba = cls._ensemble_model.predict_proba(vec)
            confidence = float(max(cat_proba[0]) * 100)  # Convert to percentage
            
            # Predict priority
            pri_pred_encoded = cls._priority_model.predict(vec)[0]
            
            # Decode predictions
            category = cls._encoder_category.inverse_transform([cat_pred_encoded])[0]
            priority = cls._encoder_priority.inverse_transform([pri_pred_encoded])[0]
            
            # Capitalize for consistency with Django
            category = category.lower()  # 'ict' or 'academic'
            priority = priority.capitalize()  # 'Low', 'Medium', 'High'
            
            return (category, priority, confidence)
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return ('other', 'Medium', 0.0)
    
    @classmethod
    def health_check(cls) -> dict:
        """
        Check if all models are loaded and ready.
        
        Returns:
            Dict with status information
        """
        return {
            'ensemble_loaded': cls._ensemble_model is not None,
            'priority_loaded': cls._priority_model is not None,
            'vectorizer_loaded': cls._vectorizer is not None,
            'encoder_category_loaded': cls._encoder_category is not None,
            'encoder_priority_loaded': cls._encoder_priority is not None,
            'model_path': str(cls.MODEL_BASE_PATH),
            'all_ready': all([cls._ensemble_model, cls._priority_model, cls._vectorizer,
                            cls._encoder_category, cls._encoder_priority])
        }


# Initialize models on module import
try:
    ModelLoader.load_all_models()
except Exception as e:
    logger.warning(f"Warning: Could not load models on startup: {str(e)}")

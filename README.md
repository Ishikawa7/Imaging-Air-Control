# Imaging-Based Air Quality Control System

## Overview

This project implements a prototype simulation of an **Imaging-based Air Quality Control System** that combines computer vision, predictive modeling, and real-time optimization to monitor and control indoor air quality. The system uses webcam-based object detection to count people in a room, predicts CO₂ levels, and automatically optimizes ventilation pump power to maintain air quality below safety thresholds.

## Project Architecture

The system consists of several interconnected components:

### 1. **Real-time Imaging System** (`imaging.py`)
- **YOLO v5 Object Detection**: Uses a pre-trained YOLOv5 model to detect objects in real-time from webcam feed
- **Person Counting**: Automatically counts the number of people in the monitored space
- **Frame Processing**: Processes video frames every 80 iterations to balance performance and accuracy
- **Supported Objects**: Detects 80 different object classes (COCO dataset classes)

### 2. **Air Quality Simulation** (`simulator.py`)
- **CO₂ Level Prediction**: Simulates and predicts CO₂ concentrations based on:
  - Room volume (m³)
  - Number of people detected
  - Ambient air pump capacity (L/min)
  - Current pump power percentage
  - Number of active pumps
- **Thread-safe Operations**: Uses queue-based communication for real-time updates
- **Predictive Capabilities**: Forecasts CO₂ levels for the next 10 time steps

### 3. **Predictive Modeling** (`predictor.py`, `predictive_model.ipynb`)
- **Linear Regression Model**: Trained to predict future CO₂ concentrations
- **Multi-step Prediction**: Capable of predicting multiple time steps ahead
- **Model Persistence**: Saves trained models using pickle for deployment

### 4. **Optimization Engine** (`optimizer.py`)
- **Intelligent Pump Control**: Automatically adjusts ventilation pump power
- **MPC Implementation**: Uses Model Predictive Control techniques for optimal control
- **Threshold-based Optimization**: Maintains CO₂ levels below configurable safety thresholds
- **Recursive Search Algorithm**: Finds optimal pump power settings by minimizing threshold violations
- **Energy Efficiency**: Balances air quality with energy consumption

### 5. **Anomaly Detection System**
#### Image-based Anomaly Detection (`anomalies_img.py`, `anomalies_detected.ipynb`)
- **Isolation Forest Model**: Detects unusual patterns in object detection results
- **Real-time Scoring**: Provides anomaly scores for detected objects
- **Visual Anomaly Detection**: Identifies unusual visual patterns that might indicate problems

#### Variables-based Anomaly Detection (`anomalies_var.py`, `anomalies_variables.ipynb`)
- **System Parameter Monitoring**: Detects anomalies in system variables (CO₂, pump power, etc.)
- **Isolation Forest Implementation**: Uses unsupervised learning to identify unusual system states
- **Real-time Alerts**: Provides immediate feedback on system anomalies

### 6. **Web-based Dashboard** (`app_test.py`)
- **Real-time Visualization**: Built with Dash and Plotly for interactive monitoring
- **Live Video Feed**: Displays real-time webcam feed with object detection overlays
- **Interactive Controls**: Allows users to adjust system parameters:
  - Room volume
  - Pump capacity
  - Number of pumps
  - CO₂ threshold levels
- **Multi-panel Display**:
  - Live video with object detection
  - CO₂ concentration trends and predictions
  - Anomaly detection scores (both imaging and variables)
  - System status indicators

### 7. **Desktop Application** (`run.py`)
- **Standalone App**: Uses PyWebView to create a desktop application
- **Compact Interface**: Optimized for on-top monitoring (225x710 pixels)
- **Flask Backend**: Runs the web interface in a desktop window

## Key Features

### 🎯 **Real-time Monitoring**
- Live webcam feed with object detection
- Continuous CO₂ level prediction
- Real-time anomaly detection
- System status monitoring

### 🧠 **Intelligent Control**
- Automatic pump power optimization
- Predictive control based on occupancy (MPC - Model Predictive Control)
- Threshold-based safety management
- Energy-efficient operation

### 📊 **Advanced Analytics**
- Dual anomaly detection (visual + variables)
- Predictive modeling with 10-step forecasting
- Historical trend analysis
- Interactive data visualization

### 🔧 **Configurable Parameters**
- Room volume adjustment
- Pump capacity settings
- CO₂ threshold configuration
- Real-time parameter tuning

## Technical Implementation

### Machine Learning Models
1. **YOLOv5**: Object detection and person counting
2. **Linear Regression**: CO₂ prediction model
3. **Isolation Forest**: Anomaly detection (2 separate models)

### Data Processing
- **Training Data**: 120,000+ synthetic data points for CO₂ prediction
- **Object Detection Data**: 1,900+ frames with detected objects
- **Real-time Processing**: Optimized for live video streaming

### Technology Stack
- **Computer Vision**: OpenCV, YOLOv5, PyTorch
- **Machine Learning**: scikit-learn, TensorFlow, PyOD
- **Web Interface**: Dash, Plotly, Flask
- **Desktop App**: PyWebView
- **Data Processing**: pandas, NumPy

## Testing and Validation

### YOLO Model Testing
- **YOLOv5 vs YOLOv8**: Comparative analysis in `test_YOLO5.ipynb` and `test_YOLO8.ipynb`
- **Performance Optimization**: Model selection based on accuracy and speed
- **Object Detection Accuracy**: Validated on various indoor scenarios

### Data Generation
- **Synthetic Data**: Created comprehensive datasets for training (`data_creation_variables.ipynb`)
- **Realistic Scenarios**: Simulated various room conditions and occupancy patterns
- **Model Validation**: Cross-validation and performance metrics analysis

## Installation and Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Key Dependencies
- OpenCV for computer vision
- YOLOv5/Ultralytics for object detection
- Dash/Plotly for web interface
- scikit-learn for machine learning
- PyWebView for desktop application

### Running the Application
```bash
# Web interface
python app_test.py

# Desktop application
python run.py
```

## Use Cases and Applications

### 🏢 **Smart Buildings**
- Automatic ventilation control in offices
- Energy-efficient air quality management
- Occupancy-based HVAC optimization

### 🏫 **Educational Facilities**
- Classroom air quality monitoring
- Student safety and comfort
- Automated ventilation in lecture halls

### 🏭 **Industrial Applications**
- Worker safety monitoring
- Air quality control in manufacturing
- Compliance with safety regulations

### 🏥 **Healthcare Facilities**
- Patient room air quality
- Infection control through proper ventilation
- Staff and patient safety

## Future Enhancements

- **Multi-room Monitoring**: Extend to multiple spaces
- **Advanced Sensors**: Integration with IoT air quality sensors
- **Machine Learning Improvements**: Deep learning for better predictions
- **Mobile App**: Remote monitoring capabilities
- **Cloud Integration**: Data storage and analytics in the cloud

## Project Significance

This prototype demonstrates the potential of combining computer vision with predictive modeling for intelligent building management. By using readily available hardware (webcam) and advanced software techniques, the system provides a cost-effective solution for air quality monitoring and control.

The project showcases:
- **Innovation**: Novel use of computer vision for air quality control
- **Practicality**: Real-world applicability with minimal hardware requirements
- **Scalability**: Architecture designed for easy expansion
- **Efficiency**: Balance between performance and energy consumption

## Conclusion

The Imaging-based Air Quality Control System represents a significant step forward in intelligent building management, combining multiple AI technologies to create a comprehensive solution for indoor air quality monitoring and control. The system's ability to predict, detect anomalies, and automatically optimize ventilation makes it valuable for various applications where air quality is critical for health, comfort, and safety.
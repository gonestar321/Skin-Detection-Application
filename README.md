
# Skin Disease Classification Using Transfer Learning

## Overview
AI-powered skin disease classification using EfficientNetV2S deep learning model. This project includes a modern fullstack web application for easy image analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+

### 1. Setup Backend
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask flask-cors tensorflow pillow numpy

# Start server
cd backend
python app.py
```
Server runs on **http://localhost:5001**

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
Opens on **http://localhost:5173**

### 3. Open in Browser
Navigate to **http://localhost:5173** and start analyzing skin conditions!

---

## 📁 Project Structure

```
Skin-Disease-Classification/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Place trained model here
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   └── index.css      # Premium styling
│   ├── index.html
│   └── package.json
├── resnet4 (5).ipynb       # Model training notebook
└── README.md
```

---

## 🔬 Model Training

The model is trained on the **DermNet dataset** with 23 skin disease classes:

1. Acne and Rosacea
2. Actinic Keratosis & Skin Cancer
3. Atopic Dermatitis
4. Bullous Disease
5. Cellulitis & Bacterial Infections
6. Eczema
7. Drug Eruptions
8. Hair Loss & Alopecia
9. Herpes & STDs
10. Pigmentation Disorders
11. Lupus & Connective Tissue
12. Melanoma & Moles
13. Nail Fungus
14. Contact Dermatitis
15. Psoriasis & Lichen Planus
16. Scabies & Infestations
17. Seborrheic Keratoses
18. Systemic Disease
19. Fungal Infections
20. Urticaria Hives
21. Vascular Tumors
22. Vasculitis
23. Warts & Viral Infections

### Training Your Own Model
1. Open `resnet4 (5).ipynb` in Google Colab
2. Upload your `kaggle.json` API key
3. Run all cells to train the model
4. Download `efficientnet_model.h5`
5. Place it in `backend/models/`

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Analyze skin image |
| `/api/classes` | GET | List disease classes |

### Example Request
```bash
curl -X POST -F "file=@skin_image.jpg" http://localhost:5001/api/predict
```

---

## ✨ Features

- **Modern UI** - Glassmorphism design with smooth animations
- **Drag & Drop** - Easy image upload
- **Instant Analysis** - AI predictions in seconds
- **Detailed Results** - Confidence scores + recommendations
- **23 Conditions** - Comprehensive disease coverage
- **Privacy First** - Images never stored

---

## ⚠️ Disclaimer

This tool is for **educational purposes only** and should not replace professional medical advice. Always consult a dermatologist for accurate diagnosis and treatment.

---

## License
GNU Affero General Public License v3.0

## Credits
- Dataset: [DermNet](https://www.kaggle.com/datasets/shubhamgoel27/dermnet)


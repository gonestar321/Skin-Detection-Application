from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import os
import tensorflow as tf

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

app = Flask(__name__)
CORS(app)

# ============================================================================
# COMPREHENSIVE SKIN DISEASE DATABASE
# ============================================================================
# The model recognizes 8 core diseases, but we provide information on many more
# The predictions will suggest related conditions when appropriate

# Core model classes (8 classes trained model can recognize)
MODEL_CLASSES = [
    "Cellulitis",
    "Impetigo", 
    "Athlete's Foot",
    "Nail Fungus",
    "Ringworm",
    "Cutaneous Larva Migrans",
    "Chickenpox",
    "Shingles"
]

# Extended disease database for comprehensive information
DISEASE_DATABASE = {
    # ========== CORE MODEL DISEASES (Can be detected) ==========
    "Cellulitis": {
        "category": "Bacterial Infections",
        "description": "A serious bacterial skin infection causing redness, swelling, warmth, and pain. Usually affects the lower legs but can occur anywhere. If untreated, it can spread to lymph nodes and bloodstream.",
        "symptoms": ["Red, swollen skin", "Pain and tenderness", "Warmth in affected area", "Fever and chills", "Skin dimpling"],
        "causes": ["Bacteria entering through cuts", "Strep or staph bacteria", "Insect bites", "Surgical wounds"],
        "recommendation": "⚠️ Seek medical attention promptly. Antibiotics are typically required. Keep the affected area elevated and apply cool compresses.",
        "severity": "moderate-high",
        "contagious": False,
        "detectable": True
    },
    "Impetigo": {
        "category": "Bacterial Infections",
        "description": "A highly contagious bacterial skin infection most common in children. Causes red sores that rupture, ooze, and form a characteristic honey-colored crust.",
        "symptoms": ["Red sores around nose/mouth", "Honey-colored crusts", "Itching", "Blisters", "Swollen lymph nodes"],
        "causes": ["Staphylococcus bacteria", "Streptococcus bacteria", "Contact with infected person", "Poor hygiene"],
        "recommendation": "Consult a doctor for antibiotic treatment (cream or oral). Keep sores clean and covered. Avoid touching and wash hands frequently.",
        "severity": "mild-moderate",
        "contagious": True,
        "detectable": True
    },
    "Athlete's Foot": {
        "category": "Fungal Infections",
        "description": "A contagious fungal infection (tinea pedis) that typically begins between the toes. Causes scaly, itchy, and sometimes painful rash. Common in people whose feet become sweaty while confined in tight shoes.",
        "symptoms": ["Scaly, peeling skin", "Itching and burning", "Blisters", "Dry skin on soles", "Raw skin between toes"],
        "causes": ["Trichophyton fungus", "Warm, moist environments", "Shared showers/pools", "Tight footwear"],
        "recommendation": "Use over-the-counter antifungal creams, sprays, or powders. Keep feet dry and clean. Wear breathable footwear and change socks regularly.",
        "severity": "mild",
        "contagious": True,
        "detectable": True
    },
    "Nail Fungus": {
        "category": "Fungal Infections",
        "description": "A fungal infection (onychomycosis) affecting fingernails or toenails. Causes thickening, discoloration (yellow/brown), and crumbling at the edge of the nail. Can be difficult to treat.",
        "symptoms": ["Thickened nails", "Yellow/brown discoloration", "Brittle, crumbly nails", "Distorted nail shape", "Foul odor"],
        "causes": ["Dermatophyte fungi", "Warm, moist conditions", "Damaged nails", "Poor circulation"],
        "recommendation": "See a dermatologist for prescription oral antifungal medication. Treatment takes 6-12 months. Keep nails trimmed short and dry.",
        "severity": "mild-moderate",
        "contagious": True,
        "detectable": True
    },
    "Ringworm": {
        "category": "Fungal Infections",
        "description": "A contagious fungal infection (tinea corporis) causing a ring-shaped, red, itchy patch on the skin with clearer skin in the center. Despite the name, no worm is involved.",
        "symptoms": ["Ring-shaped rash", "Red, scaly border", "Itching", "Clear center", "Multiple rings"],
        "causes": ["Dermatophyte fungi", "Contact with infected person/animal", "Contaminated objects", "Warm, humid conditions"],
        "recommendation": "Apply antifungal creams (clotrimazole, miconazole) for 2-4 weeks. Keep the area clean and dry. Avoid sharing personal items.",
        "severity": "mild",
        "contagious": True,
        "detectable": True
    },
    "Cutaneous Larva Migrans": {
        "category": "Parasitic Infections",
        "description": "A parasitic skin infection caused by hookworm larvae penetrating the skin. Creates distinctive winding, snake-like tracks that are intensely itchy. Often acquired from walking barefoot on contaminated sand/soil.",
        "symptoms": ["Winding red tracks", "Intense itching", "Raised, snake-like lines", "Blisters along tracks"],
        "causes": ["Hookworm larvae", "Contaminated sand/soil", "Animal feces (dogs/cats)", "Walking barefoot"],
        "recommendation": "Consult a doctor for antiparasitic medication (ivermectin or albendazole). Avoid scratching to prevent secondary infection. Wear footwear on beaches.",
        "severity": "moderate",
        "contagious": False,
        "detectable": True
    },
    "Chickenpox": {
        "category": "Viral Infections",
        "description": "A highly contagious viral infection (varicella) causing an itchy, blister-like rash covering the body. Usually mild in children but can be severe in adults and immunocompromised individuals.",
        "symptoms": ["Itchy blisters", "Fever", "Fatigue", "Loss of appetite", "Headache", "Rash progressing from spots to blisters to crusts"],
        "causes": ["Varicella-zoster virus", "Airborne transmission", "Direct contact with blisters"],
        "recommendation": "Rest and stay hydrated. Use calamine lotion and oatmeal baths for itching. Take antihistamines as needed. Consult doctor for antivirals if high-risk.",
        "severity": "moderate",
        "contagious": True,
        "detectable": True
    },
    "Shingles": {
        "category": "Viral Infections",
        "description": "A painful viral infection (herpes zoster) causing a blistering rash, typically appearing as a stripe on one side of the body. Caused by reactivation of the dormant chickenpox virus, often triggered by stress or weakened immunity.",
        "symptoms": ["Burning pain", "Tingling/numbness", "Stripe of blisters", "Sensitivity to touch", "Fever", "Fatigue"],
        "causes": ["Reactivation of varicella-zoster virus", "Weakened immune system", "Aging", "Stress"],
        "recommendation": "⚠️ Seek medical attention within 72 hours for antiviral medication. Pain management is important. Keep rash clean and covered. Vaccine available for prevention.",
        "severity": "moderate-high",
        "contagious": True,
        "detectable": True
    },
    
    # ========== ADDITIONAL DISEASES (Information provided, related to detected conditions) ==========
    "Acne": {
        "category": "Inflammatory Conditions",
        "description": "A common skin condition where hair follicles become clogged with oil and dead skin cells. Causes pimples, blackheads, whiteheads, and cysts, primarily on the face, chest, and back.",
        "symptoms": ["Pimples", "Blackheads", "Whiteheads", "Cysts", "Oily skin", "Scarring"],
        "causes": ["Excess oil production", "Clogged hair follicles", "Bacteria", "Hormonal changes"],
        "recommendation": "Use gentle cleansers and non-comedogenic products. Try OTC benzoyl peroxide or salicylic acid. See a dermatologist for severe cases.",
        "severity": "mild-moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Impetigo"]
    },
    "Eczema": {
        "category": "Inflammatory Conditions",
        "description": "A chronic condition (atopic dermatitis) causing dry, itchy, inflamed skin patches. Often appears in childhood and may be associated with allergies and asthma. Symptoms come and go in flares.",
        "symptoms": ["Dry, scaly skin", "Intense itching", "Red patches", "Thickened skin", "Small raised bumps"],
        "causes": ["Genetic factors", "Immune dysfunction", "Environmental triggers", "Skin barrier defects"],
        "recommendation": "Moisturize frequently with fragrance-free products. Identify and avoid triggers. Use topical corticosteroids during flares. See a dermatologist for persistent cases.",
        "severity": "mild-moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Ringworm", "Impetigo"]
    },
    "Psoriasis": {
        "category": "Autoimmune Conditions",
        "description": "An autoimmune condition that causes rapid skin cell buildup, resulting in thick, red patches with silvery scales. Commonly affects elbows, knees, scalp, and lower back.",
        "symptoms": ["Red patches with silvery scales", "Dry, cracked skin", "Itching and burning", "Thickened nails", "Stiff joints"],
        "causes": ["Overactive immune system", "Genetic predisposition", "Triggers (stress, infections, weather)"],
        "recommendation": "Moisturize regularly. Use medicated creams (corticosteroids, vitamin D). Phototherapy may help. Consult a dermatologist for biologics if severe.",
        "severity": "moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Ringworm", "Eczema"]
    },
    "Hives (Urticaria)": {
        "category": "Allergic Reactions",
        "description": "Red, itchy, raised welts (wheals) that appear suddenly, often as an allergic reaction. Individual hives typically last less than 24 hours, but new ones can appear.",
        "symptoms": ["Raised welts", "Intense itching", "Swelling", "Welts that change shape", "Worse with heat"],
        "causes": ["Allergic reactions", "Foods", "Medications", "Insect stings", "Stress", "Infections"],
        "recommendation": "Take antihistamines (Benadryl, Zyrtec). Avoid known triggers. Apply cool compresses. Seek emergency care if throat swelling or breathing difficulty.",
        "severity": "mild-moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Chickenpox", "Shingles"]
    },
    "Contact Dermatitis": {
        "category": "Inflammatory Conditions",
        "description": "Skin inflammation caused by direct contact with irritants (soaps, chemicals) or allergens (nickel, latex, poison ivy). Results in a red, itchy rash in the contact area.",
        "symptoms": ["Red rash", "Itching", "Blisters", "Dry, cracked skin", "Swelling", "Burning"],
        "causes": ["Irritants (soaps, solvents)", "Allergens (nickel, latex)", "Plants (poison ivy)", "Fragrances"],
        "recommendation": "Identify and avoid the trigger. Wash the area thoroughly. Apply corticosteroid cream. Use cool compresses. See a doctor if severe.",
        "severity": "mild-moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Eczema", "Ringworm"]
    },
    "Rosacea": {
        "category": "Inflammatory Conditions",
        "description": "A chronic skin condition causing facial redness, visible blood vessels, and sometimes small pus-filled bumps. Often mistaken for acne or allergic reaction. More common in fair-skinned adults.",
        "symptoms": ["Facial redness", "Visible blood vessels", "Small red bumps", "Eye irritation", "Thickened skin on nose"],
        "causes": ["Unknown (may involve blood vessels, immune system)", "Triggers (sun, stress, alcohol, spicy food)"],
        "recommendation": "Avoid triggers. Use gentle, fragrance-free skincare. Protect skin from sun. See a dermatologist for prescription treatments (metronidazole, azelaic acid).",
        "severity": "mild-moderate",
        "contagious": False,
        "detectable": False,
        "related_to": ["Impetigo", "Cellulitis"]
    },
    "Warts": {
        "category": "Viral Infections",
        "description": "Small, rough growths caused by human papillomavirus (HPV) infection. Very common in children. Can appear anywhere but often on hands and feet. Usually harmless but contagious.",
        "symptoms": ["Rough, grainy bumps", "Flesh-colored or gray", "Black dots (clotted blood vessels)", "Clusters of growths"],
        "causes": ["Human papillomavirus (HPV)", "Direct contact", "Shared surfaces", "Scratching/shaving"],
        "recommendation": "Many warts disappear on their own. Try OTC salicylic acid treatments. See a doctor for freezing (cryotherapy) or other removal methods if persistent.",
        "severity": "mild",
        "contagious": True,
        "detectable": False,
        "related_to": ["Chickenpox"]
    },
    "Skin Cancer": {
        "category": "Cancer",
        "description": "Abnormal growth of skin cells, most commonly on sun-exposed areas. Three main types: basal cell carcinoma (most common), squamous cell carcinoma, and melanoma (most dangerous). Early detection is crucial.",
        "symptoms": ["New or changing moles", "Asymmetric lesions", "Irregular borders", "Multiple colors", "Growing or evolving spots", "Non-healing sores"],
        "causes": ["UV radiation (sun/tanning beds)", "Fair skin", "History of sunburns", "Many moles", "Family history"],
        "recommendation": "⚠️ See a dermatologist immediately for any suspicious skin changes. Use ABCDE rule for moles. Protect skin from sun. Get regular skin checks.",
        "severity": "high",
        "contagious": False,
        "detectable": False,
        "related_to": ["Cellulitis"]
    },
    "Jock Itch": {
        "category": "Fungal Infections",
        "description": "A fungal infection (tinea cruris) affecting the groin, inner thighs, and buttocks. Causes an itchy, red, ring-shaped rash. More common in athletes and people who sweat heavily.",
        "symptoms": ["Ring-shaped red rash", "Itching and burning", "Flaking, peeling skin", "Redness in groin folds"],
        "causes": ["Same fungi as athlete's foot", "Warm, moist conditions", "Tight clothing", "Sweating"],
        "recommendation": "Keep area clean and dry. Apply antifungal cream (clotrimazole, terbinafine). Wear loose, cotton underwear. Treat athlete's foot to prevent spread.",
        "severity": "mild",
        "contagious": True,
        "detectable": False,
        "related_to": ["Athlete's Foot", "Ringworm"]
    },
    "Scabies": {
        "category": "Parasitic Infections",
        "description": "An intensely itchy skin condition caused by tiny burrowing mites. Spreads through close personal contact. Causes a pimple-like rash and intense itching, especially at night.",
        "symptoms": ["Intense itching (worse at night)", "Pimple-like rash", "Tiny burrow tracks", "Sores from scratching"],
        "causes": ["Sarcoptes scabiei mite", "Close personal contact", "Shared bedding/clothing"],
        "recommendation": "⚠️ See a doctor for prescription cream (permethrin). All household members should be treated. Wash all bedding and clothing in hot water.",
        "severity": "moderate",
        "contagious": True,
        "detectable": False,
        "related_to": ["Cutaneous Larva Migrans"]
    }
}

# Global model variable
model = None
IMAGE_SIZE = (150, 150)

def load_model():
    """Load the pre-trained skin disease model"""
    global model
    
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'skin_disease_model.h5')
    
    if os.path.exists(model_path):
        print(f"Loading pre-trained model from {model_path}...")
        model = tf.keras.models.load_model(model_path, compile=False)
        print(f"✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Detectable diseases: {len(MODEL_CLASSES)}")
        print(f"   Total disease database: {len(DISEASE_DATABASE)}")
    else:
        raise FileNotFoundError(f"Model not found at {model_path}. Please download the model first.")
    
    return model

def get_related_conditions(predicted_class):
    """Get related conditions that might be similar to the prediction"""
    related = []
    for name, info in DISEASE_DATABASE.items():
        if not info.get("detectable", False):
            related_to = info.get("related_to", [])
            if predicted_class in related_to:
                related.append({
                    "name": name,
                    "category": info["category"],
                    "description": info["description"][:150] + "..."
                })
    return related[:3]  # Return top 3 related conditions

def preprocess_image(image_bytes):
    """Preprocess image for prediction"""
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert('RGB')
    img = img.resize(IMAGE_SIZE)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize to [0,1]
    return img_array

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'detectable_diseases': len(MODEL_CLASSES),
        'total_diseases_in_database': len(DISEASE_DATABASE),
        'model_type': 'Pre-trained CNN'
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict skin disease from uploaded image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read and preprocess image
        image_bytes = file.read()
        img_array = preprocess_image(image_bytes)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        pred_index = np.argmax(predictions[0])
        confidence = float(predictions[0][pred_index])
        predicted_class = MODEL_CLASSES[pred_index]
        
        # Get disease info from database
        disease_info = DISEASE_DATABASE.get(predicted_class, {})
        
        # Get related conditions
        related_conditions = get_related_conditions(predicted_class)
        
        # Get top 3 predictions
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = [
            {
                'class': MODEL_CLASSES[i],
                'confidence': float(predictions[0][i]),
                'category': DISEASE_DATABASE.get(MODEL_CLASSES[i], {}).get('category', 'Unknown')
            }
            for i in top_indices
        ]
        
        return jsonify({
            'success': True,
            'prediction': {
                'class': predicted_class,
                'confidence': confidence,
                'category': disease_info.get('category', 'Unknown'),
                'description': disease_info.get('description', ''),
                'symptoms': disease_info.get('symptoms', []),
                'causes': disease_info.get('causes', []),
                'recommendation': disease_info.get('recommendation', 'Please consult a healthcare professional.'),
                'severity': disease_info.get('severity', 'unknown'),
                'contagious': disease_info.get('contagious', False)
            },
            'top_predictions': top_predictions,
            'related_conditions': related_conditions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diseases', methods=['GET'])
def get_all_diseases():
    """Get comprehensive list of all diseases in database"""
    diseases = []
    for name, info in DISEASE_DATABASE.items():
        diseases.append({
            'name': name,
            'category': info.get('category', 'Unknown'),
            'severity': info.get('severity', 'unknown'),
            'contagious': info.get('contagious', False),
            'detectable': info.get('detectable', False),
            'description': info.get('description', '')[:200] + '...'
        })
    
    # Sort by category
    diseases.sort(key=lambda x: (not x['detectable'], x['category'], x['name']))
    
    return jsonify({
        'diseases': diseases,
        'total': len(diseases),
        'detectable_count': sum(1 for d in diseases if d['detectable']),
        'categories': list(set(d['category'] for d in diseases))
    })

@app.route('/api/disease/<name>', methods=['GET'])
def get_disease_info(name):
    """Get detailed info about a specific disease"""
    # Find disease (case-insensitive)
    for disease_name, info in DISEASE_DATABASE.items():
        if disease_name.lower() == name.lower():
            return jsonify({
                'name': disease_name,
                **info
            })
    
    return jsonify({'error': 'Disease not found'}), 404

if __name__ == '__main__':
    print("🏥 Comprehensive Skin Disease Classifier API")
    print("=" * 60)
    load_model()
    print("=" * 60)
    print(f"✅ Detectable diseases: {', '.join(MODEL_CLASSES)}")
    print(f"📚 Total diseases in database: {len(DISEASE_DATABASE)}")
    print("=" * 60)
    print("Server starting on http://localhost:5001")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5001, debug=True)

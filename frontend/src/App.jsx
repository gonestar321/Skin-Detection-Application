import { useState, useCallback } from 'react'

// API Base URL - uses environment variable in production, localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

function App() {
    const [selectedImage, setSelectedImage] = useState(null)
    const [preview, setPreview] = useState(null)
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [error, setError] = useState(null)
    const [dragActive, setDragActive] = useState(false)

    const handleDrag = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }, [])

    const handleDrop = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0])
        }
    }, [])

    const handleFile = (file) => {
        if (!file.type.startsWith('image/')) {
            setError('Please upload an image file')
            return
        }

        setSelectedImage(file)
        setPreview(URL.createObjectURL(file))
        setResults(null)
        setError(null)
    }

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0])
        }
    }

    const removeImage = () => {
        setSelectedImage(null)
        setPreview(null)
        setResults(null)
        setError(null)
    }

    const analyzeImage = async () => {
        if (!selectedImage) return

        setLoading(true)
        setError(null)

        const formData = new FormData()
        formData.append('file', selectedImage)

        try {
            const response = await fetch(`${API_BASE_URL}/api/predict`, {
                method: 'POST',
                body: formData,
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.error || 'Failed to analyze image')
            }

            setResults(data)
        } catch (err) {
            setError(err.message || 'Something went wrong. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const startNewAnalysis = () => {
        setSelectedImage(null)
        setPreview(null)
        setResults(null)
        setError(null)
    }

    const getSeverityColor = (severity) => {
        if (severity?.includes('high')) return '#EF4444'
        if (severity?.includes('moderate')) return '#F59E0B'
        return '#10B981'
    }

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="logo">
                    <div className="logo-icon">🔬</div>
                    DermaScan AI
                </div>
                <nav>
                    <ul className="nav-links">
                        <li><a href="#analyze">Analyze</a></li>
                        <li><a href="#features">Features</a></li>
                        <li><a href="#about">About</a></li>
                    </ul>
                </nav>
            </header>

            {/* Main Content */}
            <main className="main-content">
                {/* Hero Section */}
                <section className="hero" id="analyze">
                    <div className="hero-badge">
                        <span className="hero-badge-dot"></span>
                        AI-Powered Analysis
                    </div>
                    <h1>
                        Skin Disease <span>Detection</span>
                        <br />Made Simple
                    </h1>
                    <p className="hero-description">
                        Upload a photo of your skin concern and get instant AI-powered analysis
                        with comprehensive information on 17+ skin conditions including symptoms,
                        causes, and recommendations.
                    </p>
                </section>

                {/* Upload Section */}
                <section className="upload-section">
                    {!preview ? (
                        <div
                            className={`upload-container ${dragActive ? 'drag-active' : ''}`}
                            onDragEnter={handleDrag}
                            onDragLeave={handleDrag}
                            onDragOver={handleDrag}
                            onDrop={handleDrop}
                            onClick={() => document.getElementById('file-input').click()}
                        >
                            <input
                                id="file-input"
                                type="file"
                                className="file-input"
                                accept="image/*"
                                onChange={handleFileChange}
                            />
                            <div className="upload-icon">📷</div>
                            <div className="upload-text">
                                <h3>Drop your image here</h3>
                                <p>or <span>browse files</span> from your device</p>
                                <p style={{ marginTop: '12px', fontSize: '0.875rem' }}>
                                    Supports JPG, PNG, WEBP
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="preview-container">
                            <div className="preview-card">
                                <div className="preview-image-wrapper">
                                    <img src={preview} alt="Preview" className="preview-image" />
                                    <button className="remove-image-btn" onClick={removeImage}>
                                        ✕
                                    </button>
                                </div>

                                {error && (
                                    <div className="error-message">
                                        {error}
                                    </div>
                                )}

                                {!results && (
                                    <button
                                        className="analyze-btn"
                                        onClick={analyzeImage}
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner"></span>
                                                Analyzing...
                                            </>
                                        ) : (
                                            <>
                                                🔍 Analyze Skin Condition
                                            </>
                                        )}
                                    </button>
                                )}
                            </div>
                        </div>
                    )}
                </section>

                {/* Results Section */}
                {results && results.success && (
                    <section className="results-section">
                        <div className="results-card">
                            <div className="results-header">
                                <h2>Analysis Complete ✓</h2>
                                <p style={{ color: 'var(--text-secondary)' }}>
                                    Here's what our AI detected
                                </p>
                            </div>

                            <div className="prediction-main">
                                <div className="prediction-category">
                                    {results.prediction.category}
                                </div>
                                <div className="prediction-class">
                                    {results.prediction.class}
                                </div>
                                <div className="confidence-bar">
                                    <div
                                        className="confidence-fill"
                                        style={{ width: `${results.prediction.confidence * 100}%` }}
                                    ></div>
                                </div>
                                <div className="confidence-text">
                                    {(results.prediction.confidence * 100).toFixed(1)}% Confidence
                                </div>

                                <div className="prediction-badges">
                                    <span
                                        className="severity-badge"
                                        style={{ backgroundColor: getSeverityColor(results.prediction.severity) }}
                                    >
                                        {results.prediction.severity?.replace('-', ' to ').toUpperCase()} SEVERITY
                                    </span>
                                    {results.prediction.contagious && (
                                        <span className="contagious-badge">
                                            ⚠️ CONTAGIOUS
                                        </span>
                                    )}
                                </div>
                            </div>

                            <div className="disease-info">
                                <div className="info-card">
                                    <h4>📋 Description</h4>
                                    <p>{results.prediction.description}</p>
                                </div>

                                {results.prediction.symptoms && results.prediction.symptoms.length > 0 && (
                                    <div className="info-card">
                                        <h4>🔍 Common Symptoms</h4>
                                        <ul className="symptoms-list">
                                            {results.prediction.symptoms.map((symptom, i) => (
                                                <li key={i}>{symptom}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {results.prediction.causes && results.prediction.causes.length > 0 && (
                                    <div className="info-card">
                                        <h4>⚡ Possible Causes</h4>
                                        <ul className="symptoms-list">
                                            {results.prediction.causes.map((cause, i) => (
                                                <li key={i}>{cause}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                <div className="info-card recommendation-card">
                                    <h4>💡 Recommendation</h4>
                                    <p>{results.prediction.recommendation}</p>
                                </div>
                            </div>

                            {results.related_conditions && results.related_conditions.length > 0 && (
                                <div className="related-conditions">
                                    <h4>📚 Other Conditions to Consider</h4>
                                    <p style={{ color: 'var(--text-secondary)', marginBottom: '16px', fontSize: '0.875rem' }}>
                                        Based on your symptoms, you may also want to learn about:
                                    </p>
                                    <div className="related-list">
                                        {results.related_conditions.map((condition, index) => (
                                            <div key={index} className="related-item">
                                                <span className="related-name">{condition.name}</span>
                                                <span className="related-category">{condition.category}</span>
                                                <p className="related-desc">{condition.description}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {results.top_predictions && results.top_predictions.length > 1 && (
                                <div className="top-predictions">
                                    <h4>Other Possible Detections</h4>
                                    <div className="prediction-list">
                                        {results.top_predictions.slice(1).map((pred, index) => (
                                            <div key={index} className="prediction-item">
                                                <div>
                                                    <span className="prediction-item-name">{pred.class}</span>
                                                    <span className="prediction-item-category">{pred.category}</span>
                                                </div>
                                                <span className="prediction-item-confidence">
                                                    {(pred.confidence * 100).toFixed(1)}%
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <button className="new-analysis-btn" onClick={startNewAnalysis}>
                                🔄 Start New Analysis
                            </button>
                        </div>

                        <div className="disclaimer">
                            <p>
                                ⚠️ <strong>Medical Disclaimer:</strong> This tool is for educational purposes only and
                                should not replace professional medical advice. Always consult a qualified dermatologist
                                or healthcare provider for accurate diagnosis and treatment.
                            </p>
                        </div>
                    </section>
                )}

                {/* Features Section */}
                <section className="features" id="features">
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">🧠</div>
                            <h3>Deep Learning</h3>
                            <p>
                                Powered by a trained CNN model capable of detecting
                                8 skin conditions with detailed information on 17+ diseases.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">📚</div>
                            <h3>Comprehensive Database</h3>
                            <p>
                                Detailed information on symptoms, causes, severity levels,
                                and treatment recommendations for each condition.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🔒</div>
                            <h3>Privacy First</h3>
                            <p>
                                Your images are processed securely and never stored on
                                our servers. All analysis happens in real-time.
                            </p>
                        </div>
                    </div>
                </section>

                {/* Supported Conditions */}
                <section className="conditions-section" style={{ maxWidth: '1200px', margin: '60px auto 0', padding: '0 20px' }}>
                    <h2 style={{ textAlign: 'center', marginBottom: '32px' }}>Conditions We Cover</h2>
                    <div className="conditions-grid" style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                        gap: '16px'
                    }}>
                        {[
                            { name: 'Acne', icon: '🔴' },
                            { name: 'Eczema', icon: '🩹' },
                            { name: 'Psoriasis', icon: '🔶' },
                            { name: 'Ringworm', icon: '⭕' },
                            { name: "Athlete's Foot", icon: '🦶' },
                            { name: 'Nail Fungus', icon: '💅' },
                            { name: 'Cellulitis', icon: '🔺' },
                            { name: 'Impetigo', icon: '🟡' },
                            { name: 'Hives', icon: '🟠' },
                            { name: 'Contact Dermatitis', icon: '⚡' },
                            { name: 'Rosacea', icon: '🌹' },
                            { name: 'Warts', icon: '🔘' },
                            { name: 'Chickenpox', icon: '🦠' },
                            { name: 'Shingles', icon: '⚠️' },
                            { name: 'Skin Cancer', icon: '🎗️' },
                            { name: 'Scabies', icon: '🔬' },
                            { name: 'Jock Itch', icon: '🏃' }
                        ].map((condition, i) => (
                            <div key={i} style={{
                                background: 'var(--glass-bg)',
                                border: '1px solid var(--glass-border)',
                                borderRadius: '12px',
                                padding: '16px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '12px'
                            }}>
                                <span style={{ fontSize: '1.5rem' }}>{condition.icon}</span>
                                <span style={{ fontSize: '0.9375rem' }}>{condition.name}</span>
                            </div>
                        ))}
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="footer" id="about">
                <p>
                    Built with ❤️ using TensorFlow & React |
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer"> View on GitHub</a>
                </p>
                <p style={{ marginTop: '8px' }}>
                    © 2024 DermaScan AI - Skin Disease Classifier by Tejasv Dua
                </p>
            </footer>
        </div>
    )
}

export default App

mishtee_css = """
/* Import premium fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400&display=swap');

/* Main Container */
.gradio-container {
    background-color: #FAF9F6 !important;
    color: #333333 !important;
    font-family: 'Inter', sans-serif;
}

/* Headings - High-end Serif */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    color: #333333;
}

/* Buttons - Sober Terracotta & Sharp Edges */
button.primary, .gr-button-lg {
    background-color: #C06C5C !important;
    color: #FAF9F6 !important;
    border: 1px solid #C06C5C !important;
    border-radius: 0px !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 12px 24px !important;
    transition: all 0.3s ease;
}

button.primary:hover {
    background-color: transparent !important;
    color: #C06C5C !important;
    border: 1px solid #C06C5C !important;
}

/* Inputs & Textboxes */
input, textarea, .gr-input {
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
    background-color: transparent !important;
    padding: 10px !important;
}

/* Tables - Lightweight Sans-Serif */
table, .gr-table {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-collapse: collapse !important;
}

th, td {
    border-bottom: 1px solid #333333 !important;
    padding: 15px !important;
    text-align: left;
}

/* Layout Spacing (Significant Padding) */
.gap, .form {
    gap: 40px !important;
}

.block {
    margin-bottom: 30px !important;
    border: 1px solid #E0DED7 !important; /* Subtle divider */
    border-radius: 0px !important;
    box-shadow: none !important; /* No shadows as requested */
}

/* Remove Bubbly Elements */
* {
    border-radius: 0px !important;
}
"""

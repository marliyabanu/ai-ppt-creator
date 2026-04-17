from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Create output folder for PPT files
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_ppts')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"✅ Output folder: {OUTPUT_DIR}")

CREATOR = "B. MARLIYA BANU"

# Colors
BLUE = RGBColor(0, 51, 102)
GREEN = RGBColor(0, 128, 0)
RED = RGBColor(220, 20, 60)
DARK = RGBColor(50, 50, 50)

def get_font_size(content_length):
    """Auto font size - smaller content = BIGGER font"""
    if content_length <= 2:
        return 40
    elif content_length <= 3:
        return 36
    elif content_length <= 4:
        return 32
    elif content_length <= 6:
        return 28
    elif content_length <= 8:
        return 24
    else:
        return 20

def detect_content_type(title):
    """Detect content type from title"""
    t = title.lower()
    if 'advantage' in t or 'benefit' in t or 'pros' in t:
        return 'advantages'
    if 'disadvantage' in t or 'challenge' in t or 'cons' in t:
        return 'disadvantages'
    if 'feature' in t:
        return 'features'
    return 'standard'

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/generate-outline', methods=['POST'])
def generate_outline():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Presentation')
        num_slides = int(data.get('num_slides', 10))
        
        outline = []
        for i in range(num_slides):
            outline.append({
                "title": f"Slide {i+1}",
                "content": [f"Point 1 about {prompt}", f"Point 2 about {prompt}", f"Point 3 about {prompt}"]
            })
        return jsonify({"outline": outline})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-ppt', methods=['POST'])
def generate_ppt():
    try:
        data = request.get_json()
        
        title = data.get('title', 'My Presentation')
        creator_name = data.get('creator_name', CREATOR)
        slides_content = data.get('slides_content', [])
        
        print(f"Generating PPT: {title}")
        
        # Create presentation
        prs = Presentation()
        
        # ===== TITLE SLIDE =====
        slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(44)
        slide.shapes.title.text_frame.paragraphs[0].font.bold = True
        slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = BLUE
        
        subtitle = slide.placeholders[1]
        subtitle.text = f"Created by {creator_name}\n{datetime.now().strftime('%B %d, %Y')}"
        for para in subtitle.text_frame.paragraphs:
            para.font.size = Pt(18)
            para.font.color.rgb = DARK
        
        # ===== CONTENT SLIDES =====
        for idx, slide_data in enumerate(slides_content[:14]):
            slide_title = slide_data.get('title', f'Slide {idx+1}')
            content_raw = slide_data.get('content', [])
            
            # Clean content
            if isinstance(content_raw, str):
                content = [c.strip() for c in content_raw.split('\n') if c.strip()]
            else:
                content = [str(c).strip() for c in content_raw if c and str(c).strip()]
            
            if not content:
                content = ["No content provided"]
            
            # Detect content type and set font size
            content_type = detect_content_type(slide_title)
            font_size = get_font_size(len(content))
            
            # Create slide
            bullet_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_layout)
            slide.shapes.title.text = slide_title
            slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(32)
            slide.shapes.title.text_frame.paragraphs[0].font.bold = True
            slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = BLUE
            
            # Add content based on type
            text_frame = slide.placeholders[1].text_frame
            text_frame.clear()
            
            if content_type == 'advantages':
                for item in content:
                    p = text_frame.add_paragraph()
                    p.text = f"✓  {item}"
                    p.font.size = Pt(font_size)
                    p.font.color.rgb = GREEN
                    p.space_after = Pt(12)
            elif content_type == 'disadvantages':
                for item in content:
                    p = text_frame.add_paragraph()
                    p.text = f"⚠  {item}"
                    p.font.size = Pt(font_size)
                    p.font.color.rgb = RED
                    p.space_after = Pt(12)
            elif content_type == 'features':
                for i, item in enumerate(content, 1):
                    p = text_frame.add_paragraph()
                    p.text = f"{i}.  {item}"
                    p.font.size = Pt(font_size)
                    p.font.color.rgb = DARK
                    p.space_after = Pt(12)
            else:
                for item in content:
                    p = text_frame.add_paragraph()
                    p.text = f"•  {item}"
                    p.font.size = Pt(font_size)
                    p.font.color.rgb = DARK
                    p.space_after = Pt(12)
        
        # ===== SAVE FILE =====
        filename = f"presentation_{uuid.uuid4().hex[:6]}.pptx"
        filepath = os.path.join(OUTPUT_DIR, filename)
        prs.save(filepath)
        
        print(f"✅ PPT saved: {filepath}")
        
        return jsonify({"download_url": f"/api/download/{filename}"})
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_ppt(filename):
    try:
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🐰 PPT CREATOR by B. MARLIYA BANU")
    print("="*60)
    print("✅ Server: http://127.0.0.1:5000")
    print("="*60)
    app.run(debug=True, port=5000)
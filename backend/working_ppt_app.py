from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get the absolute path to backend folder
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BACKEND_DIR, 'my_ppt_outputs')

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"✅ Output directory: {OUTPUT_DIR}")

@app.route('/api/generate-outline', methods=['POST'])
def generate_outline():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Presentation')
        num_slides = int(data.get('num_slides', 20))
        
        outline = []
        # Title slide
        outline.append({
            "title": prompt,
            "content": ["Executive Summary", "Key Insights", "Strategic Recommendations", "Next Steps"]
        })
        
        # Generate remaining slides
        for i in range(1, num_slides):
            outline.append({
                "title": f"Section {i}: Important Topic",
                "content": [
                    f"Key point 1 about {prompt}",
                    f"Key point 2 about {prompt}",
                    f"Key point 3 about {prompt}",
                    f"Key point 4 about {prompt}"
                ]
            })
        
        return jsonify({"outline": outline})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-ppt', methods=['POST'])
def generate_ppt():
    try:
        data = request.get_json()
        outline = data.get('outline', [])
        style = data.get('style', 'professional')
        title = data.get('title', 'Presentation')
        
        # Create unique filename
        unique_id = uuid.uuid4().hex[:8]
        filename = f"presentation_{unique_id}.pptx"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Create a simple text content (since we don't have real PPT library)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"PRESENTATION: {title}\n")
            f.write(f"Style: {style}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            for idx, slide in enumerate(outline, 1):
                f.write(f"SLIDE {idx}: {slide['title']}\n")
                f.write("-"*30 + "\n")
                for point in slide['content']:
                    f.write(f"• {point}\n")
                f.write("\n")
        
        # Verify file exists
        if os.path.exists(filepath):
            return jsonify({
                "download_url": f"/api/download/{filename}",
                "filename": filename
            })
        else:
            return jsonify({"error": "File creation failed"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_ppt(filename):
    try:
        # Prevent path traversal
        filename = os.path.basename(filename)
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/octet-stream'
            )
        else:
            return jsonify({"error": f"File not found: {filename}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "output_dir": OUTPUT_DIR})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 SERVER RUNNING")
    print(f"📁 Output folder: {OUTPUT_DIR}")
    print(f"🌐 http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
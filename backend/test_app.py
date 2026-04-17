from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import uuid
import os.path

app = Flask(__name__)
CORS(app)

# Get the absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')

# Create outputs folder if it doesn't exist
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)
    print(f"Created outputs directory at: {OUTPUTS_DIR}")

@app.route('/api/generate-outline', methods=['POST'])
def generate_outline():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Presentation')
        num_slides = data.get('num_slides', 10)
        
        outline = []
        
        # Title slide
        outline.append({
            "title": prompt,
            "content": [
                "Comprehensive Overview",
                "Key Insights and Analysis",
                "Strategic Recommendations",
                "Executive Summary"
            ]
        })
        
        # Generate content slides
        topics = [
            "Introduction and Background",
            "Market Analysis",
            "Key Challenges",
            "Opportunities and Growth",
            "Strategic Framework",
            "Implementation Plan",
            "Timeline and Milestones",
            "Resource Requirements",
            "Risk Assessment",
            "Performance Metrics",
            "Case Studies",
            "Best Practices",
            "Technology Stack",
            "Team Structure",
            "Budget Overview",
            "ROI Analysis",
            "Next Steps",
            "Conclusion",
            "Q&A Session"
        ]
        
        for i in range(min(num_slides - 1, len(topics))):
            outline.append({
                "title": topics[i],
                "content": [
                    f"Overview of {topics[i].lower()}",
                    "Key considerations and factors",
                    "Best practices and industry standards",
                    "Expected outcomes and benefits",
                    "Actionable recommendations"
                ]
            })
        
        # Add more slides if needed
        while len(outline) < num_slides:
            outline.append({
                "title": f"Additional Topic {len(outline)}",
                "content": [
                    "Important considerations",
                    "Key takeaways",
                    "Implementation strategies",
                    "Success metrics"
                ]
            })
        
        print(f"Generated outline with {len(outline)} slides")
        return jsonify({'outline': outline})
        
    except Exception as e:
        print(f"Error in generate_outline: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-ppt', methods=['POST'])
def generate_ppt():
    try:
        data = request.get_json()
        outline = data.get('outline', [])
        style = data.get('style', 'professional')
        title = data.get('title', 'Presentation')
        
        # Generate unique filename
        filename = f"presentation_{uuid.uuid4().hex[:8]}.txt"
        filepath = os.path.join(OUTPUTS_DIR, filename)
        
        print(f"Creating presentation at: {filepath}")
        
        # Create the presentation content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"PRESENTATION: {title}\n")
            f.write(f"Style: {style}\n")
            f.write(f"Total Slides: {len(outline)}\n")
            f.write("=" * 60 + "\n\n")
            
            for idx, slide in enumerate(outline, 1):
                f.write(f"\n{'=' * 50}\n")
                f.write(f"SLIDE {idx}: {slide['title']}\n")
                f.write(f"{'-' * 50}\n")
                for point in slide['content']:
                    f.write(f"  • {point}\n")
                f.write("\n")
        
        # Verify file was created
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ File created successfully: {filename} ({file_size} bytes)")
        else:
            print(f"❌ Failed to create file: {filepath}")
        
        # Return download URL
        download_url = f'/api/download/{filename}'
        print(f"Download URL: {download_url}")
        
        return jsonify({
            'download_url': download_url,
            'filename': filename
        })
        
    except Exception as e:
        print(f"Error in generate_ppt: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_ppt(filename):
    try:
        # Security check - prevent directory traversal
        filename = os.path.basename(filename)
        filepath = os.path.join(OUTPUTS_DIR, filename)
        
        print(f"Download requested for: {filename}")
        print(f"Full path: {filepath}")
        print(f"File exists: {os.path.exists(filepath)}")
        
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ File found, size: {file_size} bytes")
            
            # Send file with proper headers
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename.replace('.txt', '.pptx'),
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
        else:
            print(f"❌ File not found: {filepath}")
            # List all files in outputs directory
            if os.path.exists(OUTPUTS_DIR):
                files = os.listdir(OUTPUTS_DIR)
                print(f"Files in outputs: {files}")
            return jsonify({'error': f'File not found: {filename}'}), 404
            
    except Exception as e:
        print(f"Error in download_ppt: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    try:
        for filename in os.listdir(OUTPUTS_DIR):
            filepath = os.path.join(OUTPUTS_DIR, filename)
            os.remove(filepath)
            print(f"Removed: {filename}")
        return jsonify({'message': 'Cleanup completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/list-files', methods=['GET'])
def list_files():
    """Helper endpoint to see what files exist"""
    try:
        files = os.listdir(OUTPUTS_DIR) if os.path.exists(OUTPUTS_DIR) else []
        return jsonify({'files': files, 'directory': OUTPUTS_DIR})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SERVER STARTED SUCCESSFULLY!")
    print(f"📍 Running on: http://127.0.0.1:5000")
    print(f"📁 Outputs directory: {OUTPUTS_DIR}")
    print("📡 API Ready to accept requests")
    print("="*60 + "\n")
    app.run(debug=True, port=5000, host='127.0.0.1')
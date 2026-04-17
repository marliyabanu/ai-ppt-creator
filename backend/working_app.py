from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Create outputs folder
OUTPUT_FOLDER = 'generated_ppts'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"Created folder: {OUTPUT_FOLDER}")

@app.route('/api/generate-outline', methods=['POST'])
def generate_outline():
    """Generate presentation outline"""
    try:
        data = request.json
        prompt = data.get('prompt', 'Presentation')
        num_slides = int(data.get('num_slides', 20))
        
        print(f"Generating outline for: {prompt} with {num_slides} slides")
        
        outline = []
        
        # Title slide
        outline.append({
            "title": prompt,
            "content": [
                "Comprehensive Overview",
                "Key Insights & Analysis",
                "Strategic Recommendations",
                "Executive Summary"
            ]
        })
        
        # Generate slide titles based on prompt
        slide_templates = [
            "Introduction to {topic}",
            "Current State of {topic}",
            "Key Challenges in {topic}",
            "Emerging Trends in {topic}",
            "Market Analysis for {topic}",
            "Technological Advances in {topic}",
            "Regulatory Framework for {topic}",
            "Case Study 1: Success Stories",
            "Case Study 2: Lessons Learned",
            "Best Practices in {topic}",
            "Implementation Strategy",
            "Resource Requirements",
            "Risk Management",
            "Performance Metrics",
            "ROI Analysis",
            "Stakeholder Engagement",
            "Timeline and Milestones",
            "Team Structure and Roles",
            "Budget Planning",
            "Future Outlook for {topic}",
            "Recommendations",
            "Conclusion and Next Steps",
            "Q&A Session",
            "References and Resources",
            "Appendix: Additional Data"
        ]
        
        # Generate content for each slide
        for i in range(min(num_slides - 1, len(slide_templates))):
            slide_title = slide_templates[i].replace("{topic}", prompt.split()[0] if prompt else "Topic")
            
            content = [
                f"Overview and background of {slide_title.lower()}",
                f"Key statistics and data points for {prompt}",
                f"Important considerations and factors",
                f"Best practices and industry standards",
                f"Actionable insights and recommendations"
            ]
            
            outline.append({
                "title": slide_title,
                "content": content
            })
        
        # Add extra slides if needed
        while len(outline) < num_slides:
            outline.append({
                "title": f"Additional Insights - Part {len(outline)}",
                "content": [
                    "Deep dive into critical aspects",
                    "Supporting evidence and research",
                    "Practical applications",
                    "Future considerations",
                    "Key takeaways"
                ]
            })
        
        print(f"✅ Generated {len(outline)} slides successfully")
        return jsonify({"outline": outline})
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-ppt', methods=['POST'])
def generate_ppt():
    """Generate PowerPoint file"""
    try:
        data = request.json
        outline = data.get('outline', [])
        style = data.get('style', 'professional')
        title = data.get('title', 'Presentation')
        
        print(f"Generating PPT with {len(outline)} slides in {style} style")
        
        # Create unique filename
        unique_id = uuid.uuid4().hex[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"presentation_{timestamp}_{unique_id}.txt"  # Using .txt for testing
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        # Create the presentation content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"{'PRESENTATION: ' + title:^70}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Style: {style.upper()}\n")
            f.write(f"Total Slides: {len(outline)}\n")
            f.write("-"*70 + "\n\n")
            
            for idx, slide in enumerate(outline, 1):
                f.write(f"\n{'#'*70}\n")
                f.write(f"SLIDE {idx}: {slide['title']}\n")
                f.write(f"{'#'*70}\n")
                for point in slide['content']:
                    f.write(f"  ► {point}\n")
                f.write("\n" + "•"*70 + "\n")
        
        # Verify file was created
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ PPT created successfully: {filename} ({file_size} bytes)")
            
            # Return download info
            return jsonify({
                "success": True,
                "download_url": f"http://127.0.0.1:5000/api/download/{filename}",
                "filename": filename,
                "message": "Presentation generated successfully"
            })
        else:
            raise Exception("File was not created")
        
    except Exception as e:
        print(f"❌ Error generating PPT: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_ppt(filename):
    """Download the generated file"""
    try:
        print(f"Download request for: {filename}")
        
        # Security check
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({"error": "Invalid filename"}), 400
        
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        if os.path.exists(filepath):
            print(f"✅ File found: {filepath}")
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename.replace('.txt', '.pptx'),
                mimetype='application/octet-stream'
            )
        else:
            print(f"❌ File not found: {filepath}")
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        print(f"❌ Download error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/list-files', methods=['GET'])
def list_files():
    """List all generated files"""
    try:
        files = os.listdir(OUTPUT_FOLDER) if os.path.exists(OUTPUT_FOLDER) else []
        return jsonify({
            "files": files,
            "count": len(files),
            "folder": OUTPUT_FOLDER
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Delete all generated files"""
    try:
        for file in os.listdir(OUTPUT_FOLDER):
            filepath = os.path.join(OUTPUT_FOLDER, file)
            os.remove(filepath)
            print(f"Deleted: {file}")
        return jsonify({"message": f"Cleaned up {len(os.listdir(OUTPUT_FOLDER))} files"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "server": "running",
        "output_folder": OUTPUT_FOLDER,
        "files_count": len(os.listdir(OUTPUT_FOLDER)) if os.path.exists(OUTPUT_FOLDER) else 0
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎯 AI PPT CREATOR - BACKEND SERVER")
    print("="*70)
    print(f"✅ Server running at: http://127.0.0.1:5000")
    print(f"✅ Health check: http://127.0.0.1:5000/api/health")
    print(f"✅ Output folder: {os.path.abspath(OUTPUT_FOLDER)}")
    print("="*70)
    print("\n🚀 Ready to generate presentations!\n")
    app.run(debug=True, port=5000, host='127.0.0.1')
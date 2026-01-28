from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import PyPDF2
from youtube_transcript_api import YouTubeTranscriptApi
import re
from anthropic import Anthropic
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Anthropic client (you'll need to set your API key)
# Set your API key as environment variable: export ANTHROPIC_API_KEY='your-key-here'
anthropic_client = None
try:
    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
except Exception as e:
    print(f"Warning: Anthropic client not initialized. Set ANTHROPIC_API_KEY environment variable. Error: {e}")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text
def chunk_text(text, chunk_size=12000):
    """
    Split large text into smaller chunks to avoid token limits
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks 


from urllib.parse import urlparse, parse_qs

def extract_youtube_id(url):
    try:
        parsed = urlparse(url)

        if parsed.hostname in ("www.youtube.com", "youtube.com"):
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]
            if parsed.path.startswith("/embed/"):
                return parsed.path.split("/")[2]
            if parsed.path.startswith("/shorts/"):
                return parsed.path.split("/")[2]

        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/")

    except Exception:
        return None

    return None





def get_youtube_transcript(video_id):
    try:
        # Get all available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 1️⃣ Try manually created English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(
                ['en', 'en-US', 'en-GB']
            )
        except:
            # 2️⃣ Fallback to auto-generated English transcript
            transcript = transcript_list.find_generated_transcript(
                ['en', 'en-US', 'en-GB']
            )

        # Convert transcript to plain text
        formatter = TextFormatter()
        return formatter.format_transcript(transcript.fetch())

    except Exception as e:
        print("Transcript fetch failed:", e)
        return ""



def summarize_with_claude(text, content_type="document"):
    """Use Claude to summarize and extract information"""
    if not anthropic_client:
        # Fallback to basic extraction if Claude is not available
        return basic_extraction(text, content_type)
    
    prompt = f"""You are an academic assistant. Analyze the following {content_type} and provide:

1. A comprehensive summary (2-3 paragraphs)
2. Key concepts (list the main ideas, theories, or topics)
3. All equations and formulas (if any, in their original mathematical notation)
4. Additional important details

Format your response as JSON with the following structure:
{{
    "summary": "your summary here",
    "key_concepts": ["concept1", "concept2", ...],
    "equations": ["equation1", "equation2", ...],
    "details": "additional details here"
}}

Content to analyze:
{text[:15000]}  # Limit to first 15000 characters to stay within token limits
"""

    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse Claude's response
        response_text = message.content[0].text
        
        # Try to extract JSON from response
        import json
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            # If no JSON found, create structured response from text
            return {
                "summary": response_text[:500],
                "key_concepts": [],
                "equations": [],
                "details": response_text[500:] if len(response_text) > 500 else ""
            }
    except Exception as e:
        print(f"Error with Claude API: {str(e)}")
        return basic_extraction(text, content_type)


def basic_extraction(text, content_type):
    """Basic extraction without AI (fallback)"""
    # Extract potential equations (basic pattern matching)
    equation_patterns = [
        r'[A-Za-z]\s*=\s*[^,\n]+',  # Simple equations
        r'\$.*?\$',  # LaTeX inline
        r'\$\$.*?\$\$',  # LaTeX display
    ]
    
    equations = []
    for pattern in equation_patterns:
        matches = re.findall(pattern, text)
        equations.extend(matches[:10])  # Limit to 10 equations
    
    # Basic summary (first few sentences)
    sentences = re.split(r'[.!?]+', text)
    summary = '. '.join(sentences[:5]) + '.'
    
    # Extract potential key concepts (capitalized phrases)
    concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    key_concepts = list(set(concepts[:10]))  # Unique, limit to 10
    
    return {
        "summary": summary[:500],
        "key_concepts": key_concepts,
        "equations": list(set(equations)),
        "details": f"This is a basic extraction. For better results, set up Claude API key. Content length: {len(text)} characters."
    }


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Academic Summarizer API",
        "version": "1.0",
        "endpoints": {
            "/api/summarize-pdf": "POST - Upload PDF file",
            "/api/summarize-youtube": "POST - Submit YouTube URL"
        }
    })


@app.route('/api/summarize-pdf', methods=['POST'])
def summarize_pdf():
    """Endpoint to summarize PDF documents"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            text = extract_text_from_pdf(filepath)

            # Split text into chunks
            chunks = chunk_text(text)
            
            combined_summary = []
            key_concepts = set()
            equations = set()
            # Limit number of chunks to avoid huge API cost
            MAX_CHUNKS = 5
            for chunk in chunks[:MAX_CHUNKS]:
                result = summarize_with_claude(chunk, "PDF document")
                combined_summary.append(result.get("summary", ""))
                key_concepts.update(result.get("key_concepts", []))
                equations.update(result.get("equations", []))
            return jsonify({
                "summary": " ".join(combined_summary),
                "key_concepts": list(key_concepts),
                "equations": list(equations),
                "details": f"Processed {min(len(chunks), MAX_CHUNKS)} chunks out of {len(chunks)}"
                }), 200
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/summarize-youtube', methods=['POST'])
def summarize_youtube():
    """Endpoint to summarize YouTube videos"""
    try:
        # Get URL from request
        data = request.form
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        # Extract video ID
        video_id = extract_youtube_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        # Get transcript
        transcript = get_youtube_transcript(video_id)
        
        if not transcript.strip():
            return jsonify({"error": "No transcript available for this video"}), 400
        
        # Summarize with Claude
        result = summarize_with_claude(transcript, "YouTube video")
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "claude_api": "configured" if anthropic_client else "not configured"
    }), 200


if __name__ == '__main__':
    print("="*60)
    print("Academic Summarizer Backend Server")
    print("="*60)
    print("Server starting on http://localhost:5000")
    print()
    if not anthropic_client:
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("   Basic extraction will be used without AI.")
    else:
        print("✓ Claude API configured")
    print()
    print("Endpoints available:")
    print("  - POST /api/summarize-pdf")
    print("  - POST /api/summarize-youtube")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

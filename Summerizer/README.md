# Academic Summarizer

A web application that extracts and summarizes key concepts, equations, and data from PDF documents and YouTube videos for academic purposes.

## Features

- 📄 **PDF Analysis**: Upload academic PDFs to extract summaries, key concepts, and equations
- 🎥 **YouTube Video Analysis**: Analyze educational YouTube videos using transcripts
- 🤖 **AI-Powered**: Uses Claude AI for intelligent summarization (with fallback for basic extraction)
- 🎨 **Beautiful UI**: Clean, academic-themed interface with smooth animations
- 🔒 **Privacy-Focused**: Files are processed locally and deleted after analysis

## Architecture

- **Frontend**: Pure HTML/CSS/JavaScript with a scholarly design aesthetic
- **Backend**: Python Flask REST API
- **AI Processing**: Anthropic Claude API for intelligent content analysis

## Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- (Optional) Anthropic API key for AI-powered summarization

## Installation

### 1. Clone or Download the Project

Extract the files to a directory on your computer.

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure Claude API

For AI-powered summarization, you need an Anthropic API key:

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Set it as an environment variable:

```bash
# On Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"

# On macOS/Linux
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Note**: Without the API key, the app will use basic extraction (pattern matching) which is less sophisticated but still functional.

## Running the Application

### 1. Start the Backend Server

From the backend directory (with virtual environment activated):

```bash
python app.py
```

You should see:
```
Academic Summarizer Backend Server
Server starting on http://localhost:5000
✓ Claude API configured (or warning if not set)
```

The backend will run on `http://localhost:5000`

### 2. Open the Frontend

Simply open the `frontend/index.html` file in your web browser:

- **Option 1**: Double-click `index.html` in your file explorer
- **Option 2**: Right-click → Open with → Your Browser
- **Option 3**: Drag and drop into browser window

Or use a local server (recommended for development):

```bash
cd frontend
# Python 3
python -m http.server 8080

# Then open: http://localhost:8080
```

## Usage

### Analyzing a PDF Document

1. Click "Choose File" in the PDF Document card
2. Select your academic PDF
3. Click "Analyze PDF"
4. Wait for processing (usually 5-30 seconds)
5. View the extracted summary, concepts, and equations

### Analyzing a YouTube Video

1. Copy a YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Paste it into the YouTube Video URL field
3. Click "Analyze Video"
4. Wait for processing
5. View the summarized content

**Note**: Only videos with available transcripts (closed captions) can be analyzed.

## API Endpoints

### Health Check
```
GET http://localhost:5000/health
```

### Summarize PDF
```
POST http://localhost:5000/api/summarize-pdf
Content-Type: multipart/form-data

Body: 
- file: PDF file
```

### Summarize YouTube
```
POST http://localhost:5000/api/summarize-youtube
Content-Type: multipart/form-data

Body:
- url: YouTube video URL
```

## Response Format

All summarization endpoints return JSON:

```json
{
  "summary": "A comprehensive summary of the content...",
  "key_concepts": [
    "Concept 1",
    "Concept 2",
    "Concept 3"
  ],
  "equations": [
    "E = mc²",
    "F = ma"
  ],
  "details": "Additional important details..."
}
```

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Make sure you've activated the virtual environment and installed requirements:
  ```bash
  pip install -r requirements.txt
  ```

### Frontend can't connect to backend

**Error**: "Failed to connect to the server"
- **Solution**: 
  1. Verify backend is running on port 5000
  2. Check for firewall blocking localhost connections
  3. Try accessing `http://localhost:5000/health` directly in browser

### PDF extraction returns no text

**Issue**: PDF analysis says "No text could be extracted"
- **Solution**: 
  - The PDF might be image-based (scanned document)
  - Try a different PDF with selectable text
  - Consider using OCR tools to convert scanned PDFs first

### YouTube transcript not available

**Error**: "No transcript available for this video"
- **Solution**:
  - Video might not have captions/subtitles
  - Try a different video with available transcripts
  - Look for educational content which usually has captions

### Claude API errors

**Error**: Related to Anthropic API
- **Solution**:
  1. Verify your API key is correct
  2. Check you have API credits available
  3. The app will fall back to basic extraction if Claude fails

## File Structure

```
academic-summarizer/
├── frontend/
│   └── index.html          # Frontend application
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── uploads/            # Temporary upload directory (created automatically)
└── README.md               # This file
```

## Development

### Modifying the Frontend

The frontend is a single HTML file with embedded CSS and JavaScript. Key sections:

- **Styling**: `<style>` tag contains all CSS with CSS variables for theming
- **HTML Structure**: Two cards for PDF/YouTube input, result section
- **JavaScript**: API calls, form handling, and result display

### Modifying the Backend

Key files in `app.py`:

- **Routes**: Flask route handlers for each endpoint
- **PDF Processing**: `extract_text_from_pdf()` function
- **YouTube Processing**: `get_youtube_transcript()` function  
- **AI Summarization**: `summarize_with_claude()` function
- **Fallback**: `basic_extraction()` for when Claude isn't available

## Security Considerations

- Files are temporarily stored and immediately deleted after processing
- Maximum file size is limited to 16MB
- Only PDF files are accepted for upload
- CORS is enabled (configure appropriately for production)
- Input validation on URLs and file types

## Performance Tips

- For large PDFs (100+ pages), processing may take 30-60 seconds
- Long YouTube videos (>1 hour) may take longer to process
- Consider adding pagination for very long results
- The app limits text to 15,000 characters when sending to Claude

## Future Enhancements

Potential improvements:

- [ ] Support for more file types (DOCX, TXT, HTML)
- [ ] Batch processing multiple files
- [ ] Export summaries to various formats
- [ ] User authentication and history
- [ ] Advanced equation rendering (LaTeX)
- [ ] Support for multiple languages
- [ ] Real-time progress indicators
- [ ] Caching of processed content

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check backend logs for detailed error messages
4. Ensure API credentials are properly configured

## Credits

- **UI Design**: Scholarly aesthetic with Crimson Pro and JetBrains Mono fonts
- **PDF Processing**: PyPDF2 library
- **YouTube Transcripts**: youtube-transcript-api
- **AI Summarization**: Anthropic Claude API
- **Backend Framework**: Flask with CORS support

---

**Happy Learning! 📚**

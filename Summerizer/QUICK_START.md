# Quick Reference Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
# On Mac/Linux
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# On Windows
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: (Optional) Set API Key
```bash
# Mac/Linux
export ANTHROPIC_API_KEY='your-key-here'

# Windows CMD
set ANTHROPIC_API_KEY=your-key-here

# Windows PowerShell
$env:ANTHROPIC_API_KEY="your-key-here"
```

### Step 3: Run the Application
```bash
# Start backend (from backend folder)
python app.py

# Open frontend/index.html in your browser
```

## 📁 Project Structure
```
academic-summarizer/
├── frontend/
│   └── index.html          # Open this in browser
├── backend/
│   ├── app.py              # Main server
│   ├── requirements.txt    # Dependencies
│   └── test_setup.py       # Test installation
├── README.md               # Full documentation
├── setup.sh                # Auto-setup (Mac/Linux)
└── setup.bat               # Auto-setup (Windows)
```

## 🔧 Common Commands

**Test Installation:**
```bash
cd backend
python test_setup.py
```

**Check Server Health:**
```bash
curl http://localhost:5000/health
```

**View Server Logs:**
- Watch terminal where `python app.py` is running

## 🐛 Quick Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Cannot connect to server":**
- Check backend is running: http://localhost:5000/health
- Check browser console for errors (F12)

**"No text extracted from PDF":**
- PDF might be image-based (scanned)
- Try a different PDF with selectable text

**"No transcript available":**
- Video doesn't have captions
- Try different YouTube video

## 💡 Tips

1. **Use Chrome DevTools** (F12) to see network requests and errors
2. **Backend logs** show detailed error messages
3. **Without Claude API:** App uses basic pattern matching (still works!)
4. **Large files:** May take 30-60 seconds to process
5. **YouTube videos:** Only works with videos that have transcripts/captions

## 📊 Expected Response Time

- Small PDF (1-10 pages): 5-10 seconds
- Medium PDF (10-50 pages): 15-30 seconds
- Large PDF (50+ pages): 30-60 seconds
- YouTube video (10-30 min): 10-20 seconds
- YouTube video (1+ hour): 30-60 seconds

## 🎯 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/api/summarize-pdf` | POST | Analyze PDF |
| `/api/summarize-youtube` | POST | Analyze video |

## 🔐 Security Notes

- Files are deleted immediately after processing
- No data is stored permanently
- All processing happens locally
- 16MB file size limit

## 📝 Example Usage

**Python API Test:**
```python
import requests

# Test PDF
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/summarize-pdf',
        files={'file': f}
    )
print(response.json())

# Test YouTube
response = requests.post(
    'http://localhost:5000/api/summarize-youtube',
    data={'url': 'https://www.youtube.com/watch?v=VIDEO_ID'}
)
print(response.json())
```

## 🌟 Feature Highlights

✓ Beautiful, academic-themed UI
✓ AI-powered summarization
✓ Equation extraction
✓ Concept identification
✓ Works offline (basic mode)
✓ No authentication needed
✓ Privacy-focused
✓ Easy to deploy

---

For full documentation, see README.md

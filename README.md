# WebMind AI

Smart web content analysis with AI-powered multilingual support.

## Features

- 🧠 **AI-Powered Analysis**: Advanced content understanding using Groq LLM
- 🌍 **Multilingual Support**: 12+ languages including English, Spanish, French, German, etc.
- 🔍 **Smart Content Extraction**: Automatically extracts and analyzes web page content
- ⚡ **Real-time Processing**: Fast RAG-based question answering
- 🎯 **Context-Aware**: Provides relevant answers based on page content

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration and RAG pipeline
- **Groq** - High-performance LLM inference
- **FAISS** - Vector similarity search
- **HuggingFace Embeddings** - Text embeddings

### Frontend
- **Chrome Extension** - Browser integration
- **Vanilla JavaScript** - Lightweight UI
- **Modern CSS** - Responsive design

## Installation

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd PageScan/PageSense-RAG-Extension

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 2. Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

### 3. Start the Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Usage

1. **Start the backend server** (must be running on localhost:8000)
2. **Navigate to any webpage** you want to analyze
3. **Click the WebMind AI extension icon**
4. **Select your preferred language** from the dropdown
5. **Ask any question** about the page content
6. **Get AI-powered answers** in your chosen language

## API Endpoints

- `GET /` - API information
- `POST /chat` - Process queries with RAG
- `GET /languages` - Get supported languages

## Configuration

### Environment Variables

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Supported Languages

- 🇺🇸 English
- 🇪🇸 Spanish  
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇨🇳 Chinese
- 🇸🇦 Arabic
- 🇮🇳 Hindi

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Chrome         │    │  FastAPI         │    │  Groq LLM       │
│  Extension      │◄──►│  Backend         │◄──►│  Service        │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  FAISS Vector    │
                       │  Store           │
                       └──────────────────┘
```

## Development

### Project Structure

```
PageSense-RAG-Extension/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag.py               # RAG processor
│   └── requirements.txt     # Python dependencies
├── extension/
│   ├── manifest.json        # Extension configuration
│   ├── popup.html          # Extension UI
│   ├── popup_multilang.js  # Extension logic
│   └── content.js          # Content script
└── README.md
```

### Adding New Languages

1. Update `supported_languages` in `rag.py`
2. Add language patterns in `detect_language()` method
3. Update language options in `popup.html`

## Troubleshooting

### Common Issues

**Extension not working:**
- Ensure backend server is running on localhost:8000
- Check browser console for errors
- Verify extension permissions

**No content found:**
- Try refreshing the page
- Ensure page has readable text content
- Check if page is not a Chrome internal page

**API errors:**
- Verify GROQ_API_KEY is set correctly
- Check internet connection
- Ensure all dependencies are installed

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open a GitHub issue.
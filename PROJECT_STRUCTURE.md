# Project Structure

Complete overview of all files and their purposes.

## 📁 Core Application Files

### `app.py` ⭐
**Main application entry point**
- Pathway streaming pipeline
- Document transformation and chunking
- Vector embedding with OpenAI
- RAG server setup
- **Run with:** `python app.py`

### `config.py`
**Configuration management**
- Environment variable loading
- API keys (OpenAI, GNews)
- Model settings (embedding, LLM)
- Server configuration (host, port)
- Validation logic

### `connectors/news_connector.py` ⭐
**Custom streaming connector**
- Extends `pw.io.python.ConnectorSubject`
- Polls GNews API every 60 seconds
- Deduplicates articles by URL
- Error handling with exponential backoff
- **Key innovation of the project**

## 🧪 Testing & Demo Files

### `demo.py`
**Interactive demonstration**
- Queries RAG system twice
- Proves real-time knowledge updates
- Shows before/after comparison
- Interactive Q&A mode
- **Run with:** `python demo.py`

### `test_api.py`
**API testing script**
- Quick health check
- Tests local or remote deployment
- Validates API responses
- **Run with:** `python test_api.py [URL]`

### `health_check.py`
**Health monitoring**
- Simple health check endpoint
- Used by monitoring systems
- Returns 0 on success, 1 on failure

## 🚀 Deployment Files

### `Dockerfile` ⭐
**Docker containerization**
- Base: python:3.11-slim
- Installs dependencies
- Exposes port 8080
- Runs app.py
- **Build with:** `docker build -t live-news-analyst .`

### `render.yaml` ⭐
**Render deployment config**
- Auto-detected by Render
- Defines web service
- Build and start commands
- Environment variables
- Health check path
- **Enables one-click deployment**

### `runtime.txt`
**Python version specification**
- Specifies Python 3.11.0
- Used by Render and other platforms

### `.dockerignore`
**Docker build exclusions**
- Excludes .env, venv, cache files
- Reduces image size
- Improves build speed

## 📚 Documentation Files

### `README.md` ⭐
**Main project documentation**
- Overview and features
- Quick start guide
- Architecture diagram
- API usage examples
- Links to other docs

### `QUICKSTART.md`
**5-minute setup guide**
- Step-by-step local setup
- API key acquisition
- Installation commands
- Testing instructions
- Troubleshooting basics

### `DEPLOYMENT.md` ⭐
**Production deployment guide**
- Render deployment steps
- Environment variable setup
- Docker deployment
- Cost estimates
- Production optimizations

### `HACKATHON_CHECKLIST.md` ⭐
**Complete submission guide**
- Pre-deployment checklist
- Deployment steps
- Testing procedures
- Demo preparation
- Submission checklist
- **Use this for hackathon submission!**

### `VIDEO_SCRIPT.md` ⭐
**3-minute demo script**
- Timed sections (180 seconds)
- What to show and say
- Visual aids to prepare
- Backup plans
- Recording checklist
- **Follow this for video demo!**

### `ARCHITECTURE.md`
**Technical deep dive**
- System architecture
- Component descriptions
- Data flow diagrams
- Latency analysis
- Scalability considerations
- Comparison with traditional RAG

### `TROUBLESHOOTING.md`
**Problem-solving guide**
- Common issues and solutions
- Deployment problems
- API key issues
- Runtime errors
- Performance optimization
- Debug checklist

### `PITCH.md`
**Hackathon pitch deck**
- Problem statement
- Solution overview
- Technical innovations
- Use cases
- Comparison table
- Demo script
- **Use for presentation!**

### `PROJECT_STRUCTURE.md` (this file)
**File organization guide**
- Complete file listing
- Purpose of each file
- Usage instructions
- Priority indicators (⭐)

## ⚙️ Configuration Files

### `.env.example`
**Environment template**
- Shows required variables
- Example format
- API key placeholders
- **Copy to `.env` and fill in**

### `.gitignore`
**Git exclusions**
- .env (secrets)
- venv/ (dependencies)
- __pycache__/ (Python cache)
- .pathway/ (Pathway cache)
- IDE files

### `requirements.txt` ⭐
**Python dependencies**
- pathway>=0.13.0
- openai>=1.0.0
- python-dotenv>=1.0.0
- requests>=2.31.0
- **Install with:** `pip install -r requirements.txt`

## 🗂️ Alternative Implementations

### `app_file_monitor.py`
**File-based RAG alternative**
- Monitors local folder for changes
- Useful for testing without API limits
- Demonstrates Pathway's file monitoring
- **Run with:** `python app_file_monitor.py`

### `demo_file_monitor.py`
**Demo for file monitoring**
- Currently empty/placeholder
- Would demonstrate file-based updates

## 📊 File Priority Guide

### ⭐⭐⭐ Critical (Must Read)
1. `README.md` - Start here
2. `HACKATHON_CHECKLIST.md` - For submission
3. `VIDEO_SCRIPT.md` - For demo video
4. `app.py` - Main application
5. `connectors/news_connector.py` - Key innovation
6. `render.yaml` - For deployment
7. `DEPLOYMENT.md` - For production

### ⭐⭐ Important (Should Read)
1. `QUICKSTART.md` - For local setup
2. `ARCHITECTURE.md` - For understanding
3. `PITCH.md` - For presentation
4. `config.py` - For configuration
5. `Dockerfile` - For Docker deployment

### ⭐ Useful (Nice to Have)
1. `TROUBLESHOOTING.md` - When issues arise
2. `demo.py` - For testing
3. `test_api.py` - For validation
4. `PROJECT_STRUCTURE.md` - For navigation

## 🎯 Quick Navigation

### Want to...

**Deploy to Render?**
→ Read `DEPLOYMENT.md`
→ Use `render.yaml`
→ Follow `HACKATHON_CHECKLIST.md`

**Run locally?**
→ Read `QUICKSTART.md`
→ Copy `.env.example` to `.env`
→ Run `python app.py`

**Record demo video?**
→ Follow `VIDEO_SCRIPT.md`
→ Use `demo.py` for live demo
→ Reference `PITCH.md` for talking points

**Understand the code?**
→ Read `ARCHITECTURE.md`
→ Study `app.py` and `connectors/news_connector.py`
→ Check `config.py` for settings

**Fix issues?**
→ Check `TROUBLESHOOTING.md`
→ Run `test_api.py` for diagnostics
→ Review logs

**Present to judges?**
→ Use `PITCH.md` as slides
→ Show `README.md` architecture diagram
→ Demo with `demo.py`

## 📈 File Statistics

- **Total Files**: 20+
- **Python Files**: 7
- **Documentation**: 10
- **Configuration**: 6
- **Lines of Code**: ~500
- **Lines of Docs**: ~2000

## 🔄 Typical Workflow

### 1. Initial Setup (10 minutes)
```bash
# Read documentation
cat README.md
cat QUICKSTART.md

# Setup environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with API keys

# Test locally
python app.py
python test_api.py
```

### 2. Deployment (5 minutes)
```bash
# Read deployment guide
cat DEPLOYMENT.md
cat HACKATHON_CHECKLIST.md

# Push to GitHub
git init
git add .
git commit -m "Ready for deployment"
git push

# Deploy on Render
# Follow DEPLOYMENT.md steps
```

### 3. Demo Preparation (15 minutes)
```bash
# Read demo scripts
cat VIDEO_SCRIPT.md
cat PITCH.md

# Practice demo
python demo.py

# Test remote deployment
python test_api.py https://your-app.onrender.com
```

### 4. Submission (5 minutes)
```bash
# Follow checklist
cat HACKATHON_CHECKLIST.md

# Verify all items
# - Code pushed ✓
# - Deployment live ✓
# - Video recorded ✓
# - Documentation complete ✓
```

## 🎓 Learning Path

### Beginner
1. Start with `README.md`
2. Follow `QUICKSTART.md`
3. Run `demo.py`
4. Read `ARCHITECTURE.md` (overview sections)

### Intermediate
1. Study `app.py` structure
2. Understand `connectors/news_connector.py`
3. Read `ARCHITECTURE.md` (deep dive)
4. Experiment with `config.py` settings

### Advanced
1. Modify connector for new sources
2. Optimize chunking strategy
3. Add monitoring and metrics
4. Scale with Docker/Kubernetes

## 🤝 Contributing

If extending this project:

1. **Add new connector**: Create in `connectors/`
2. **Add new docs**: Follow existing format
3. **Update README**: Keep it current
4. **Test thoroughly**: Use `test_api.py`
5. **Document changes**: Update relevant .md files

## 📞 Support

- **Quick questions**: Check `TROUBLESHOOTING.md`
- **Setup issues**: See `QUICKSTART.md`
- **Deployment problems**: Read `DEPLOYMENT.md`
- **Architecture questions**: Study `ARCHITECTURE.md`

---

**Built for Inter IIT Hackathon 2026** 🚀

Last Updated: January 2026

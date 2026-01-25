# News 4U - RSS News Aggregator

A comprehensive news aggregation platform that automatically fetches, processes, and displays news articles from multiple RSS feeds across different categories.

## 📚 Documentation

**For complete documentation, see [DOCUMENTATION.md](./DOCUMENTATION.md)**

**For Raspberry Pi deployment, see [RASPBERRY_PI_DEPLOYMENT.md](./RASPBERRY_PI_DEPLOYMENT.md)**

The full documentation includes:
- Detailed architecture overview
- Complete feature list
- Backend and frontend structure
- API reference
- Database schema
- Development guide
- Deployment instructions
- **Raspberry Pi deployment guide** (with Nginx configuration)

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **Docker** (optional, for containerized setup)

### Local Development Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates SQLite database)
python scripts/init_db.py

# Start the server
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Docker Setup (Recommended for Beginners)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend (port 3000)

## 📖 Key Features

- **Automated RSS Feed Fetching**: Scheduled fetching from multiple news sources
- **Content Extraction**: Intelligent extraction of full article content
- **Categorization**: Automatic categorization (Tech, Global News, Vietnamese News, US News)
- **Search & Filter**: Advanced search and filtering capabilities
- **Feed Management**: Enable/disable feeds dynamically
- **Responsive UI**: Modern interface with dark mode support

## 🏗️ Project Structure

```
news-4u/
├── backend/                  # FastAPI backend application
│   ├── config/              # RSS feed configuration
│   ├── models/              # Database models
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── scripts/             # Utility scripts
├── frontend/                # Next.js frontend application
│   ├── app/                # Next.js pages
│   ├── components/         # React components
│   └── lib/                # Utilities
├── docker-compose.yml       # Docker configuration
└── DOCUMENTATION.md         # Complete documentation
```

## 🔧 Configuration

RSS feeds are configured in `backend/config/rss_feeds.py`.

**To add or modify feeds:**
1. Edit `backend/config/rss_feeds.py`
2. Run `python backend/scripts/init_db.py` to update the database

## 📡 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 For Beginners

This project demonstrates:
- **Full-stack development** with modern frameworks
- **RESTful API design** with FastAPI
- **Database operations** with SQLAlchemy
- **Async programming** in Python
- **React/Next.js** frontend development
- **Docker containerization**
- **RSS feed processing**
- **Web scraping and content extraction**

**Start with**: Read [DOCUMENTATION.md](./DOCUMENTATION.md) for detailed explanations of each component.

## 🐛 Troubleshooting

### Common Issues

1. **Database locked**: Ensure no other process is using the database
2. **Feed fetch failures**: Check internet connection and feed URLs
3. **Import errors**: Make sure virtual environment is activated
4. **Frontend API errors**: Verify `NEXT_PUBLIC_API_URL` is set correctly

For more troubleshooting tips, see [DOCUMENTATION.md](./DOCUMENTATION.md#troubleshooting)

## 📝 License

[Specify your license here]

## 🤝 Contributing

Contributions are welcome! Please read the documentation first to understand the codebase structure.

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
- **PostgreSQL** 15+ (for database)
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

# Create .env file with database credentials
# See backend/DATABASE_SETUP.md for details
cp .env.example .env  # Edit with your database credentials

# Initialize database (PostgreSQL)
# Tables will be created automatically when you start the server
# Or manually apply schema: psql -U your_user -d your_db -f sql/create_schema.sql

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
│   ├── config/              # Configuration (settings, RSS feeds)
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic (RSS, scheduler, extractors)
│   ├── sql/                 # SQL schema files
│   ├── models.py            # Database models (SQLAlchemy)
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── main.py              # FastAPI application entry point
│   ├── README.md            # Backend documentation
│   ├── QUICKSTART.md        # Quick start guide
│   └── DATABASE_SETUP.md    # Database setup guide
├── frontend/                # Next.js frontend application
│   ├── app/                # Next.js pages
│   ├── components/         # React components
│   └── lib/                # Utilities and API client
├── docker-compose.yml       # Docker configuration
└── DOCUMENTATION.md         # Complete documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
DB_NAME=news4u_db
DB_USER=news4u_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
SCHEDULE_ENABLE=true
GEMINI_API_KEY=your_api_key
ARTICLE_EXTRACTION_MAX_RETRY=3
DEBUG_LEVEL=INFO
```

### RSS Feeds
RSS feeds are configured in `backend/config/rss_feeds.py` and stored in the database.

**To add or modify feeds:**
1. Use the API endpoint `/api/news/feeds/add` to add new feeds
2. Use the Feed Manager in the frontend UI
3. Directly edit the database if needed

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

1. **Database connection errors**:
   - Verify PostgreSQL is running
   - Check credentials in `.env` file
   - See [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md#troubleshooting)

2. **Feed fetch failures**:
   - Check internet connection and feed URLs
   - View fetch logs at `/api/news/feeds/logs`

3. **Import errors**:
   - Make sure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Frontend API errors**:
   - Verify `NEXT_PUBLIC_API_URL` is set correctly in frontend/.env
   - Check that backend is running on the correct port

For more troubleshooting tips, see [backend/README.md](backend/README.md#troubleshooting)

## 📝 License

[Specify your license here]

## 🤝 Contributing

Contributions are welcome! Please read the documentation first to understand the codebase structure.

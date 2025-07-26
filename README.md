# 🧠 Dropship Intelligence – Production-Ready Platform

A comprehensive, AI-powered dropshipping product research and analysis platform with real database integration, advanced filtering, and production-ready features.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **MongoDB 4.4+**
- **Git**

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SupperDropShip
   ```

2. **Install MongoDB** (if not already installed)
   ```bash
   # macOS
   brew install mongodb-community
   
   # Ubuntu/Debian
   sudo apt-get install mongodb
   
   # Windows
   # Download from https://www.mongodb.com/try/download/community
   ```

3. **Start MongoDB**
   ```bash
   # macOS
   brew services start mongodb-community
   
   # Ubuntu/Debian
   sudo systemctl start mongod
   ```

4. **Run the production startup script**
   ```bash
   ./start_production.sh
   ```

   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Create a `.env` file with configuration
   - Seed the database with 100+ sample products
   - Start both backend and frontend servers

## 🏗️ Architecture

### Backend (FastAPI + MongoDB)
- **Database**: MongoDB with Motor async driver
- **API**: FastAPI with automatic documentation
- **Authentication**: JWT-based (ready for implementation)
- **AI Integration**: OpenAI and Google AI for content generation
- **Scoring Engine**: Advanced product scoring algorithm
- **Real-time Data**: Social media and trend analysis

### Frontend (Next.js + TypeScript)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with responsive design
- **State Management**: Custom hooks with local storage
- **UI Components**: Modern, accessible components
- **Real-time Updates**: Live data synchronization

## 📊 Features

### 🔍 Product Discovery
- **Advanced Filtering**: Category, price range, score, tags
- **Real-time Search**: Full-text search across titles and descriptions
- **Smart Sorting**: Multiple sort options (score, price, trend, date)
- **Pagination**: Efficient data loading for large datasets

### 🤖 AI-Powered Tools
- **Title Rewriting**: Generate compelling product titles
- **Ad Copy Generation**: Create persuasive marketing copy
- **Description Writing**: Professional product descriptions
- **Trend Analysis**: AI-powered trend insights
- **Keyword Generation**: SEO-optimized keywords

### 📈 Analytics & Scoring
- **Winning Score Algorithm**: 0-100 scoring system
- **Social Media Integration**: Facebook ads and TikTok mentions
- **Trend Data**: Google Trends integration
- **Supplier Tracking**: AliExpress and Temu price monitoring
- **Performance Metrics**: Engagement rates and ROI analysis

### 🎨 User Experience
- **Responsive Design**: Mobile-first approach
- **Real-time Notifications**: Toast notifications for user feedback
- **Local Storage**: Persistent user preferences
- **Dark/Light Mode**: Theme support (ready for implementation)
- **Accessibility**: WCAG compliant components

## 🗄️ Database Schema

### Products Collection
```javascript
{
  _id: ObjectId,
  id: String,
  title: String,
  description: String,
  price: Number,
  compare_price: Number,
  currency: String,
  score: Number,
  category: String,
  tags: [String],
  source_store: String,
  source_url: String,
  supplier_links: Object,
  supplier_prices: Object,
  facebook_ads: [Object],
  tiktok_mentions: [Object],
  trend_data: Object,
  created_at: Date,
  updated_at: Date
}
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=dropship_intelligence

# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```

## 🚀 Production Deployment

### Docker Deployment (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. **Backend**: Deploy FastAPI app to your preferred hosting
2. **Frontend**: Build and deploy Next.js app
3. **Database**: Set up MongoDB cluster
4. **Environment**: Configure production environment variables

## 📚 API Documentation

### Products Endpoints
- `GET /api/products/` - Get products with filtering
- `GET /api/products/{id}` - Get specific product
- `POST /api/products/` - Create new product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `GET /api/products/stats/overview` - Get statistics
- `GET /api/products/categories/list` - Get categories
- `GET /api/products/tags/list` - Get tags

### AI Endpoints
- `POST /api/ai/rewrite-title` - Rewrite product title
- `POST /api/ai/write-ad-copy` - Generate ad copy
- `POST /api/ai/write-description` - Write product description
- `POST /api/ai/explain-why-winning` - Analyze winning factors
- `POST /api/ai/analyze-trends` - Analyze trends
- `POST /api/ai/generate-keywords` - Generate keywords

## 🧪 Development

### Running in Development Mode
```bash
# Backend
cd backend
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

### Database Seeding
```bash
# Seed with sample data
python -c "
import asyncio
from backend.database.seeder import seed_database
asyncio.run(seed_database())
"
```

### Testing
```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend
npm test
```

## 🔒 Security Features

- **CORS Configuration**: Proper cross-origin settings
- **Input Validation**: Pydantic models for data validation
- **Error Handling**: Comprehensive error management
- **Rate Limiting**: Ready for implementation
- **Authentication**: JWT-based auth system (ready)

## 📈 Performance Optimizations

- **Database Indexing**: Optimized MongoDB indexes
- **Async Operations**: Non-blocking I/O operations
- **Caching**: Redis integration ready
- **Pagination**: Efficient data loading
- **Image Optimization**: Next.js image optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting guide

## 🎯 Roadmap

- [ ] User authentication and authorization
- [ ] Advanced analytics dashboard
- [ ] Automated product crawling
- [ ] Email notifications
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Advanced AI features
- [ ] Integration with more platforms

---

**Built with ❤️ for the dropshipping community**

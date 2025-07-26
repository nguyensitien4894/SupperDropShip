# 🧠 Dropship Intelligence – All-in-One Product Research Platform

A full-stack system to discover, analyze, and predict winning dropshipping products across Shopify stores, Facebook Ads, TikTok videos, and supplier platforms like AliExpress, Temu, and 1688.

This system combines and extends the best features of Dropship.io, Minea, and PPSpy — with enhanced AI intelligence, ad analysis, store tracking, and product scoring.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SupperDropShip
   ```

2. **Run the setup script**
   ```bash
   ./start.sh
   ```
   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Create a `.env` file with configuration
   - Set up the project structure

3. **Start the platform**
   ```bash
   ./run.sh
   ```
   This will start both backend and frontend services.

### Manual Setup (Alternative)

If you prefer to set up manually:

1. **Backend Setup**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements-simple.txt
   
   # Start backend
   python -m backend.main
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🌐 Access the Platform

Once running, you can access:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## ✅ Core Modules Overview

| Module                    | Description                                                  |
|---------------------------|--------------------------------------------------------------|
| `shopify-crawler`         | Crawls and indexes products from public Shopify stores       |
| `facebook-ads-crawler`    | Extracts Facebook Ads related to trending products           |
| `tiktok-crawler`          | Scrapes TikTok trending videos based on keywords & hashtags  |
| `supplier-matcher`        | Matches products to AliExpress, Temu, and 1688 suppliers     |
| `score-engine`            | Calculates a winning score based on 5 criteria               |
| `ai-writer`               | Rewrites product titles, descriptions, and ad copy using GPT |
| `trend-analyzer`          | Uses Google Trends to validate keyword interest              |
| `store-analyzer`          | Detects stores using same product + theme + apps             |
| `dashboard-ui`            | User dashboard for search, filter, save, and export          |
| `cron-job-scheduler`      | Auto-update system via hourly/daily jobs                     |

## 🧱 Project Structure
```
SupperDropShip/
│
├── backend/
│ ├── api/ # All REST endpoints
│ │ └── routes/
│ │   ├── products.py
│ │   └── ai_tools.py
│ ├── crawlers/
│ │ └── shopify.py
│ ├── ai/
│ │ └── writer.py
│ ├── scoring/
│ │ └── engine.py
│ ├── database/
│ │ └── models.py
│ └── main.py
│
├── frontend/
│ ├── pages/
│ │ ├── index.tsx
│ │ └── _app.tsx
│ ├── styles/
│ │ └── globals.css
│ └── package.json
│
├── requirements-simple.txt
├── start.sh
├── run.sh
└── README.md
```

## 🌐 API Endpoints

### Product Discovery
- `GET /api/products/` - Get all products with filtering
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/{id}/similar` - Get similar products
- `GET /api/products/{id}/score-breakdown` - Get detailed score analysis
- `POST /api/products/crawl` - Crawl for new products

### AI Tools
- `POST /api/ai/rewrite-title` - Rewrite product titles
- `POST /api/ai/write-ad-copy` - Generate Facebook ad copy
- `POST /api/ai/write-description` - Generate product descriptions
- `POST /api/ai/explain-why-winning` - Analyze product potential

## 🧠 Winning Score Formula

Each product is scored (0–100) based on weighted metrics:

| Metric                    | Weight |
|---------------------------|--------|
| Facebook Ad Engagement    | 30%    |
| TikTok Viral Ratio        | 25%    |
| Profit Margin (compare vs price) | 20% |
| Google Trends Volume      | 10%    |
| Store Saturation Level    | 15%    |

## 🧠 AI Features

| Function                      | Description                              |
|-------------------------------|------------------------------------------|
| `rewrite-title()`             | Improve product name for virality        |
| `write-ad-copy()`             | Generate engaging Facebook ad text       |
| `explain-why-winning()`       | Explain why a product is likely to win   |

All powered by OpenAI/Gemini APIs (with mock responses when no API keys configured).

## 🔧 Configuration

Edit the `.env` file to configure:

```env
# API Keys (Optional - mock responses will be used if not configured)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
PORT=8000
NODE_ENV=development

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Sample Data

The platform comes with sample product data including:
- LED Flame Speaker (Score: 82.5)
- Smart Water Bottle (Score: 78.2)

Each product includes:
- Facebook ad data
- TikTok mentions
- Supplier links and prices
- Trend analysis
- Detailed scoring breakdown

## 🚀 Development

### Backend Development
```bash
cd backend
source ../venv/bin/activate
python -m main
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### API Testing
```bash
# Test products API
curl http://localhost:8000/api/products/

# Test AI tools
curl -X POST http://localhost:8000/api/ai/rewrite-title \
  -H "Content-Type: application/json" \
  -d '{"text":"LED Flame Speaker","purpose":"title","tone":"professional"}'
```

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**🎉 Ready to discover winning dropshipping products!**

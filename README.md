# 🧠 Dropship Intelligence – All-in-One Product Research Platform

A full-stack system to discover, analyze, and predict winning dropshipping products across Shopify stores, Facebook Ads, TikTok videos, and supplier platforms like AliExpress, Temu, and 1688.

This system combines and extends the best features of Dropship.io, Minea, and PPSpy — with enhanced AI intelligence, ad analysis, store tracking, and product scoring.

---

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

---

## 🧱 Folder Structure
dropship-platform/
│
├── backend/
│ ├── api/ # All REST endpoints
│ ├── crawlers/
│ │ ├── shopify.py
│ │ ├── facebook_ads.py
│ │ └── tiktok.py
│ ├── ai/
│ │ └── writer.py
│ ├── scoring/engine.py # Winning score calculator
│ ├── matcher/supplier.py # Find product source link
│ ├── database/
│ │ └── models.py
│ ├── cron/
│ │ └── scheduler.py
│ └── main.py
│
├── frontend/
│ └── nextjs-app/ # Modern dashboard UI
│
├── data/
│ ├── rpm_by_country.json
│ └── tags_by_niche.json
│
├── .env.template
└── README.md

yaml
Copy
Edit

---

## 🌐 API Endpoints (Simplified)

### Product Discovery
GET /products
GET /products/:id
GET /products/similar/:id

shell
Copy
Edit

### Crawler Controls
POST /crawl/shopify
POST /crawl/facebook
POST /crawl/tiktok
POST /crawl/supplier

shell
Copy
Edit

### AI Tools
POST /ai/rewrite-title
POST /ai/write-ad-copy

yaml
Copy
Edit

---

## 🧠 Winning Score Formula

Each product is scored (0–100) based on weighted metrics:

| Metric                    | Weight |
|---------------------------|--------|
| Facebook Ad Engagement    | 30%    |
| TikTok Viral Ratio        | 25%    |
| Profit Margin (compare vs price) | 20% |
| Google Trends Volume      | 10%    |
| Store Saturation Level    | 15%    |

→ Stored under: `score-engine/engine.py`

---

## 🧠 AI Features

| Function                      | Description                              |
|-------------------------------|------------------------------------------|
| `rewrite-title()`             | Improve product name for virality        |
| `write-ad-copy()`             | Generate engaging Facebook ad text       |
| `explain-why-winning()`       | Explain why a product is likely to win   |

All powered by OpenAI/Gemini APIs.

---

## ⏱ Cron Jobs

| Job                         | Frequency |
|-----------------------------|-----------|
| Shopify product discovery   | Every 4h  |
| Facebook Ads scan           | Every 6h  |
| TikTok update               | Daily     |
| Supplier match & price sync | Daily     |
| Score recalculation         | Every 12h |

→ Implemented in `cron/scheduler.py`

---

## 🧪 Database Sample (MongoDB)

```json
{
  "_id": "product_1234",
  "title": "LED Flame Speaker",
  "price": 29.99,
  "compare_price": 59.99,
  "score": 82.5,
  "tags": ["gadgets", "home", "gift"],
  "facebook_ads": [...],
  "tiktok_mentions": [...],
  "supplier_links": {
    "aliexpress": "...",
    "temu": "...",
    "1688": "..."
  },
  "trend_data": {
    "keyword": "LED flame speaker",
    "google_trend": 75
  }
}

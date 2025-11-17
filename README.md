# OSINT-Based SIM Swap Fraud Detection System

A full-stack application for analyzing phone numbers to detect potential fraud indicators using **real OSINT (Open Source Intelligence)** data sources and APIs.

## ⚠️ Important: Real API Integration

This project now uses **legitimate APIs** for phone number analysis:
- **IPQualityScore** - Fraud detection, spam scoring, abuse detection
- **Numverify** - Phone validation and carrier lookup
- **Abstract API** - Alternative validation service

**The system no longer uses dummy/mock data.** All analysis results come from real API responses.

## 🚀 Quick Start

### 1. Get API Keys (Required)

**Minimum Required**: IPQualityScore API (FREE tier available)

1. **IPQualityScore** (Primary - REQUIRED)
   - Sign up: https://www.ipqualityscore.com/create-account
   - Free tier: 5,000 requests/month
   - Get API key from dashboard

2. **Numverify** (Optional but recommended)
   - Sign up: https://numverify.com/product
   - Free tier: 100 requests/month

3. **Abstract API** (Optional)
   - Sign up: https://www.abstractapi.com/phone-validation-api
   - Free tier: 250 requests/month

**See `API_SETUP_GUIDE.md` for detailed instructions.**

### 2. Configure Environment

Edit `backend/.env` and add your API keys:

```env
# Required
IPQUALITYSCORE_API_KEY=your_key_here

# Optional (but recommended)
NUMVERIFY_API_KEY=your_key_here
ABSTRACT_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///osint_fraud.db

# Flask config
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### 3. Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
```

**Frontend:**
```bash
cd frontend
npm install --legacy-peer-deps
```

### 4. Test API Configuration

```bash
cd backend
.\venv\Scripts\Activate.ps1
python test_apis.py
```

This will verify your API keys are working correctly.

### 5. Run the Application

**Backend** (Terminal 1):
```bash
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm start
```

**Access**: http://localhost:3000

## 🔍 Features

### Real OSINT Analysis
- ✅ **Fraud Score Detection** (0-100) via IPQualityScore
- ✅ **Spam Database Checking** with real spam reports
- ✅ **Carrier & Line Type Lookup** (Mobile, Landline, VOIP)
- ✅ **Recent Abuse Detection** for numbers flagged recently
- ✅ **VOIP/Prepaid Detection** for high-risk line types
- ✅ **Geographic Information** (Country, City, Region)
- ✅ **Do Not Call Registry** check
- ✅ **Risk Factor Breakdown** with severity levels

### Application Features
- 📊 Real-time phone number analysis
- 📈 Risk scoring with weighted factors
- 🗄️ Analysis history with search and filter
- 📄 Detailed fraud reports
- 🔒 Rate limiting (10 requests/hour per IP)
- ⚡ 24-hour result caching

## 🛠️ Tech Stack

**Backend:**
- Python 3.13 + Flask 3.1
- SQLAlchemy ORM + SQLite
- Real API Integrations (IPQualityScore, Numverify, Abstract)
- Flask-Limiter for rate limiting

**Frontend:**
- React 18 + Material-UI 5
- Axios for API calls
- React Router for navigation
- Recharts for data visualization

## 📖 API Documentation

### Analyze Phone Number
```bash
POST /api/analysis/analyze
Content-Type: application/json

{
  "phone_number": "+14158586273",
  "deep_scan": true
}
```

**Response includes:**
- Fraud score (0-100)
- Spam reports count
- Carrier and line type
- Risk factors with evidence
- Geographic data
- Abuse detection results

### Get Analysis Report
```bash
GET /api/analysis/report/:id
```

### View History
```bash
GET /api/analysis/history?page=1&per_page=10
```

### Search Analyses
```bash
POST /api/analysis/search
Content-Type: application/json

{
  "phone_number": "+1415",
  "risk_level": "HIGH"
}
```

### Get Statistics
```bash
GET /api/analysis/statistics
```

## 📊 API Usage & Costs

### Free Tier (Recommended for Development)
- IPQualityScore: 5,000 requests/month (FREE)
- Numverify: 100 requests/month (FREE)
- Abstract API: 250 requests/month (FREE)
- **Total**: ~5,350 free requests/month

### Paid Plans (For Production)
- IPQualityScore: $29.99/mo (25,000 requests)
- Numverify: $9.99/mo (5,000 requests)
- **Total**: ~$40/month for 30,000 requests

## 🔒 Legal & Ethical Use

⚠️ **Important Disclaimers:**

1. **Permission Required**: Only analyze phone numbers you have explicit permission to investigate
2. **Privacy Compliance**: Comply with GDPR, CCPA, and local privacy laws
3. **Legitimate Use Only**: For fraud prevention, not harassment or stalking
4. **User Consent**: Get consent before analyzing personal numbers
5. **Terms of Service**: Respect all API provider ToS and rate limits

## 🧪 Testing

Test with known numbers:
- Google Voice: `+14158586273`
- Your own number (with permission)

**Expected Results:**
- Fraud Score: 0-100 (lower is better)
- Spam Reports: Count of spam database entries
- Risk Level: LOW/MEDIUM/HIGH/CRITICAL
- Carrier: Actual carrier name
- Line Type: Mobile/Landline/VOIP

## 🐛 Troubleshooting

### "API Key Not Configured" Error
- Verify API keys are in `backend/.env`
- Restart backend server after adding keys
- Check for typos in environment variable names

### No Data Returned
- Verify API keys are valid in provider dashboards
- Check API usage limits haven't been exceeded
- Ensure phone number format is correct (+countrycode...)

### Rate Limit Exceeded
- Wait 1 hour or upgrade API plan
- Check rate limit settings in code
- Enable caching to reduce API calls

## 📁 Project Structure

```
OSINT_Project/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/
│   │   │   ├── osint_modules_real.py  # Real API integrations
│   │   │   ├── phone_analyzer.py      # Analysis orchestrator
│   │   │   └── risk_scorer.py         # Risk calculation
│   │   └── utils/           # Validators, helpers
│   ├── .env                 # API keys (DO NOT COMMIT)
│   ├── requirements.txt
│   ├── test_apis.py        # API configuration test
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── API_SETUP_GUIDE.md      # Detailed API setup instructions
└── README.md
```

## 🤝 Contributing

1. Never commit API keys
2. Test all changes with real APIs
3. Update documentation for new features
4. Follow privacy and legal guidelines

## 📞 Support

- IPQualityScore Docs: https://www.ipqualityscore.com/documentation
- Numverify Docs: https://numverify.com/documentation
- Project Issues: Create an issue in this repository

## 📄 License

This project is for educational and legitimate fraud prevention purposes only.

---

**Built with real OSINT APIs for legitimate phone number fraud detection.**

A full-stack application that identifies indicators of mobile number fraud using Open Source Intelligence (OSINT) techniques.

## 🎯 Features

- **Phone Number Analysis**: Validate and analyze mobile numbers
- **Social Media Presence**: Check number's presence across social platforms
- **Spam Database Scanning**: Integrate with spam/scam databases
- **Fraud Forum Detection**: Search for number mentions in fraud databases
- **Messaging App Investigation**: Check Telegram/WhatsApp presence
- **Risk Scoring**: AI-powered risk assessment algorithm
- **Detailed Reports**: Generate comprehensive fraud risk reports
- **Historical Tracking**: Store and track analysis history

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend│────▶│  Flask Backend  │────▶│   PostgreSQL    │
│                 │     │                 │     │    Database     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              │
                        ┌─────▼─────┐
                        │   OSINT   │
                        │  Modules  │
                        └───────────┘
```

## 📁 Project Structure

```
OSINT_Project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── database/
│   └── schema.sql
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python run.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### Database Setup

```bash
psql -U postgres -d osint_fraud_db -f database/schema.sql
```

## 🔧 Configuration

Create a `.env` file in the backend directory:

```env
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/osint_fraud_db
SECRET_KEY=your-secret-key-here
TELEGRAM_API_ID=your-telegram-api-id
TELEGRAM_API_HASH=your-telegram-api-hash
```

## 📊 OSINT Data Sources

1. **PhoneInfoga**: Phone number reconnaissance
2. **Numverify API**: Number validation
3. **Social Media APIs**: Twitter, Facebook, Instagram
4. **Telegram Bot API**: Group/channel scanning
5. **Public Spam Databases**: Whocalld, ShouldIAnswer
6. **LeakCheck**: Data breach monitoring

## 🔒 Ethical Use & Legal Disclaimer

⚠️ **IMPORTANT**: This tool is for educational and legitimate fraud prevention purposes only.

- Only use on numbers you have permission to investigate
- Respect privacy laws and regulations (GDPR, CCPA)
- Do not use for harassment or unauthorized surveillance
- Always obtain proper authorization before conducting investigations
- Comply with terms of service of all data sources

## 📈 Risk Scoring Algorithm

The system calculates risk scores based on:

- **Social Media Anomalies** (30%): Unusual activity patterns
- **Spam Reports** (25%): Number of spam/scam reports
- **Fraud Forum Mentions** (25%): Appearances in fraud discussions
- **Account Age** (10%): Recent registrations on multiple platforms
- **Geographic Anomalies** (10%): Location inconsistencies

## 🛠️ Technologies Used

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- Celery (for async tasks)
- Redis (task queue)

### Frontend
- React 18
- TypeScript
- Material-UI
- Axios
- Recharts (data visualization)

### Database
- PostgreSQL

## 📝 API Endpoints

```
POST   /api/analyze          - Submit phone number for analysis
GET    /api/report/:id       - Get analysis report
GET    /api/history          - Get analysis history
POST   /api/search           - Search previous analyses
```

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for details.

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- PhoneInfoga for number reconnaissance
- OSINT Framework community
- Open source intelligence tools

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and regulations.

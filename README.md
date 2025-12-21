# Fees & Charges Explainer Agent

AI-powered system for answering questions about HDFC mutual fund fees, charges, and taxation.

---

## ✅ What's Working

### **1. Data Pipeline**
- ✅ Selenium scraper extracts 19 HDFC funds from Groww.in
- ✅ Enhanced data extraction (returns, managers, tax info)
- ✅ Pinecone vector database (19 vectors with 16 metadata fields)
- ✅ AI agent answers fee/tax questions accurately

### **2. Test Results**
```
Q: What is the exit load for HDFC Mid Cap?
A: Exit load of 1% if redeemed within 1 year

Q: What is the expense ratio for HDFC Focused Fund?
A: Expense Ratio: 0.62%

Q: What is the taxation for HDFC ELSS?
A: STCG 20%, LTCG 12.5% (above ₹1.25 lakh)
```

---

## 📁 Project Files

### **Core Scripts**
- `scraper_complete.py` - Selenium scraper (19 HDFC funds)
- `enhance_fund_data.py` - Extract returns, managers, tax
- `upload_one_by_one.py` - Upload to Pinecone (one-by-one)
- `test_ai_agent.py` - Test queries

### **Data Files**
- `complete_fund_data.json` - Raw scraped data
- `enhanced_fund_data.json` - Enhanced with returns, managers
- `sources.csv` - List of 19 fund URLs

### **Libraries** (`lib/`)
- `scraper.py` - Scraping utilities
- `embeddings.py` - Gemini embeddings
- `vector_store.py` - Pinecone operations
- `compliance.py` - Compliance checks

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Set Environment Variables**
```bash
export GEMINI_API_KEY="your-key"
export PINECONE_API_KEY="your-key"
export PINECONE_HOST="your-host"
```

### **3. Test AI Agent**
```bash
python3 test_ai_agent.py
```

---

## 🔄 Data Pipeline

```
1. Scrape (scraper_complete.py)
   ↓ 19 HDFC funds from Groww.in
   
2. Enhance (enhance_fund_data.py)
   ↓ Extract returns, managers, tax
   
3. Upload (upload_one_by_one.py)
   ↓ 19 vectors to Pinecone
   
4. Query (test_ai_agent.py)
   ↓ AI answers with sources
```

---

## 📊 Data Coverage (19 Funds)

| Field | Coverage | Range |
|-------|----------|-------|
| Expense Ratio | 100% | 0.07% - 1.15% |
| Exit Load | 100% | Full text |
| Min SIP | 100% | ₹100 - ₹500 |
| Tax Info | 100% | STCG 20%, LTCG 12.5% |
| 3Y Returns | 95% | 4.2% - 25.8% |
| Fund Managers | 100% | 1-3 per fund |
| AUM | 100% | ₹414Cr - ₹1,07,971Cr |

---

## 🔧 Re-scrape Data

```bash
# 1. Scrape fresh data
python3 scraper_complete.py

# 2. Enhance data
python3 enhance_fund_data.py

# 3. Upload to Pinecone
python3 upload_one_by_one.py
```

---

## 💰 Cost Estimate

**For 1000 queries/month:**
- Gemini Embeddings: ~$0.01
- Gemini Generation: ~$2.00
- Pinecone (19 vectors): ~$0.10
- **Total**: ~$2.11/month

---

## 📝 Next Steps

To complete the milestone, you need to:

1. **Build N8N Workflow** (manually in N8N)
   - Use N8N Chat as trigger
   - Add compliance check (Code + HTTP to Gemini)
   - Search Pinecone (HTTP Request)
   - Generate answer (Code + HTTP to Gemini)
   - Approval gate (Wait for response)
   - MCP actions (Google Docs, Gmail, Sheets)

2. **Test End-to-End**
   - User asks question in N8N Chat
   - Agent checks compliance
   - Searches Pinecone
   - Generates answer
   - Waits for approval
   - Executes MCP actions

See artifacts for detailed N8N workflow guide.

---

**✅ Core System Working - Ready for N8N Integration**

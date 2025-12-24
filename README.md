# Fees & Charges Explainer Agent

An AI-powered agent that explains financial fees for HDFC mutual funds using only official sources. Built with n8n workflows, Gemini AI, and Pinecone vector database.

## 🚀 Try It Live

**Chat Interface**: [https://singhmanavi.app.n8n.cloud/webhook/1b7ca1b9-35ec-4227-a232-924bc41084c9/chat](https://singhmanavi.app.n8n.cloud/webhook/1b7ca1b9-35ec-4227-a232-924bc41084c9/chat)

Ask questions about HDFC mutual fund fees, charges, taxation, and more!

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [System Flow](#system-flow)
- [Workflows](#workflows)
- [Key Concepts](#key-concepts)
- [Setup & Installation](#setup--installation)
- [Data Pipeline](#data-pipeline)
- [Compliance & Safety](#compliance--safety)

---

## 🎯 Overview

This system provides a **SEBI-compliant** AI agent that:
- ✅ Explains fees/charges for 19 HDFC mutual funds
- ✅ Uses only official sources (Groww.in, AMC documents)
- ✅ Asks clarifying questions when needed
- ✅ Generates bullet-point explanations with citations
- ✅ Performs MCP actions (notes, email drafts, audit logs)
- ✅ Maintains conversation memory
- ✅ Updates data daily via automated scraping

### Supported Fee Scenarios

1. **EXIT_LOAD** - Redemption charges
2. **TAXATION** - Short-term/Long-term capital gains
3. **SIP_CHARGES** - Systematic Investment Plan fees
4. **EXPENSE_RATIO** - Total Expense Ratio
5. **LOCK_IN_PERIOD** - Lock-in periods
6. **RETURNS** - Historical returns (1Y, 3Y, 5Y)
7. **FUND_RATING** - Star ratings
8. **AUM** - Assets Under Management
9. **FUND_INFO** - General fund information
10. **NAV** - Net Asset Value

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (n8n Chat Trigger)                           │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW 1: MAIN ORCHESTRATION                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Compliance   │→ │ Intent       │→ │ Clarification│          │
│  │ Check        │  │ Extraction   │  │ Questions    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                 │
│         │                  ▼                  │                 │
│         │         ┌──────────────┐            │                 │
│         │         │ Execute      │            │                 │
│         │         │ Workflow 2   │            │                 │
│         │         └──────────────┘            │                 │
│         │                  │                  │                 │
│         │                  ▼                  │                 │
│         │         ┌──────────────┐            │                 │
│         │         │ Generate     │            │                 │
│         │         │ Answer       │            │                 │
│         │         └──────────────┘            │                 │
│         │                  │                  │                 │
│         │                  ▼                  │                 │
│         │         ┌──────────────┐            │                 │
│         │         │ Approval Gate │            │                 │
│         │         └──────────────┘            │                 │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                     │
│                  ┌──────────────┐                                │
│                  │ Execute      │                                │
│                  │ Workflow 3   │                                │
│                  └──────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW 2: PREPROCESSING                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Extract      │→ │ Generate     │→ │ Query        │          │
│  │ Parameters   │  │ Embedding    │  │ Pinecone     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                 │
│         │                  │                  ▼                 │
│         │                  │         ┌──────────────┐           │
│         │                  │         │ Filter &     │           │
│         │                  │         │ Parse        │           │
│         │                  │         └──────────────┘           │
│         │                  │                                   │
│         └──────────────────┴───────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW 3: MCP ACTIONS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Format       │→ │ Google Docs  │  │ Google      │          │
│  │ Content      │  │ (Notes)      │  │ Sheets      │          │
│  └──────────────┘  └──────────────┘  │ (Audit)     │          │
│         │                  │          └──────────────┘          │
│         │                  │                  │                 │
│         │                  │                  ▼                 │
│         │                  │         ┌──────────────┐           │
│         │                  │         │ Gmail Draft  │           │
│         │                  │         └──────────────┘           │
│         │                  │                                   │
│         └──────────────────┴───────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW 4: DAILY SCRAPING                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Schedule     │→ │ Download     │→ │ Parse Funds  │          │
│  │ (2 AM)      │  │ from GitHub  │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                 │
│         │                  │                  ▼                 │
│         │                  │         ┌──────────────┐           │
│         │                  │         │ Delete Old  │           │
│         │                  │         │ Vectors      │           │
│         │                  │         └──────────────┘           │
│         │                  │                  │                 │
│         │                  │                  ▼                 │
│         │                  │         ┌──────────────┐           │
│         │                  │         │ Loop Over    │           │
│         │                  │         │ Funds        │           │
│         │                  │         └──────────────┘           │
│         │                  │                  │                 │
│         │                  │    ┌─────────────┴─────────────┐   │
│         │                  │    │                          │   │
│         │                  │    ▼                          │   │
│         │                  │ ┌──────────────┐              │   │
│         │                  │ │ Generate     │              │   │
│         │                  │ │ Embedding    │              │   │
│         │                  │ └──────────────┘              │   │
│         │                  │    │                          │   │
│         │                  │    ▼                          │   │
│         │                  │ ┌──────────────┐              │   │
│         │                  │ │ Upload to   │              │   │
│         │                  │ │ Pinecone    │              │   │
│         │                  │ └──────────────┘              │   │
│         │                  │    │                          │   │
│         │                  │    ▼                          │   │
│         │                  │ ┌──────────────┐              │   │
│         │                  │ │ Wait (Rate   │              │   │
│         │                  │ │ Limit)       │              │   │
│         │                  │ └──────────────┘              │   │
│         │                  │    │                          │   │
│         │                  └────┴──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 System Flow

### User Query Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Compliance Check                │
│    - Check forbidden keywords      │
│    - Validate query scope          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Intent Extraction                │
│    - AI Agent analyzes query        │
│    - Extracts intent & fund name    │
│    - Determines if clarification   │
│      needed                         │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
   Needs         No Clarification
   Clarification      │
        │             │
        │             ▼
        │    ┌──────────────────────┐
        │    │ 3. Execute Workflow 2│
        │    │    - Generate        │
        │    │      embedding       │
        │    │    - Query Pinecone  │
        │    │    - Get fund data   │
        │    └──────────┬───────────┘
        │               │
        │               ▼
        │    ┌──────────────────────┐
        │    │ 4. Generate Answer   │
        │    │    - Format bullets  │
        │    │    - Add citations    │
        │    │    - Include "Last   │
        │    │      checked" date   │
        │    └──────────┬───────────┘
        │               │
        │               ▼
        │    ┌──────────────────────┐
        │    │ 5. Approval Gate     │
        │    │    - User approves   │
        │    │      MCP actions     │
        │    └──────────┬───────────┘
        │               │
        │               ▼
        │    ┌──────────────────────┐
        │    │ 6. Execute Workflow 3│
        │    │    - Save notes      │
        │    │    - Draft email     │
        │    │    - Log audit       │
        │    └──────────────────────┘
        │
        └──────────────┐
                       │
                       ▼
              Ask Clarification
              Question & Wait
```

### Data Pipeline Flow

```
GitHub Actions (Daily at 1:30 AM UTC)
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Run scraper_complete.py         │
│    - Scrape Groww.in               │
│    - Extract fund data             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Run enhance_fund_data.py         │
│    - Extract NAV, returns           │
│    - Extract fund managers         │
│    - Enhance metadata               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Commit enhanced_fund_data.json   │
│    to GitHub                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Workflow 4 (2 AM Daily)         │
│    - Download from GitHub           │
│    - Parse funds                    │
│    - Delete old vectors             │
│    - Generate embeddings            │
│    - Upload to Pinecone             │
└─────────────────────────────────────┘
```

---

## 📦 Workflows

### Workflow 1: Smart Finance Director (Main Orchestration)

**Purpose**: Central coordinator for user interactions

**Key Components**:
- **Chat Trigger**: Receives user messages
- **Compliance Check**: Validates queries against SEBI guidelines
- **AI Agent**: Extracts intent and fund name using Gemini
- **Simple Memory**: Maintains conversation context (20 messages)
- **Intent Router**: Routes to appropriate handlers
- **Answer Generator**: Creates formatted responses with citations
- **Approval Gate**: User approval before MCP actions
- **Workflow Executor**: Calls Workflow 2 and Workflow 3

**Supported Intents**:
- GREETING, FUND_LIST, GRATITUDE
- EXIT_LOAD, TAXATION, SIP_CHARGES
- EXPENSE_RATIO, LOCK_IN_PERIOD, RETURNS
- FUND_RATING, AUM, FUND_INFO, NAV

**Clarification Logic**:
- Asks for fund name if missing
- Asks for holding period for EXIT_LOAD
- Asks for tax term (short/long) for TAXATION
- Asks for time period (1Y/3Y/5Y) for RETURNS

---

### Workflow 2: Preprocessing (RAG Pipeline)

**Purpose**: Retrieve fund data from Pinecone vector store

**Flow**:
1. **Extract Input Parameters**: Parse query, intent, fund_name
2. **Generate Embedding**: Create vector embedding using Gemini text-embedding-004
3. **Query Pinecone**: Search vector database (topK=3)
4. **Filter Matches**: Remove low-quality results (score < 0.6)
5. **Parse Results**: Format fund data for answer generation

**Output Format**:
```json
{
  "success": true,
  "fund": {
    "name": "HDFC Mid Cap Fund",
    "category": "Equity - Mid Cap",
    "expense_ratio": "0.71%",
    "exit_load": "1% if redeemed within 1 year",
    "source_url": "https://groww.in/..."
  },
  "relevance": 0.95
}
```

---

### Workflow 3: MCP Actions

**Purpose**: Perform side effects after user approval

**Actions**:
1. **Format Content**: Prepare structured content for all actions
2. **Google Docs**: Append notes entry with:
   - Conversation context
   - Query history
   - Answer provided
   - Key facts with citations
   - Sources
   - Last checked date

3. **Gmail Draft**: Create email draft with:
   - HTML formatted body
   - Fund name and scenario
   - Conversation summary
   - Answer provided
   - Sources and citations

4. **Google Sheets**: Log audit entry with:
   - Session ID, User ID
   - Timestamp, Date
   - Query and query history
   - Scenario and fund name
   - Action flags (email_created, document_updated)
   - System metadata

**Approval Gate**: Only executes after explicit user approval in Workflow 1

---

### Workflow 4: Daily Scraping

**Purpose**: Scheduled daily update of Pinecone vector store

**Schedule**: Runs daily at 2:00 AM

**Flow**:
1. **Schedule Trigger**: Daily at 2 AM
2. **Delete Old Vectors**: Clear existing Pinecone vectors (with error handling)
3. **Download from GitHub**: Fetch `enhanced_fund_data.json`
4. **Parse Funds**: Transform and validate fund data
5. **Loop Over Funds**: Process each fund sequentially (batchSize=1)
   - **Generate Embedding**: Create vector using Gemini
   - **Prepare Pinecone Data**: Combine embedding with metadata
   - **Upload to Pinecone**: Store vector in database
   - **Wait (Rate Limit)**: 0.5 second delay between uploads

**Data Structure**:
- **Vector ID**: `hdfc-fund-{index}`
- **Metadata**: fund_name, category, exit_load, expense_ratio, returns, etc.
- **Namespace**: `fund-documents` (configurable)

---

## 🧠 Key Concepts

### 1. RAG (Retrieval-Augmented Generation)

The system uses RAG to provide accurate, source-backed answers:

```
User Query → Embedding → Pinecone Search → Relevant Fund Data → Answer Generation
```

**Why RAG?**
- Ensures answers are based on official sources
- Provides citations for transparency
- Updates automatically with daily scraping
- No hallucination of fees/charges

### 2. Compliance Engine

**RefusalMatrix** (`lib/compliance.py`):
- **Forbidden Keywords**: Detects comparison, advice, performance queries
- **Regulatory Messages**: SEBI-compliant refusal responses
- **Deterministic**: Rule-based, not AI-based (for compliance)

**Refusal Reasons**:
- COMPARISON: "Cannot provide comparisons between schemes"
- ADVICE: "Cannot provide investment advice"
- PERFORMANCE: "Cannot discuss historical performance"
- HYPOTHETICAL: "Cannot simulate hypothetical scenarios"
- OUT_OF_SCOPE: "Out of scope - fees & charges only"

### 3. Intent Extraction

**AI Agent** uses Gemini to extract:
- **Intent**: One of 13 supported intents
- **Fund Name**: Extracted from query (e.g., "Mid Cap" → "HDFC Mid Cap Fund")
- **Clarification Needs**: Determines if additional info needed

**Fund Name Mapping**:
- "ELSS" → "HDFC ELSS Tax Saver Fund"
- "Mid Cap" → "HDFC Mid Cap Fund"
- "Balanced" → "HDFC Balanced Advantage Fund"
- "Banking" → "HDFC Banking & Financial Services Fund"

### 4. Memory & Context

**Simple Memory** (Buffer Window):
- Maintains last 20 messages
- Enables follow-up questions
- Example: "What about expense ratio?" (no need to repeat fund name)

### 5. MCP (Model Context Protocol) Actions

**Approval-Gated Side Effects**:
- User must explicitly approve before execution
- Three actions:
  1. **Notes**: Google Docs entry
  2. **Email Draft**: Gmail draft (not auto-sent)
  3. **Audit Log**: Google Sheets entry

**Why Approval-Gated?**
- Prevents unauthorized actions
- Gives user control
- Maintains audit trail

---

## 🚀 Quick Start

**Try the live chat**: [https://singhmanavi.app.n8n.cloud/webhook/1b7ca1b9-35ec-4227-a232-924bc41084c9/chat](https://singhmanavi.app.n8n.cloud/webhook/1b7ca1b9-35ec-4227-a232-924bc41084c9/chat)

Example queries:
- "What is the exit load for HDFC Mid Cap Fund?"
- "Tell me about taxation for ELSS funds"
- "What are the SIP charges?"
- "List all HDFC funds"

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- n8n (cloud or self-hosted)
- Google Gemini API key
- Pinecone account and API key
- Google Cloud credentials (for Docs, Sheets, Gmail)

### 1. Clone Repository

```bash
git clone <repository-url>
cd fees_explainer_agent
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

**n8n Environment Variables**:
- `GEMINI_API_KEY`: Your Gemini API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_HOST`: Your Pinecone host URL

**Google Cloud Setup**:
1. Create Google Cloud project
2. Enable APIs: Google Docs, Google Sheets, Gmail
3. Create OAuth2 credentials
4. Add credentials in n8n Settings → Credentials

### 4. Import Workflows

1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Import in order:
   - `workflows/Workflow 4_ Daily Scraping.json`
   - `workflows/Workflow 2_ Preprocessing.json`
   - `workflows/Workflow 3_ MCP Actions.json`
   - `workflows/Workflow 1_ Smart Finance Director.json`

### 5. Configure Workflows

**Workflow 1**:
- Update workflow IDs for Workflow 2 and Workflow 3
- Configure Google credentials
- Set email recipient in Workflow 3

**Workflow 2**:
- Update Gemini API key
- Update Pinecone API key and host

**Workflow 3**:
- Configure Google Docs document ID
- Configure Google Sheets spreadsheet ID
- Set Gmail recipient

**Workflow 4**:
- Update GitHub raw URL (if using different repo)
- Update Pinecone namespace (if different)
- Configure Gemini API key
- Note: GitHub Actions workflow generates `enhanced_fund_data.json` in `data/` folder

### 6. Setup GitHub Actions (Optional)

The `.github/workflows/daily-scraper.yml` workflow:
- Runs daily at 1:30 AM UTC
- Scrapes fund data
- Enhances data
- Commits to repository

**Setup**:
1. Ensure `enhanced_fund_data.json` is NOT in `.gitignore`
2. GitHub Actions will automatically run daily
3. Workflow 4 downloads from GitHub at 2 AM

---

## 📊 Data Pipeline

### Scraping Scripts

**`scraper_complete.py`**:
- Uses Selenium to scrape Groww.in
- Extracts fund data (name, category, fees, etc.)
- Saves to `complete_fund_data.json`

**`enhance_fund_data.py`**:
- Processes `complete_fund_data.json`
- Extracts NAV, returns, fund managers
- Enhances metadata
- Saves to `enhanced_fund_data.json`

**`upload_one_by_one.py`**:
- Legacy script for manual Pinecone upload
- Replaced by Workflow 4 (automated)

### Data Structure

**Fund Data Schema**:
```json
{
  "fund_name": "HDFC Mid Cap Fund Direct Growth",
  "category": "Equity",
  "sub_category": "Mid Cap",
  "exit_load": "Exit load of 1% if redeemed within 1 year",
  "expense_ratio": "0.71%",
  "min_investment": {
    "sip": "100",
    "lump_sum": "5000"
  },
  "returns": {
    "1y": "28.3%",
    "3y": "28.3%",
    "5y": "26.8%"
  },
  "rating": "5",
  "aum": "92,168.85Cr",
  "risk_level": "Very High Risk",
  "page_url": "https://groww.in/mutual-funds/..."
}
```

### Vector Database

**Pinecone Configuration**:
- **Index**: `fees-explainer-2znm61p`
- **Namespace**: `fund-documents`
- **Dimensions**: 768 (Gemini text-embedding-004)
- **Metadata**: 16 fields per vector

**Vector Structure**:
```json
{
  "id": "hdfc-fund-1",
  "values": [0.123, 0.456, ...],  // 768-dimensional embedding
  "metadata": {
    "fund_name": "HDFC Mid Cap Fund",
    "category": "Equity",
    "exit_load": "1% if redeemed within 1 year",
    "expense_ratio": "0.71%",
    "page_url": "https://..."
  }
}
```

---

## 🛡 Compliance & Safety

### SEBI Compliance

**What We Do**:
- ✅ Explain fees and charges from official sources
- ✅ Provide citations for all information
- ✅ Ask clarifying questions when needed
- ✅ Maintain audit trails

**What We Don't Do**:
- ❌ Provide investment advice
- ❌ Compare funds
- ❌ Discuss performance/predictions
- ❌ Make recommendations

### Refusal Matrix

The system automatically refuses:
- Comparison queries ("better than", "vs")
- Advice requests ("should I", "recommend")
- Performance discussions ("returns", "CAGR")
- Hypothetical scenarios ("what if", "if I had")

### Data Privacy

- No PII (Personally Identifiable Information) stored
- User IDs are anonymized
- Audit logs contain only query metadata
- No personal financial data collected

---

## 📝 File Structure

```
fees_explainer_agent/
├── README.md                          # Comprehensive documentation
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── daily-scraper.yml         # GitHub Actions workflow (runs daily at 1:30 AM UTC)
│
├── workflows/                        # n8n workflow files
│   ├── Workflow 1_ Smart Finance Director.json    # Main orchestration
│   ├── Workflow 2_ Preprocessing.json             # RAG pipeline
│   ├── Workflow 3_ MCP Actions.json               # Side effects (notes, email, audit)
│   └── Workflow 4_ Daily Scraping.json            # Data pipeline
│
├── scripts/                          # Python scripts
│   ├── scraper_complete.py           # Scrapes Groww.in for fund data
│   ├── enhance_fund_data.py          # Enhances scraped data with NAV, returns, etc.
│   └── upload_one_by_one.py          # Legacy script (replaced by Workflow 4)
│
├── lib/                              # Core library modules
│   ├── compliance.py                 # SEBI compliance engine (RefusalMatrix)
│   └── domain_model.py               # Pydantic data models
│
└── data/                             # Data files (auto-generated)
    ├── complete_fund_data.json       # Raw scraped data (temporary, gitignored)
    └── enhanced_fund_data.json       # Enhanced fund data (committed to repo)
```

### Folder Organization

- **`workflows/`**: All n8n workflow JSON files for import
- **`scripts/`**: Python scripts for data scraping and processing
- **`lib/`**: Core Python modules (compliance engine, data models)
- **`data/`**: Generated data files (JSON outputs from scripts)
- **`.github/workflows/`**: GitHub Actions automation for daily scraping

---

## 🔧 Troubleshooting

### Workflow Issues

**Loop running continuously**:
- Check `batchSize` is set to 1 in "Loop Over Funds"
- Ensure "Wait (Rate Limit)" connects correctly
- Verify no duplicate data flowing back

**Embedding generation fails**:
- Check Gemini API key is valid
- Verify API quota not exceeded
- Check JSON body format

**Pinecone upload fails**:
- Verify API key and host URL
- Check namespace exists
- Ensure metadata fields are strings (Pinecone requirement)

### Data Issues

**Scraper fails**:
- Check Selenium Chrome driver is installed
- Verify Groww.in website structure hasn't changed
- Check network connectivity

**Missing fund data**:
- Verify `enhanced_fund_data.json` exists
- Check GitHub Actions workflow ran successfully
- Ensure file is committed to repository

---

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [SEBI Mutual Fund Regulations](https://www.sebi.gov.in/)

---

## 📄 License

[Add your license here]

---

## 👥 Contributors

[Add contributors here]

---

**Last Updated**: December 2024

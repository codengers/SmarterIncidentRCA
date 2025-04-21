# Smarter Incident RCA using GroqCloud + ServiceNow + ChromaDB + Streamlit

## 🛠 Features
- Real-time webhook-based RCA updates to ServiceNow
- Vector memory of past incidents with ChromaDB
- Streamlit UI for real-time incident RCA
- Bulk processing of incidents from CSV

## 🚀 Getting Started

### 1. Clone the Repo & Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up `.env`
```env
SERVICENOW_INSTANCE=dev12345
SERVICENOW_USER=admin
SERVICENOW_PASSWORD=your_password_here
```

### 3. Ingest Past Incidents into ChromaDB
```bash
python memory/ingest_csv_to_chromadb.py
```

### 4. Start the Webhook Listener
```bash
python main.py
```

### 5. Run the Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

### 6. Run Bulk RCA (optional)
```bash
python tools/bulk_rca.py
```
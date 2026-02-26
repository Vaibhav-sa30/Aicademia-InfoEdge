# 🧠 Aicademia — AI Bias Detection Tool

A full-stack web application for **detecting and mitigating algorithmic bias** in AI/ML datasets. Built as part of the Aicademia platform, which focuses on AI education, fairness, and research.

---

## 📌 What It Does

- **Bias Detection** — Upload any CSV dataset and compute fairness metrics (Mean Difference, Disparate Impact) using IBM's [AIF360](https://github.com/Trusted-AI/AIF360) library
- **Bias Mitigation** — Uses Reweighing and (optionally) Adversarial Debiasing to reduce detected bias
- **Research Paper Fetcher** — Automatically fetches AI-related academic papers (engineering, ethics, policy) from the arXiv API and stores them in MongoDB
- **RAG Pipeline** — Preprocesses research papers, generates sentence embeddings, and produces trend analyses and summaries
- **User Auth** — Registration and login with role-based access (`student`, `professional`, `business`, `admin`)

---

## 🗂️ Project Structure

```
bias_detection_tool/
├── backend/                  # Flask API server
│   ├── app.py                # Main Flask app & API routes
│   ├── models.py             # DB models + AIF360 bias functions
│   ├── fns_papers.py         # arXiv paper fetcher (async)
│   ├── requirements.txt      # Python dependencies
│   ├── templates/            # Jinja2 HTML templates
│   ├── static/               # Static assets
│   └── rag-integration/      # RAG pipeline
│       ├── preprocessing.py  # Text cleaning & embeddings
│       ├── indexing.py       # Vector indexing
│       ├── retrieval.py      # Semantic retrieval
│       ├── generation.py     # Response generation
│       └── report_generation.py # Trend analysis & summaries
├── frontend/                 # React frontend
│   └── src/
│       ├── app.js            # Main React app
│       └── components/
│           ├── BiasDetectionForm.js  # Upload form
│           └── BiasResult.js         # Results display
├── sample_datasets/          # Sample CSV datasets for testing
├── Dockerfile
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 17, Axios |
| Backend | Flask (Python), Flask-CORS, Flask-SQLAlchemy |
| Bias Engine | IBM AIF360, scikit-learn |
| Database (users) | SQLite (via SQLAlchemy) |
| Database (papers) | MongoDB (via Motor async client) |
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Paper source | arXiv API |
| Containerization | Docker |

---

## 🚀 Running the App

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- MongoDB (optional — only needed for the research paper features)

---

### 1. Clone the Repository

```bash
git clone <repo-url>
cd bias_detection_tool
```

---

### 2. Start the Backend (Flask)

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

Install Python dependencies:

```bash
pip install flask flask-cors flask-sqlalchemy pandas numpy scikit-learn aif360 motor aiohttp werkzeug
```

Start the server:

```bash
python backend/app.py
```

> **Windows tip:** If you get a *"No Python at..."* error, use the venv Python directly instead:
> ```bash
> .venv\Scripts\python.exe backend/app.py
> ```

The backend will run at **http://127.0.0.1:8000**

> **Note:** You'll see some warnings about optional AIF360 extras (`tensorflow`, `fairlearn`, `inFairness`). These are safe to ignore — the core bias detection features work without them.

---

### 3. Start the Frontend (React)

In a **separate terminal**:

```bash
cd frontend
npm install
npm start
```

The frontend will open automatically at **http://localhost:3000**

---

### 4. Use the Bias Detection Tool

1. Open **http://localhost:3000** in your browser
2. Upload a CSV dataset
3. Fill in the fields:

| Field | Description | Example |
|---|---|---|
| **Label Column** | The column representing the outcome/prediction | `label` |
| **Protected Attribute** | The sensitive demographic column | `gender`, `race`, `religion` |
| **Favorable Class** | The positive/desirable outcome value | `0` |
| **Privileged Value** | The dominant/majority group value | `male`, `white`, `christian` |

4. Click **Check Bias** — results will show:
   - **Mean Difference** — Difference in outcome rates between groups (ideal: `0`)
   - **Disparate Impact** — Ratio of outcome rates (ideal: `1.0`, below `0.8` indicates bias)

---

## 🧪 Sample Dataset

A sample dataset is included in `sample_datasets/comment category classification.csv` (198,000 rows).

Suggested field values for this dataset:

| Field | Value |
|---|---|
| Label Column | `label` |
| Protected Attribute | `gender` (or `race` or `religion`) |
| Favorable Class | `0` |
| Privileged Value | `male` (or `white` or `christian`) |

> **Note:** This dataset contains NaN values in protected attribute columns (rows where the attribute was not recorded). These rows may cause an error in AIF360 — dropping them before upload is recommended.

---

## 🐳 Running with Docker

```bash
docker build -t aicademia-bias-tool .
docker run -p 8000:8000 aicademia-bias-tool
```

---

## 📚 How Bias Detection Works

```
User uploads CSV
       ↓
Flask reads file with pandas
       ↓
AIF360 StandardDataset wraps the data
       ↓
BinaryLabelDatasetMetric computes:
  • Mean Difference  → How much outcome rates differ between groups
  • Disparate Impact → Ratio of outcome rates (80% rule threshold)
       ↓
Results displayed in the browser
```

---

## 🔑 User Roles

| Role | Dashboard |
|---|---|
| `student` | Student dashboard |
| `professional` | Professional dashboard |
| `business` | Business dashboard |
| `admin` | Admin access |

Register at `/register` and login at `/login`.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## Ideas

- add opensource SLM? for something?

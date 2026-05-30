# Customer Segmentation Analysis

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset](#dataset)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [Installation & Setup](#installation--setup)
6. [How to Run](#how-to-run)
7. [Database Schema](#database-schema)
8. [SQL Analysis](#sql-analysis)
9. [Visualizations](#visualizations)
10. [Key Findings](#key-findings)
11. [Technologies Used](#technologies-used)

---

## Project Overview

This project performs **customer segmentation analysis** on e-commerce data using Python and PostgreSQL. The goal is to identify distinct customer groups based on demographic and behavioural attributes, enabling businesses to design targeted marketing strategies and improve customer retention.
Customer segmentation divides a customer base into groups that share similar characteristics — such as age, profession, spending habits, and marital status. Understanding these groups allows companies to:

- Personalise marketing campaigns
- Improve customer satisfaction and loyalty
- Allocate resources more efficiently
- Identify high-value and at-risk customer groups

---

## Dataset

**Source:** [Kaggle — Customer Segmentation](https://www.kaggle.com/datasets/abisheksudarshan/customer-segmentation)

| File | Records | Description |
|------|---------|-------------|
| `train.csv` | 8,068 | Customers with known segment labels (A / B / C / D) |
| `test.csv` | 2,627 | Customers without segment labels |
| **Total loaded** | **8,363** | After deduplication and merging |

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `ID` | Integer | Unique customer identifier |
| `Gender` | String | Male / Female |
| `Ever_Married` | String | Yes / No — marital status |
| `Age` | Integer | Customer age in years |
| `Graduated` | String | Yes / No — university degree |
| `Profession` | String | Customer's profession |
| `Work_Experience` | Float | Years of work experience |
| `Spending_Score` | String | Low / Average / High |
| `Family_Size` | Float | Number of family members |
| `Var_1` | String | Anonymised categorical variable |
| `Segmentation` | String | Target segment: A, B, C, or D |


## Requirements

- Python 3.8+
- PostgreSQL 16
- The following Python libraries:

```
pandas
psycopg2-binary
matplotlib
seaborn
```

---

## Installation & Setup

### Step 1 — Install Python dependencies

```bash
pip install pandas psycopg2-binary matplotlib seaborn
```

### Step 2 — Install PostgreSQL (if not already installed)

```bash
brew install postgresql@16
brew services start postgresql@16
```

### Step 3 — Create a PostgreSQL user and database

```bash
psql postgres
```

Inside psql, run:

```sql
CREATE USER your_username WITH PASSWORD 'your_password';
\q
```

Back in the terminal:

```bash
psql postgres -c "CREATE DATABASE customer_segmentation OWNER your_username;"
```

### Step 4 — Update database credentials

Open each `.py` file and update the `DB_CONFIG` dictionary with your credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "customer_segmentation",
    "user": "your_username",
    "password": "your_password",
}
```

---

## How to Run

Run the scripts **in order**:

```bash
# 1. Create tables and load data into PostgreSQL
python db_setup.py

# 2. Run SQL analysis — results printed to terminal
python sql.py

# 3. Generate charts — saved to /diagramos folder
python visualizations.py
```

---

## Database Schema

Two tables are created in PostgreSQL:

### `customers`
Stores all customer records loaded from the CSV files.

```sql
CREATE TABLE customers (
    id              INTEGER PRIMARY KEY,
    gender          VARCHAR(10),
    ever_married    VARCHAR(5),
    age             INTEGER,
    graduated       VARCHAR(5),
    profession      VARCHAR(50),
    work_experience FLOAT,
    spending_score  VARCHAR(10),
    family_size     FLOAT,
    var_1           VARCHAR(20),
    segmentation    VARCHAR(5)
);
```

### `segments`
Reference table with descriptions for each segment code.

```sql
CREATE TABLE segments (
    segment_code  VARCHAR(5) PRIMARY KEY,
    segment_name  VARCHAR(50),
    description   TEXT
);
```

---

## SQL Analysis

The file `sql.py` executes **8 analytical queries**:

| # | Query | Description |
|---|-------|-------------|
| 1 | Segment distribution | Count and percentage of customers per segment |
| 2 | Demographic averages | Average age, work experience, and family size per segment |
| 3 | Spending score | Breakdown of Low / Average / High spenders per segment |
| 4 | Top professions | Most common professions in each segment |
| 5 | Gender split | Male / Female ratio per segment with percentages |
| 6 | Marital status & education | Combined marital and graduation status per segment |
| 7 | Loyalty analysis | Experienced (≥5 years) vs new customers per segment |
| 8 | Age groups | Gen Z / Millennials / Gen X / Boomers breakdown |

---

## Visualizations

The file `visualizations.py` generates **6 charts** saved to the `diagramos/` folder:

| File | Chart Type | Description |
|------|-----------|-------------|
| `klientu_pasiskirstymas.png` | Pie chart | Customer share per segment |
| `amziaus_pasiskirstymas.png` | KDE density plot | Age distribution per segment |
| `isleidziami_pinigai.png` | Grouped bar chart | Spending score per segment |
| `profesijos.png` | Horizontal bar chart | Top 5 professions per segment (2x2 grid) |
| `lyciu_pasiskirstymas.png` | Grouped bar chart | Gender split per segment |
| `amziaus_grupes.png` | Stacked bar chart | Age group breakdown per segment |

---

## Key Findings

### Segment Profiles

| Segment | Name | Size | Avg Age | Key Characteristics |
|---------|------|------|---------|---------------------|
| **A** | Premium | 24.4% | 45 yrs | Mostly artists & engineers, balanced gender, stable spenders |
| **B** | Established | 23.0% | 48 yrs | Mostly married, regular buyers, broad profession mix |
| **C** | Potential | 24.4% | 49 yrs | Oldest group, Boomers, highly educated and married |
| **D** | Budget | 28.1% | 33 yrs | Youngest, Gen Z & Millennials, mostly unmarried, low spenders |

### Notable Observations

- **Segment D is the largest** at 28.1% — mostly young, unmarried customers with low spending
- **Segment A (Premium) paradox** — despite the "premium" label, the majority spend at a Low level, suggesting income potential not yet converted to spending
- **Artist is the top profession** across all four segments
- **Loyalty is highest in Segment D** (29.2% experienced workers) — unexpected for the youngest group
- **Gender is relatively balanced** across all segments (~53-58% male)
- **Segment C has the most married and educated customers** - strong target for family-oriented products

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Main programming language |
| **PostgreSQL 16** | Relational database for storing and querying data |
| **psycopg2** | PostgreSQL adapter for Python |
| **pandas** | Data manipulation and CSV loading |
| **matplotlib** | Chart generation |
| **seaborn** | Chart styling and themes |
| **SQL** | Data aggregation, filtering, and behavioural analysis |

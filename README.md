# 🛡️ SENTINEL

### Anonymous Student Safety & Wellbeing Reporting System

**SENTINEL** is an anonymous reporting and early-warning platform designed to help educational institutions identify concerning student wellbeing and safety signals before they escalate.

Students can submit concerns **without logging in or providing their identity**, while authorized counsellors or administrators can review reports through a protected dashboard.

> **You don't have to know someone's whole story to notice that something is wrong. SENTINEL helps turn those observations into early action.**

---

## 🚀 Live Demo

🌐 **[Launch SENTINEL](https://sentinel-sulm.onrender.com)**

---

## ✨ Features

* 🔒 **Completely Anonymous Reporting**

  * No login required
  * No name collection
  * No IP address storage

* 🧠 **Intelligent Risk Detection**

  * Identifies potentially concerning language
  * Uses keyword and phrase-level analysis
  * Categorizes reports based on calculated risk

* ⚡ **Three-Level Risk Classification**

  * 🟢 **Mild** — low-level concern
  * 🟡 **Concerning** — requires attention
  * 🔴 **Urgent** — requires immediate attention

* 📊 **Counsellor Dashboard**

  * Review submitted reports
  * View risk levels
  * Monitor emerging patterns

* 📞 **Helpline Access**

  * Provides immediate access to available support resources

* 🗄️ **Local Data Storage**

  * Uses SQLite for lightweight and simple deployment

* 🌐 **Web-Based**

  * Built with Flask
  * Can be deployed online using platforms such as Render

---

## 🧩 How SENTINEL Works

```text
Student
   │
   ▼
Anonymous Report
   │
   ▼
Text Processing
   │
   ├── Keyword Detection
   │
   └── Phrase Detection
   │
   ▼
Risk Engine
   │
   ▼
Risk Score
   │
   ├── 🟢 Mild
   ├── 🟡 Concerning
   └── 🔴 Urgent
   │
   ▼
SQLite Database
   │
   ▼
Counsellor Dashboard
```

The system is designed as an **early-warning tool**, not as a replacement for professional counselling or emergency services.

---

## 🧠 Technical Approach

### Trie-Based Keyword Detection

SENTINEL uses a **Trie data structure** to efficiently search submitted text for relevant keywords.

This is particularly useful when scanning reports against a larger vocabulary of predefined terms.

The project also includes **phrase-level detection** for multi-word expressions that cannot be reliably detected using individual keyword matching alone.

### Weighted Risk Scoring

Detected signals are passed to the risk engine, where they contribute to an overall risk score.

Conceptually:

```text
Risk Score = Σ (detected signal × weight)
```

The resulting score is mapped to a risk category:

```text
Low Score       → Mild
Medium Score    → Concerning
High Score      → Urgent
```

This allows SENTINEL to prioritize reports rather than treating every report equally.

---

## 🏗️ Tech Stack

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| 🐍 Python           | Core programming language  |
| 🌐 Flask            | Web application framework  |
| 🗃️ SQLite          | Database                   |
| 🌳 Trie             | Efficient keyword matching |
| 🧮 Weighted Scoring | Risk classification        |
| 🎨 HTML / CSS       | Frontend                   |
| ☁️ Render           | Deployment                 |

---

## 📁 Project Structure

```text
sentinel/
│
├── app.py                  # Flask application and routes
├── database.py             # SQLite setup and database queries
├── trie_engine.py          # Trie-based keyword & phrase detection
├── risk_engine.py          # Risk scoring and classification
│
├── keywords.json           # Keyword dictionary
├── phrases.json            # Multi-word phrase dictionary
│
├── templates/
│   ├── index.html          # Anonymous reporting page
│   ├── dashboard.html      # Counsellor dashboard
│   └── helplines.html      # Support & helpline information
│
├── static/
│   └── style.css           # Frontend styling
│
├── requirements.txt        # Python dependencies
├── sentinel.db             # SQLite database
└── README.md               # Project documentation
```

---

## ⚙️ Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/dhyansherdiwala2604-code/sentinel.git
cd sentinel
```

### 2. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open the application

Go to:

```text
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables

For deployment, configure sensitive values through environment variables rather than hard-coding them.

Recommended variables:

```text
DASHBOARD_PASSWORD=your_secure_password
SECRET_KEY=your_secure_secret_key
```

For production deployment, use strong, unique values.

---

## 🧪 Testing the System

Try submitting reports representing different levels of concern.

### 🟢 Mild

A report describing a student who seems stressed, isolated, or unusually withdrawn.

### 🟡 Concerning

A report describing repeated worrying behaviour, significant distress, or a noticeable change in behaviour.

### 🔴 Urgent

A report indicating that someone may require immediate professional intervention.

> These examples are intended for **system testing only**. Real-world situations should be handled by appropriate trained professionals and support services.

---

## 🎯 Why SENTINEL?

Students and staff may notice warning signs long before a serious situation becomes obvious.

However, people may hesitate to report concerns because they:

* Don't know who to approach
* Don't want to reveal their identity
* Don't know whether their concern is "serious enough"
* Are worried about social consequences

SENTINEL lowers that barrier by providing a simple anonymous reporting channel.

The goal is not to diagnose students.

The goal is to **surface potentially important signals so qualified people can decide what action, if any, is appropriate.**

---

## 🛡️ Privacy by Design

Privacy is a core part of SENTINEL.

The reporting interface is designed around anonymous submissions:

* No account creation
* No student name required
* No IP address stored
* Optional contextual information
* Reports are stored without identity fields

However, **anonymity should not be confused with guaranteed anonymity in every deployment environment**. Production deployments should be configured carefully, including application logs, hosting infrastructure, database access, and administrator permissions.

---

## ⚠️ Important Disclaimer

SENTINEL is an **early-warning and reporting tool**.

It is **not a medical diagnostic system**, counselling service, or replacement for trained professionals.

Risk classification is intended to help prioritize attention and should not be treated as a definitive assessment of an individual's mental health or safety.

If someone appears to be in immediate danger, contact the appropriate emergency or professional support service rather than relying solely on SENTINEL.

---

## 🏆 Hackathon Focus

SENTINEL demonstrates the practical combination of:

* **Data Structures** — Trie-based text matching
* **Algorithms** — Keyword and phrase scanning
* **Mathematics** — Weighted risk scoring
* **Backend Development** — Flask
* **Database Management** — SQLite
* **Frontend Development** — HTML/CSS
* **Deployment** — Render
* **Privacy-Aware Design** — Anonymous reporting

---

## 🔮 Future Improvements

Potential future development includes:

* 📱 Responsive mobile-first interface
* 🔔 Real-time dashboard notifications
* 📈 Anonymous trend analytics
* 🧠 More sophisticated NLP-based classification
* 🌍 Multi-language support
* 🔐 Improved authentication and role-based access
* 🏫 Institution-specific configuration
* 📝 Audit logs for authorized administrators
* ☁️ Production-grade database infrastructure
* ♿ Improved accessibility
* 🧪 Automated unit and integration testing

---

## 👨‍💻 Built By

**Dhyan Sherdiwala**

B.Tech CSE — Data Science

Built as a student hackathon project focused on using technology to create safer and more supportive educational environments.

---

## ⭐ Project

If you find the idea interesting, consider giving the repository a ⭐ on GitHub!

**GitHub:**
https://github.com/dhyansherdiwala2604-code/sentinel

**Live Demo:**
https://sentinel-sulm.onrender.com

---

### 🛡️ SENTINEL

**Notice early. Report safely. Respond responsibly.**

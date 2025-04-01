# AI-Driven Test Automation Framework 🤖

![GitHub](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Last Updated](https://img.shields.io/badge/last%20updated-2025--04--01-brightgreen)

## 📋 Project Details
- **Submitted By**: srikrishnavansi
- **Submission Date**: 2025-04-01
- **Last Updated**: 2025-04-01 16:54:19 UTC

## 🎯 Project Overview

This project implements an AI-driven test automation framework that combines web scraping, AI-powered test case generation using Gemini, and automated Selenium script generation. The framework streamlines QA processes by automating test creation and maintenance.

### Key Features
- 🕷️ Automated web element extraction using BeautifulSoup4
- 🤖 AI-powered test case generation via Gemini & LangChain
- 📝 Automated Selenium script generation 
- 📊 Structured outputs (JSON/Excel)
- 🔄 Modular and extensible design

## 🏗️ System Architecture

```mermaid
graph TD
    A[Target Website] -->|Web Scraping| B[Task 1: Web Scraper]
    B -->|elements.json| C[Element Repository]
    C -->|UI Elements| D[Task 2: Test Case Generator]
    D -->|test_cases.xlsx| E[Test Case Repository]
    E -->|Test Cases| F[Task 3: Script Generator]
    F -->|test_scripts.xlsx| G[Selenium Scripts]
    H[Gemini AI] -->|API| D
    H -->|API| F
```

## 📑 Implementation Details

### Task 1: Web Scraping
```mermaid
sequenceDiagram
    participant W as Website
    participant S as Scraper
    participant J as elements.json
    
    S->>W: HTTP Request
    W->>S: HTML Response
    S->>S: Extract Elements
    Note right of S: Parse:<br/>- Buttons<br/>- Links<br/>- Inputs<br/>- Forms
    S->>J: Save JSON
```

**Features:**
- BeautifulSoup4 for parsing
- Dynamic content handling
- Error handling & retries
- Structured JSON output
- Element attribute extraction

### Task 2: Test Generation
```mermaid
sequenceDiagram
    participant J as elements.json
    participant G as Generator
    participant A as Gemini AI
    participant E as test_cases.xlsx
    
    J->>G: Load Elements
    G->>A: Generate Tests
    Note right of A: Process:<br/>1. Analyze Elements<br/>2. Create Scenarios<br/>3. Define Steps
    A->>G: Test Cases
    G->>E: Save Excel
```

**Features:**
- Gemini AI integration
- LangChain workflows
- Structured prompts
- Response validation
- Excel formatting

### Task 3: Script Generation
```mermaid
sequenceDiagram
    participant E as test_cases.xlsx
    participant G as Generator
    participant A as Gemini AI 
    participant S as test_scripts.xlsx
    
    E->>G: Load Tests
    G->>A: Generate Code
    Note right of A: Create:<br/>1. Page Objects<br/>2. Test Methods<br/>3. Error Handlers
    A->>G: Scripts
    G->>S: Save Excel
```

**Features:**
- Page Object Model
- Error handling
- Logging
- Cross-browser support

## 🔧 Project Structure

```
ai_testing_automation/
│
├── src/
│   ├── task1_web_scraping/
│   │   ├── __init__.py
│   │   └── scraper.py
│   ├── task2_test_generation/
│   │   ├── __init__.py
│   │   └── test_case_generator.py
│   ├── task3_script_generation/
│   │   ├── __init__.py
│   │   └── selenium_script_generator.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
│
├── output/
│   ├── elements.json
│   ├── test_cases.xlsx
│   └── test_scripts.xlsx
│
├── requirements.txt
└── README.md
```

## 🚀 Setup & Installation

1. **Clone Repository**
```bash
git clone https://github.com/srikrishnavansi/Ai_Automation.git
cd Ai_Automation
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```

## 📖 Usage Instructions

1. **Run Web Scraper**
```bash
python src/task1_web_scraping/scraper.py
```

2. **Generate Test Cases**
```bash
python src/task2_test_generation/test_case_generator.py
```

3. **Generate Scripts**
```bash
python src/task3_script_generation/selenium_script_generator.py
```

## 🎯 Challenges & Solutions

| Challenge | Solution | Implementation |
|-----------|----------|----------------|
| Dynamic Content | Wait Mechanisms | Selenium WebDriverWait |
| JSON Parsing | Error Handling | Response Validation |
| Rate Limits | Retries | Exponential Backoff |
| Response Format | Prompt Engineering | JSON Templates |
| Code Structure | Design Patterns | Modular Architecture |
| Test Coverage | AI Analysis | Scenario Generation |

## 🔄 Future Improvements

### Technical Enhancements
- [ ] Parallel Execution
- [ ] Docker Support
- [ ] CI/CD Integration
- [ ] Cross-browser Testing
- [ ] Performance Testing
- [ ] API Testing Support

### AI Enhancements
- [ ] Self-healing Tests
- [ ] Smart Prioritization
- [ ] Auto-maintenance
- [ ] Result Analysis
- [ ] Coverage Optimization

### Architecture Vision
```mermaid
graph TD
    A[Web UI] -->|API| B[Backend]
    B -->|Queue| C[Generator]
    C -->|Queue| D[Executor]
    D -->|Store| E[Results]
    E -->|Trigger| F[CI/CD]
    F -->|Run| G[Test Farm]
    G -->|Data| H[Analytics]
```

## ✅ Submission Checklist

### Required Files
- [x] Python Scripts
  - [x] scraper.py
  - [x] test_case_generator.py
  - [x] selenium_script_generator.py
  
- [x] Output Files
  - [x] elements.json
  - [x] test_cases.xlsx
  - [x] test_scripts.xlsx

### Documentation
- [x] README.md
  - [x] Overview
  - [x] Setup Guide
  - [x] Usage Steps
  - [x] Architecture
  - [x] Future Plans

### Code Quality
- [x] Type Hints
- [x] Error Handling
- [x] Logging
- [x] Comments
- [x] Tests

## 📚 Dependencies

```json
{
    "python": ">=3.8",
    "beautifulsoup4": "4.12.2",
    "requests": "2.31.0",
    "pandas": "2.1.4",
    "selenium": "4.16.0",
    "openpyxl": "3.1.2",
    "python-dotenv": "1.0.0",
    "langchain": ">=0.1.17",
    "langchain-google-genai": ">=0.0.4"
}
```

## 🤖 GenAI References

   - [GPT Link](https://chatgpt.com/share/67ec1fef-eb00-8011-a5df-fc87025ebb46) 


## 📊 Project Stats

```mermaid
pie title "Code Distribution"
    "Web Scraping" : 30
    "Test Generation" : 35
    "Script Generation" : 35
```

## 📞 Contact

- **Name**: srikrishnavansi
- **GitHub**: [srikrishnavansi](https://github.com/srikrishnavansi)
- **Submission**: 2025-04-01 16:54:19 UTC

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

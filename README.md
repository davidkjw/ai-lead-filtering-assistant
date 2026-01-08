# 🤖 AI Lead Filtering Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI-powered lead scoring and prioritization system for webinar and sales leads. Automatically categorizes leads based on response patterns and assigns priority scores for efficient follow-up.**

![Lead AI Dashboard](https://via.placeholder.com/1200x600/1E3A8A/ffffff?text=AI+Lead+Filtering+Assistant+Dashboard)

## ✨ Key Features

- **🤖 Intelligent Categorization**: Automatically classifies leads into Hot/Warm/Cold/Demo Scheduled categories
- **🎯 Priority Scoring**: AI calculates priority scores (0-100+) for each lead
- **📊 Visual Analytics**: Interactive charts and metrics for lead distribution
- **🔍 Smart Filtering**: Filter leads by category, priority score, and language
- **📥 Export Capabilities**: Export to Excel with categorized results and summaries
- **🔄 Customizable Rules**: Adjust keyword lists for your specific business needs
- **📱 Web Interface**: User-friendly Streamlit dashboard
- **⚡ Fast Processing**: Instant analysis of thousands of leads

## 🎯 Who Should Use This?

- **Sales Teams**: Prioritize follow-ups and increase conversion rates
- **Marketing Teams**: Analyze webinar/seminar lead quality
- **Business Owners**: Automate lead qualification process
- **Customer Support**: Identify high-value customers
- **Sales Managers**: Monitor team performance and lead quality

## 📦 Quick Start

### Prerequisites
- Python 3.8 or higher
- 2GB+ RAM
- Web browser (Chrome, Firefox, Edge recommended)

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/yourusername/lead-ai-priority.git
   cd lead-ai-priority

2. **Install dependencies**
   
   pip install -r requirements.txt
   
### Or install individually:

   pip install streamlit pandas numpy matplotlib seaborn openpyxl xlsxwriter

3. **Run the application**

   streamlit run lead_ai_priority.py

4. **Open your browser and go to http://localhost:8501**


## 🚀 Usage Guide

## Step 1: Prepare Your Data
Your Excel file should contain at minimum:

Name: Contact name

Remarks: Text containing lead responses

Email address (optional)

Phone number (optional)

Company Name (optional)

Language (optional, for multilingual analysis)

## Step 2: Upload Your File
Launch the app

Click "Upload Leads Excel File" in the sidebar

Select your Excel file (.xlsx or .xls)

## Step 3: Customize Keywords (Optional)
Adjust the keyword lists in the sidebar:

Hot Lead Keywords: "demo", "appointment", "scheduled"

Warm Lead Keywords: "call back", "will get back", "think about it"

Cold Lead Keywords: "no need", "not interested", "hung up"

Demo Scheduled Keywords: "demo at", "appointment at", specific days

## Step 4: Process Leads
Click "🚀 Process Leads" to start AI analysis

## Step 5: Review & Export
View categorized leads with priority scores

Filter by category or language

Export results to Excel

Download high-priority leads only

## 🔧 How It Works
Categorization Logic

def categorize_lead(remarks):
    # 1. Check for demo scheduled keywords
    if any(keyword in remarks for keyword in demo_keywords):
        return "Demo Scheduled"
    
    # 2. Check for hot lead keywords
    elif any(keyword in remarks for keyword in hot_keywords):
        return "Hot Lead"
    
    # 3. Check for warm lead keywords
    elif any(keyword in remarks for keyword in warm_keywords):
        return "Warm Lead"
    
    # 4. Check for cold lead keywords
    elif any(keyword in remarks for keyword in cold_keywords):
        return "Cold/Dead Lead"
    
    return "Needs Review"

 ## Priority Score Calculation
 Scores are calculated based on:

+100 points: Demo scheduled keywords

+80 points: Hot lead keywords

+50 points: Warm lead keywords

-100 points: Cold lead keywords

+10 points: Language match (e.g., CHI for Chinese webinars)

-20 to -30 points: Small company/freelancer indicators

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Streamlit for the amazing web framework

Pandas for data manipulation

Matplotlib for visualizations

XlsxWriter for Excel export

# 📞 Support
GitHub Issues: Report bugs or request features

Documentation: Read the docs

Email: support@example.com

Discussion: Join our community

## ⭐ If this tool helps your sales team, please give it a star on GitHub! ⭐

https://img.shields.io/github/stars/yourusername/lead-ai-priority?style=social
https://img.shields.io/github/forks/yourusername/lead-ai-priority?style=social
https://img.shields.io/github/issues/yourusername/lead-ai-priority
https://img.shields.io/badge/License-MIT-yellow.svg

# Galaxium Travels Knowledge Base

This repo contains documents about a fake company called Galaxium Travels. Those documents are used 
to showcase a variety of capabilities of different generative AI approaches.

![Galaxium Travels Logo](99_visual_assets/main_logo.png)

Welcome to **Galaxium Travels**, the premier luxury space travel experience provider (fictional). This repository contains company assets and documentation for showcasing generative AI and RAG (Retrieval-Augmented Generation) capabilities.

---

## 📁 Directory Structure

```
galaxium-travels/
├── 01_corporate/
│   └── ...
├── 02_customer_service/
│   └── ...
├── 03_hr/
│   └── ...
├── 04_marketing/
│   └── ...
├── 05_legal/
│   └── ...
├── 06_technical/
│   └── ...
├── 07_finance/
│   └── ...
├── 08_it/
│   └── ...
├── 09_emergency/
│   └── ...
├── 97_raw_markdown_files/         # Source markdown files (edit here)
│   └── ... (mirrors main folders)
├── 98_utils/                      # PDF generation scripts & utils
│   ├── batch_md_to_pdf.py
│   ├── md_to_pdf_weasy.py
│   ├── md_pdf_style.css
│   └── created_pdfs/              # Output PDFs (mirrors structure)
├── 99_visual_assets/              # Logos and visual assets
│   └── ...
└── README.md
```

---

## 📝 How to Edit and Generate PDFs

1. **Edit Markdown:**
   - Make changes in the `97_raw_markdown_files/` directory. This mirrors the main folder structure.
   - Do **not** edit PDFs directly; always update the markdown source.

2. **Install Requirements:**
   - Ensure you have Python 3.7+.
   - Install dependencies:
     ```bash
     pip install -r 98_utils/requirements.txt
     ```

3. **Generate PDFs:**
   - Run the batch script from the project root:
     ```bash
     python 98_utils/batch_md_to_pdf.py
     ```
   - This will convert all markdown files (except those in the ignore list) to PDFs, placing them in `98_utils/created_pdfs/` with a mirrored folder structure.

4. **Styling & Assets:**
   - PDFs use `98_utils/md_pdf_style.css` for consistent branding.
   - Logos from `99_visual_assets/` are embedded in the PDFs automatically.

---

## 📚 Asset Categories

- **Corporate Documents:** Policies, mission, strategy
- **Marketing Materials:** Brochures, packages, partnerships
- **Technical Documentation:** Spacecraft specs, research
- **Customer Service:** QA, manuals
- **HR:** Training, handbooks
- **Legal, Finance, IT, Emergency:** Terms, budgets, plans

---

## 💡 Usage

This repository is a comprehensive knowledge base for Galaxium Travels, supporting:
- Generative AI and RAG demonstrations
- Company documentation and training
- Marketing and technical reference
- Customer service resources

---

## 🛠️ Utilities

- **batch_md_to_pdf.py:** Batch converts markdown to PDF using WeasyPrint.
- **md_to_pdf_weasy.py:** Core script for single-file conversion (used by batch script).
- **md_pdf_style.css:** Custom CSS for PDF output.

---

## 🖼️ Visual Assets

- Logos and branding images are in `99_visual_assets/` and are automatically included in generated PDFs.

---

## Note

This is a fictional company and the documents are for demonstration purposes only.



## Company Structure

- **Corporate Documents**: Company policies, mission statements, and strategic documents
- **Marketing Materials**: Brochures, press releases, and promotional content
- **Technical Documentation**: Spacecraft specifications, safety protocols, and operational procedures
- **Customer Resources**: Travel guides, FAQs, and booking information
- **Research & Development**: Innovation initiatives and future travel concepts
- **Employee Resources**: Training materials, internal policies, and organizational structure

## Asset Categories

### 1. Corporate Documents
- Company history and vision
- Annual reports
- Strategic planning documents
- Corporate policies
- Board meeting minutes
- Investor relations materials

### 2. Marketing & Sales
- Destination brochures
- Pricing packages
- Press releases
- Social media content
- Customer testimonials
- Partnership agreements
- Marketing campaigns

### 3. Technical Documentation
- Spacecraft specifications
- Safety protocols
- Maintenance procedures
- Training manuals
- Emergency response plans
- Quality assurance documents

### 4. Customer Experience
- Travel itineraries
- Pre-flight preparation guides
- In-flight services documentation
- Post-travel feedback forms
- Loyalty program details
- Booking procedures

### 5. Research & Development
- New destination proposals
- Technology innovation reports
- Environmental impact studies
- Market research
- Competitive analysis
- Future travel concepts

### 6. Human Resources
- Employee handbooks
- Training materials
- Organizational charts
- Job descriptions
- Performance review templates
- Internal communications

## Usage

This repository serves as a comprehensive knowledge base for Galaxium Travels. Each directory contains specific types of documents and resources that can be used for various purposes, including:

- AI and RAG demonstrations
- Company documentation
- Training materials
- Marketing content
- Technical reference
- Customer service resources

## Directory Structure

```
galaxium-travels/
├── corporate/
├── marketing/
├── technical/
├── customer/
├── research/
└── hr/
``` 

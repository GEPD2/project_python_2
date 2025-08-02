# MediSearch 🔍💊

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Kivy](https://img.shields.io/badge/Kivy-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A smart medicine search application that combines text and image recognition to provide drug information from [galinos.gr](https://www.galinos.gr).

## Features ✨

- **Multiple Search Methods**:
  - Text search by medicine name
  - Camera capture with text recognition
  - Photo upload from device
- **Information Retrieval**:
  - Detailed medicine descriptions
  - Usage instructions
  - Side effects
- **Image Processing**:
  - Background removal
  - Text extraction (OCR)
- **User-Friendly Interface**:
  - Simple navigation between screens
  - Local photo storage
  - Responsive design

## Installation 📦

### Prerequisites
```bash
pip install kivy requests beautifulsoup4 rembg easyocr matplotlib pillow AppOpener IPython
```
Run the Application

```bash
python medicine_search.py
```
## Technology Stack 🛠️

### Core Components

```mermaid
graph LR
    A[User Interface] --> B[Kivy]
    C[Web Scraping] --> D[Requests]
    C --> E[BeautifulSoup]
    F[Image Processing] --> G[Rembg]
    F --> H[EasyOCR]
    B --> I[Application]
    C --> I
    F --> I
```
| Icon       | Library                                                                       | Purpose	                          | Version        |  Docs   |
|------------|-------------------------------------------------------------------------------|------------------------------------|----------------|---------|
|<img src="https://kivy.org/logos/kivy-logo-black-64.png" width="40">                        |	Kivy	Cross-platform GUI framework|	≥ 2.0	         |📚 Docs  |
<img src="https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png" width="40">|	Requests	HTTP requests handling	| 2.28+	         |📚 Docs  |
<img src="https://www.crummy.com/software/BeautifulSoup/bs4/doc/_static/bs4.png" width="40"> |	BeautifulSoup	HTML/XML parsing	  | 4.11+	         |📚 Docs  |
<img src="https://github.com/danielgatis/rembg/raw/main/docs/icon.png" width="40">	         |  Rembg	Background removal	        | 2.0+	         |📚 Docs  |
<img src="https://github.com/JaidedAI/EasyOCR/raw/master/examples/logo.png" width="40">	     |  EasyOCR	Text recognition	        | 1.6+	         |📚 Docs  |

## 📊 Technology Distribution

```mermaid
pie showData
    title Feature Weighting
    "GUI Framework" : 35
    "Web Scraping" : 25 
    "Image Processing" : 30
    "Text Recognition" : 10
```

**Legend**:
- GUI: Kivy implementation
- Web: Requests + BeautifulSoup
- Imaging: Rembg pipeline
- OCR: EasyOCR integration

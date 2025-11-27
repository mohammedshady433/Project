import streamlit as st
import subprocess as sp

st.title("QANDA")
import streamlit as st

st.title("🧬 Transcriptomics Analysis Automation Tool")
st.markdown("""
Welcome to the **QANDA**, a Streamlit-based platform designed to automate and simplify the complete RNA-Seq analysis workflow.  
This tool allows you to process raw FASTQ files all the way to functional interpretation, without requiring command-line experience.

---

## 📌 **Overview**
This application integrates essential steps in transcriptomics analysis and provides an easy-to-use interface suitable for students, researchers, and bioinformatics practitioners.

---

## 🔍 **Workflow Steps**

### **1. Quality Control**
- Upload FASTQ or FASTQ.GZ files  
- Run FastQC automatically  
- View quality metrics: per-base quality, GC content, adapter sequences, etc.  

### **2. Alignment**
- Align reads to a reference genome using **HISAT2**  
- Supports both single-end and paired-end reads  
- Generates SAM/BAM files for downstream analysis  

### **3. Normalization & Quantification**
- Compute expression levels using:
  - TPM  
  - RPKM  
  - TRM  
- Produces clean count matrices for DE analysis  

### **4. Differential Expression Analysis**
- Perform DE analysis using:
  - **DESeq2**
  - **edgeR**
- Identify significantly up/down-regulated genes  
- Visualizations include:
  - Volcano plots  
  - PCA  
  - Heatmaps  

### **5. Annotation & Functional Analysis**
- Annotate genes with GO terms and KEGG pathways  
- Perform enrichment analysis  
- Generate interactive visual summaries  

---

## 🎯 **Key Features**
- Clean and interactive GUI powered by Streamlit  
- Automates complex bioinformatics workflows  
- Handles FASTQ → counts → DE → functional interpretation  
- Exportable results and visualizations  
- Beginner-friendly, research-grade performance  

---

## 🚀 **Getting Started**
Use the sidebar to navigate between different sections of the pipeline:
- **Upload FASTQ Files**
- **Quality Control**
- **Alignment**
- **Normalization**
- **Differential Expression**
- **Visualization & Annotation**

---

If you need help at any point, feel free to check each page's instructions or ask the tool for guidance.
""")

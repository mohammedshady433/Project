import streamlit as st
import gzip
import os 
import subprocess

st.title("Upload FASTQ File")

uploaded_file = st.file_uploader("Upload FASTQ or FASTQ.GZ file", 
                                type=["fastq", "fq", "fastq.gz", "fq.gz"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Example: read first few lines
    st.write("Preview of the file:")
    try:
        if uploaded_file.name.endswith(".gz"):
            with gzip.open(uploaded_file, "rt") as f:
                lines = [next(f) for _ in range(8)]
        else:
            lines = [next(uploaded_file) for _ in range(8)]
            lines = [l.decode() for l in lines]  # convert bytes → string

        st.code("".join(lines))
    except Exception as e:
        st.error(f"Error reading file: {e}")

    # Save uploaded file to disk for FastQC processing
    save_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to {save_path}")
    # Run FastQC
    st.info("Running FastQC...")
    try:
        result = subprocess.run(["fastqc", save_path, "-o", "uploads"], 
                                capture_output=True, text=True)
        if result.returncode == 0:
            st.success("FastQC completed successfully!")
            st.write("FastQC output files are saved in the 'uploads' directory.")
        else:
            st.error(f"FastQC failed:\n{result.stderr}")
    except Exception as e:
        st.error(f"Error running FastQC: {e}")
        
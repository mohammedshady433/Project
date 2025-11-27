import streamlit as st
import gzip
import os 
import subprocess
import streamlit.components.v1 as components
import glob
import cutadapt

def quality_fastqc(uploaded_file):
    # Save uploaded file to disk for FastQC processing
    save_path = os.path.join("viewer_uploads", uploaded_file.name)
    os.makedirs("viewer_uploads", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to {save_path}")
    # Run FastQC
    st.info("Running FastQC...")
    try:
        fastqc_dir = r"C:\\Program Files\\FastQC"
        fastqc_path = os.path.join(fastqc_dir, "fastqc.bat")

        save_path = os.path.abspath(save_path)
        output_dir = os.path.abspath("viewer_uploads")
        result = subprocess.run(
            [
                fastqc_path,
                save_path,
                "--outdir",
                output_dir
            ],
            capture_output=True,
            text=True,
            cwd=fastqc_dir
        )

        #Display FastQC html report
        html_report = glob.glob(os.path.join("viewer_uploads", "*.html"))[0]
        with open(html_report, "r") as f:
            html_content = f.read()
        components.html(html_content, height=1000, scrolling=True)


        st.success("FastQC completed successfully!")
        st.write("FastQC output files are saved in the 'uploads' directory.")
    except Exception as e:
        st.error(f"Error running FastQC: {e}")
#--------------------------------------------------------------------------------------------------------

st.title("Upload FASTQ File")

uploaded_file = st.file_uploader("Upload FASTQ or FASTQ.GZ file", 
                                type=["fastq", "fq", "fastq.gz", "fq.gz"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    
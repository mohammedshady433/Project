import streamlit as st
import gzip
import os 
import subprocess
import streamlit.components.v1 as components
import glob
import cutadapt

def quality_fastqc(uploaded_file):
    # Save uploaded file to disk for FastQC processing
    save_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to {save_path}")
    # Run FastQC
    st.info("Running FastQC...")
    try:
        fastqc_dir = r"C:\\Program Files\\FastQC"
        fastqc_path = os.path.join(fastqc_dir, "fastqc.bat")

        save_path = os.path.abspath(save_path)
        output_dir = os.path.abspath("uploads")
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
        html_report = glob.glob(os.path.join("uploads", "*.html"))[0]
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
        fastqc_dir = r"C:\\Program Files\\FastQC"
        fastqc_path = os.path.join(fastqc_dir, "fastqc.bat")

        save_path = os.path.abspath(save_path)
        output_dir = os.path.abspath("uploads")
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
        html_report = glob.glob(os.path.join("uploads", "*.html"))[0]
        with open(html_report, "r") as f:
            html_content = f.read()
        components.html(html_content, height=1000, scrolling=True)


        st.success("FastQC completed successfully!")
        st.write("FastQC output files are saved in the 'uploads' directory.")
    except Exception as e:
        st.error(f"Error running FastQC: {e}")


#--------------------------------------------------------------------------------------------------------
    # Trimming and Filtering
    st.write("Trimming and filtering")
    #--------------------------------------------------------------------------------------------------------
    seq = st.text_input("Enter adapter sequence to trim (optional):", key="adapter_seq")
    check1 = st.button("Trim adapter sequence")

    if seq.strip() == "":
        st.warning("No adapter sequence provided!")
    else:
        st.info(f"Trimming adapter sequence: {seq}")
        # with cutadapt
        output_trimmed = os.path.join("trimmed_output", f"filtered_{uploaded_file.name}")
        cmd = [
            "cutadapt",
            "-a", seq,
            "-o", output_trimmed,
            save_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        #print cmd respond message
        st.chat_message("user").write(f"Executed command result: {' '.join(result.stdout.splitlines())}")
        st.success(f"Adapter trimmed file saved as {output_trimmed}")
#--------------------------------------------------------------------------------------------------------
    end_trim_count = st.number_input("Enter number of bases to trim from each end (optional):", min_value=0, max_value=100)
    check2 = st.button("Trim")

    if end_trim_count == 0:
        st.warning("Please enter number of bases to trim from end")
    else:
        st.info(f"Trimming {end_trim_count} bases from end")
        # Example: using cutadapt for end trimming
        output_trimmed_end = os.path.join("trimmed_output", f"filtered_{uploaded_file.name}")
        cmd = [
            "cutadapt",
            f"-u -{end_trim_count}",  # remove from end
            "-o", output_trimmed_end,
            save_path
        ]
        result2 = subprocess.run(cmd, capture_output=True, text=True)
        st.chat_message("user").write(f"Executed command result: {' '.join(result2.stdout.splitlines())}")
        st.success(f"End-trimmed file saved as {output_trimmed_end}")
        
#---------------------------------------------------------------------------------------------------------    
    start_trim_count = st.number_input("Enter number of bases to trim from start (optional):", min_value=0, max_value=100)
    check3 = st.button("Trim from start")

    if start_trim_count == 0:
        st.warning("Please enter number of bases to trim from start")
    else:
        st.info(f"Trimming {start_trim_count} bases from start")
        output_trimmed_start = os.path.join("trimmed_output", f"filtered_{uploaded_file.name}")
        cmd = [
            "cutadapt",
            f"-u {start_trim_count}",  # remove from start
            "-o", output_trimmed_start,
            save_path
        ]
        result3 = subprocess.run(cmd, capture_output=True, text=True)
        st.chat_message("user").write(f"Executed command result: {' '.join(result3.stdout.splitlines())}")
        st.success(f"Start-trimmed file saved as {output_trimmed_start}")

#--------------------------------------------------------------------------------------------------------

    quality_threshold = st.number_input("Enter quality threshold (Phred score)(optional):", min_value=0, max_value=40)
    check4 = st.button("Trim and Filter Reads")
    if check4:
        if quality_threshold == 0:
            st.warning("Please enter a quality threshold")
        else:
            st.info(f"Trimming and filtering reads with quality threshold >= {quality_threshold}")
            output_filtered = os.path.join("trimmed_output", f"filtered_{uploaded_file.name}")
            cmd = [
                "cutadapt",
                f"-q {quality_threshold}",
                "-o", output_filtered,
                save_path
            ]
            result4 = subprocess.run(cmd, capture_output=True, text=True)
            st.chat_message("user").write(f"Executed command result: {' '.join(result4.stdout.splitlines())}")
            st.success(f"Trimmed and filtered file saved as {output_filtered}")
#--------------------------------------------------------------------------------------------------------
    # Run FastQC on trimmed/filtered file
    st.info("you could check you results by uploading the trimmed/filtered file again to run FastQC Viewer")
else:
    st.info("Please upload a FASTQ or FASTQ.GZ file to proceed.")
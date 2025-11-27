import streamlit as st
import subprocess
import os

# ----------------------------
# Step 1: Page Title
# ----------------------------
st.title("RNA-Seq Alignment with HISAT2")

# ----------------------------
# Step 2: Upload trimmed FASTQ file
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload your trimmed FASTQ file (from QC/Trimming page)", 
    type=["fastq","fq","fastq.gz","fq.gz"]
)

# ----------------------------
# Step 3: Input HISAT2 genome index
# ----------------------------
hisat2_index = st.text_input(
    "Enter HISAT2 genome index prefix (path to index files)",
    help="Example: C:\\tools\\hisat2\\genomes\\GRCh38\\GRCh38"
)

# ----------------------------
# Step 4: Choose output format
# ----------------------------
output_format = st.radio(
    "Select output format",
    options=("SAM","BAM"),
    help="SAM = uncompressed alignment; BAM = compressed alignment"
)

# ----------------------------
# Step 5: Run Alignment Button
# ----------------------------
if st.button("Run Alignment"):

    # Validate inputs
    if uploaded_file is None:
        st.warning("Please upload a FASTQ file before running alignment.")
    elif not hisat2_index:
        st.warning("Please provide the HISAT2 genome index path.")
    else:
        # ----------------------------
        # Step 6: Save uploaded FASTQ file
        # ----------------------------
        os.makedirs("alignment_output", exist_ok=True)
        input_path = os.path.join("alignment_output", uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"FASTQ file saved: {input_path}")

        # ----------------------------
        # Step 7: Run HISAT2 alignment
        # ----------------------------
        base_name = os.path.splitext(uploaded_file.name)[0]
        output_sam = os.path.join("alignment_output", f"{base_name}.sam")

        st.info("Running HISAT2 alignment... This may take some time.")

        try:

            hisat2_path = r"C:\Program Files\hisat2.1\hisat2-align-l.exe"

            # Build HISAT2 command
            cmd = [
                hisat2_path,
                "-x", hisat2_index,     # genome index prefix
                "-U", input_path,       # input FASTQ
                "-S", output_sam        # output SAM file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Display HISAT2 log
            st.subheader("HISAT2 Log")
            st.code(result.stdout + "\n" + result.stderr)

            st.success(f"Alignment completed! SAM file saved at: {output_sam}")

            # ----------------------------
            # Step 8: Convert SAM → BAM (if selected)
            # ----------------------------
            samtools_path = r"C:\Program Files\samtools-1.22.1\samtools.exe"
            if output_format == "BAM":
                output_bam = os.path.join("alignment_output", f"{base_name}.bam")
                cmd_bam = [samtools_path, "view", "-bS", output_sam, "-o", output_bam]
                subprocess.run(cmd_bam)
                st.success(f"BAM file created: {output_bam}")

        except Exception as e:
            st.error(f"Error during alignment: {e}")

# ----------------------------
# Step 9: Inform user about next steps
# ----------------------------
st.info(
    """
    After alignment, you can use the BAM file for:
    - Counting reads per gene (for expression analysis)
    - Normalization (RPKM/TPM)
    - Differential expression analysis (DESeq2/EdgeR)
    """
)

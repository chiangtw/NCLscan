# NCLscan

Accurate detection of non-co-linear (NCL) transcripts (fusion, trans-splicing, circRNA) from paired-end RNA-seq




## Overview

NCLscan is a command-line pipeline for detecting **non-co-linear (NCL) transcripts** from paired-end RNA-seq data. NCL events include gene fusions, trans-splicing events and circular RNAs, where the exon order in the transcript does not follow the linear genomic order. The method was originally introduced in the context of human RNA-seq analysis to distinguish different types of NCL transcripts based on poly(A)+ and non-poly(A) RNA-seq data.

The core pipeline combines multiple mapping and filtering stages to remove reads that can be explained by canonical co-linear splicing, and then search for candidate NCL junctions. In the original NCLscan paper, the method was reported to achieve high precision while maintaining a good balance between sensitivity and precision for both **intragenic** and **intergenic** events.

NCLscan has been updated to support modern Python 3 environments and a simplified command-line front end, while keeping the original algorithm and workflow:

- `NCLscan index` — build and cache the required references and indices  
- `NCLscan run` — execute the NCLscan pipeline on paired-end RNA-seq FASTQ files  

Reference FASTA/GTF files are supplied by the user (for example, from GENCODE), and we recommend managing external dependencies via a dedicated conda/mamba environment.




## Installation

### Prerequisites

NCLscan is intended to run on 64-bit Linux systems.

Before building NCLscan, please make sure you have:

- **Python**: Python 3 (for example 3.9–3.11)
- **Build tools**: a C/C++ compiler (e.g. `gcc`/`g++`) and `make`
- **External command-line tools** available on your `PATH`:
  - `bedtools`
  - `samtools`
  - `bwa`
  - `blat`
  - `novoalign` and `novoindex` (plus a valid Novoalign license file)

These external tools are not bundled with NCLscan and must be installed separately, either via your preferred package manager or by following the installation instructions on each tool’s official website.

### Create a conda environment (recommended)

We recommend using a dedicated conda environment to manage NCLscan and its dependencies. In practice, you can use either the original `conda` command or `mamba` (a faster drop-in replacement). The example below uses `mamba`, but you can simply replace `mamba` with `conda` if you prefer.

Most required tools are available via the `conda-forge` and `bioconda` channels:

```bash
mamba create -n nclscan-env -c conda-forge -c bioconda \
  python bedtools samtools bwa novoalign blat

mamba activate nclscan-env
```

You are still responsible for ensuring that Novoalign is properly licensed on your system. If you installed Novoalign from `bioconda`, you can register your license file (for example `novoalign.lic`) using:

```bash
novoalign-license-register novoalign.lic
```

Please refer to the Novoalign documentation for details about obtaining and managing license files.

### Build and install NCLscan

With the `nclscan-env` environment active, build and install NCLscan:

```bash
# make sure the nclscan-env mamba environment from the previous step is active:
#   mamba activate nclscan-env

# obtain the source code
git clone https://github.com/TreesLab/NCLscan.git
cd NCLscan

# compile helper binaries in bin/
make

# install scripts and binaries into the current environment
make install

```

If you prefer to install into a different location, you can override the prefix, for example:

```bash
make install PREFIX=/usr/local/bin
```

After installation, you should be able to run:

```bash
NCLscan --help
NCLscan index --help
NCLscan run --help
```




## Quick Start

This section assumes that NCLscan has been installed and that you are working inside the `nclscan-env` mamba environment described above.

### 1. Prepare reference files

NCLscan requires four reference files for a given genome build:

- reference genome FASTA
- gene annotation GTF
- protein-coding transcript FASTA
- lncRNA transcript FASTA

These files are **not** bundled with NCLscan. You need to download and prepare them yourself (for example from GENCODE), making sure they are all based on the same genome assembly.

### 2. Build the NCLscan index

Use `NCLscan index` to create the reference configuration and index files:

```bash
NCLscan index \
  -r /path/to/NCLscan_ref \
  -g /path/to/genome.fa \
  -a /path/to/annotation.gtf \
  -c /path/to/pc_transcripts.fa \
  -l /path/to/lncRNA_transcripts.fa
```

Here:

- `-r / --ref_dir` is a directory where NCLscan will write `refs.cfg` and all derived index files. The directory will be created if it does not exist.
- `-g / --genome` is the reference genome FASTA.
- `-a / --gtf` is the gene annotation GTF.
- `-c / --pc_transcripts` is the protein-coding transcript FASTA.
- `-l / --lnc_transcripts` is the lncRNA transcript FASTA.

You only need to build the index once for a given set of references. The same `REF_DIR` can then be reused for multiple RNA-seq samples.

### 3. Run NCLscan on a sample

Once the index has been created, you can run the NCLscan pipeline on paired-end RNA-seq FASTQ files:

```bash
NCLscan run \
  -r /path/to/NCLscan_ref \
  -1 sample_R1.fastq.gz \
  -2 sample_R2.fastq.gz \
  -P SampleName \
  -o /path/to/output_dir \
  -t 8
```

Key options:

- `-r / --ref_dir`
  The same reference directory that was used with `NCLscan index`.

- `-1` and `-2`
  Paired-end FASTQ files (plain `.fastq` or gzipped `.fastq.gz` are both supported).

- `-P / --name_prefix`
  A short sample name that will be used as the prefix of the output files (e.g. `SampleName.result`).

- `-o / --out_dir`
  Directory where all output and intermediate files will be written. It will be created if it does not exist.

- `-t / --threads` (optional, default: `1`)
  Number of threads/processes to use. You can give a single integer (as in the example above) or a more detailed setting such as `bwa=10,blat=4`.

Additional parameters (such as `--max_read_len`, `--max_fragment_size`, `--quality_score` and `--span_range`) have sensible defaults and can usually be left unchanged for a first run. For details, see `NCLscan run --help`.

### 4. Output overview

The output directory will contain a number of intermediate files produced by the different stages of the pipeline. In typical use, users only need to look at the following main result files (assuming `-P SampleName`):

- `SampleName.result`  
  Tab-delimited table of detected NCL events (one row per event). This is the primary output for downstream analysis.  
  The file does not contain a header line. Each row has 12 columns:

  (1) Chromosome of the donor side (5′ splice site)  
  (2) Junction coordinate of the donor side  
  (3) Strand of the donor side (`+` or `-`)  
  (4) Chromosome of the acceptor side (3′ splice site)  
  (5) Junction coordinate of the acceptor side  
  (6) Strand of the acceptor side (`+` or `-`)  
  (7) Gene name(s) on the donor side  
  (8) Gene name(s) on the acceptor side  
  (9) Intragenic/intergenic flag (`1` = intragenic, `0` = intergenic)  
  (10) Total number of supporting reads  
  (11) Number of junction reads  
  (12) Number of span reads

- `SampleName.result.sam`
  SAM file with the final alignments of reads supporting the reported NCL events. This file is mainly useful for inspection, visualization or debugging, and is not required for most downstream analyses.

- `SampleName.result.readthrough`
  NCL events classified as potential readthrough transcription.

For a detailed description of the method, please refer to the original NCLscan paper.




## Test dataset

A small test RNA-seq dataset (`simu_5X_100PE`) is available for quickly checking that NCLscan has been installed and configured correctly. It can be downloaded from:

https://treeslab1.genomics.sinica.edu.tw/NCLscan/test.tar.gz





## Legacy / advanced interface

For backward compatibility, NCLscan also keeps the original configuration-based interface. Existing workflows that call `NCLscan.py` directly (using an explicit configuration file) can still be used.

The new `NCLscan run` command is a thin wrapper around `NCLscan.py`: it generates a temporary configuration based on `refs.cfg` and the command-line options, and then runs the original pipeline internally.

The legacy usage and options are documented in `README.legacy.md`. New users are encouraged to use the simplified `NCLscan index` / `NCLscan run` interface described above.




## Citation

If you use NCLscan in your research, please cite:

Trees-Juen Chuang\*, Chan-Shuo Wu, Chia-Ying Chen, Li-Yang Hung, Tai-Wei Chiang. (2016)  
**NCLscan: accurate identification of non-co-linear transcripts (fusion, trans-splicing and circular RNA) with a good balance between sensitivity and precision.**  
*Nucleic Acids Research*, 44(3), e29. https://doi.org/10.1093/nar/gkv1013



## License

NCLscan is distributed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.











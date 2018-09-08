Finemapping molecular traits (prelim)
=====================================

Finemapping pipeline for molecular traits

### Usage

```
# Install dependencies into isolated environment
conda env create -n finemapping_mt --file environment.yaml

# Activate environment
source activate finemapping_mt

# Alter configuration file
nano configs/config.yaml

# Execute workflow (locally)
snakemake -p define_loci
snakemake -p finemap_loci

# Execute workflow (on Sanger farm)
bsub < bsub_wrapper.sh
```

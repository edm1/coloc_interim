Colocalisation (interim solution)
=====================================

Interim solution for colocalisation

### Usage

```
# Execute workflow (locally)
bash master

# Copy to gcs (dry-run)
gsutil -m rsync -rn output gs://genetics-portal-staging/coloc_interim/180911

```

### Columns

```
study_id (str)
variant_id (str)
source_id (str)
tissue_code (str)
tissue_name (str)
biomarker (str)
ensembl_id (str)
n_variants (int) = Number of overlapping variants used in the analysis
pp_h0 (float) = Posterior probability (PP) that neither trait is associated
pp_h1 (float) = PP that only trait 1 is associated
pp_h2 (float) = PP that only trait 2 is associated
pp_h3 (float) = PP that only both are associated but don't colocalise
pp_h4 (float) = PP that only both are associated and colocalise
pp_h4_over_h3_log2 (float) = log2(pp_h4/pp_h3) [Log-likelihood of colocisation over no colocalisation]
```

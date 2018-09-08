Colocalisation (interim solution)
=====================================

Interim solution for colocalisation

### Usage

```
# Install dependencies into isolated environment
conda env create -n coloc --file environment.yaml

# Activate environment
source activate coloc

# Alter configuration file
nano configs/config.yaml

# Execute workflow (locally)
bash 1_get_input_data.sh
python 2_make_commands.py

```

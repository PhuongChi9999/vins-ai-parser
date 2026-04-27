# Quick start
## Install with requirements.txt
```terminal
pip install -r requirements.txt
```

### Run Part 1
To run parser (part 1)
```terminal
python dataset.py
```
### Run Part 2
To run cleaner (part 2)
```terminal
python clean.py
```

### Run Part 2
To run cleaner (part 2)
```terminal
python learn.py
```

## Install dependencies with UV
- `uv` - python package manager
- `make` - build tool (might be preinstalled on most systems)
- `python-3.14` - programming language

## Run the project
Firstly create `venv` and install deps.
```terminal
uv venv && uv install
```

To run the project. Parser + Cleaner
```terminal
make 
```

To generate the dataset (Part 1)
```
make dataset
```

To clean the `vins.csv` file, you will receive `vins_cleaned.csv` as result (Part 2)  
```
make clean
```

To learn the `vins_cleaned.csv` file (Part 3)  
```
make learn
```

## Tests (works only when you are using UV)
`make test` - run tests (only for BL functions)  
`make test NAME=<file-name>` - run tests for a specific file

## Rapport
Une analyse détaillée des résultats (modèles, scores, conclusions) est disponible dans [report.md](report.md).

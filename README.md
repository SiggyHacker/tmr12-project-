# TMR12 – Data analytics for marine systems: course project

Shared repo for Magnus and Martin's TMR12 project work, analysing AIS data for the Nordic Pearl / Nordic Crown (2025).

## Structure

```
data/        # local only, not in git (see below)
notebooks/   # Jupyter notebooks
src/         # reusable Python code
figures/     # plots for the report
```

## Data

The AIS file (`ais_221026-ramleh.csv`, ~609 MB) is too large for GitHub and is ignored by `.gitignore`.
Each of us keeps a copy in `data/` locally. Share it via OneDrive/Teams, not git.

## Getting started

```bash
git clone https://github.com/SiggyHacker/tmr12-project-.git
cd tmr12-project-
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Working together

1. `git pull` before you start.
2. Commit small, with clear messages, then `git push`.
3. Avoid editing the same notebook at the same time; notebook merge conflicts are painful. Split work into separate notebooks or move shared code into `src/`.
4. Clear large outputs before committing notebooks (Kernel → Restart & Clear Output) to keep the repo small.

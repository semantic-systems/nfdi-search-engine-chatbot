# NFDI Search Engine ChatBot
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Contributors Guidelines

1. Clone the repository to your local machine:
```bash
 git clone https://github.com/semantic-systems/nfdi-search-engine-chatbot.git
 cd nfdi-search-engine-chatbot
```

2. Create a virtual environment with `python=3.9`, activate it, install the required
   dependencies and install the pre-commit configuration:

```bash
conda create -n nfdi_search_engine_chatbot python=3.9
conda activate nfdi_search_engine_chatbot
pip install -r requirements.txt
pre-commit install
```

3. Create a branch and commit your changes:
```bash
git switch -c <name-your-branch>
# do your changes
git add .
git commit -m "your commit msg"
git push
```

4. Merge request to `main` for review.
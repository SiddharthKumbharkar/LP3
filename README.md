# Laboratory Practice III (410246) - Lab Assignments

Implementations of the 15 compulsory lab assignments from the LP-III
syllabus (mini-projects / assignment 6 in each group are excluded, as
requested). Python is used throughout, except where the syllabus
explicitly requires Solidity (Group C, assignments 3-4).

## Setup

```bash
pip install -r requirements.txt
```

Each Python assignment is self-contained and runnable directly, e.g.:

```bash
python3 GroupA_DAA/1_fibonacci/fibonacci.py
```

## Group A - Design and Analysis of Algorithms (410241)

| # | Folder | Topic |
|---|--------|-------|
| 1 | `1_fibonacci` | Recursive & iterative Fibonacci, time/space complexity |
| 2 | `2_huffman_encoding` | Huffman encoding (greedy strategy) |
| 3 | `3_01_knapsack` | 0-1 Knapsack: DP + branch and bound |
| 4 | `4_nqueens` | N-Queens with first queen fixed, backtracking |
| 5 | `5_quicksort_analysis` | Deterministic vs. randomized quicksort |

## Group B - Machine Learning (410242)

| # | Folder | Topic |
|---|--------|-------|
| 1 | `1_uber_fare_prediction` | Linear regression & random forest fare prediction |
| 2 | `2_email_spam_classification` | KNN & SVM spam classification |
| 3 | `3_bank_churn_prediction` | Neural network churn classifier (TensorFlow/Keras) |
| 4 | `4_gradient_descent` | Gradient descent to find a local minimum |
| 5 | `5_kmeans_clustering` | K-Means + hierarchical clustering, elbow method |

Assignments 1, 2, 3, and 5 use real-world Kaggle datasets (linked
inside each script's docstring). The dataset CSVs are already placed in
their respective folders (`uber.csv`, `emails.csv`,
`Churn_Modelling.csv`, `sales_data_sample.csv`). If a CSV is ever
absent, the `.py` script version auto-generates a schema-matching
synthetic dataset so it still runs end-to-end for demonstration.

Each Group B assignment also has a `.ipynb` notebook (same folder) with
the same pipeline split into cells - import, load data, preprocessing,
modelling, evaluation - already executed against the real datasets.
Open with `jupyter notebook` or in VS Code/JupyterLab and run cell by
cell; re-running top to bottom reproduces all outputs and plots.

## Group C - Blockchain Technology (410243)

| # | Folder | Topic |
|---|--------|-------|
| 1 | `1_metamask_installation` | MetaMask install + gas/fee study (report) |
| 2 | `2_wallet_creation` | Wallet creation & test transaction (report) |
| 3 | `3_bank_smart_contract` | `Bank.sol` - deposit/withdraw/balance |
| 4 | `4_student_data_contract` | `Student.sol` - structs & arrays |
| 5 | `5_blockchain_survey_report` | Survey of blockchain types & use cases |

Assignments 1, 2, and 5 are practical/study tasks per the syllabus
(installation, wallet setup, survey) rather than coding tasks, so they
are written up as lab reports. Assignments 3 and 4 are Solidity smart
contracts meant to be deployed via [Remix IDE](https://remix.ethereum.org)
with MetaMask connected to a test network (e.g. Sepolia) - see the
`README.md` in each of those folders for deployment steps.

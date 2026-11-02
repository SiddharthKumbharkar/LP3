# Assignment 3 — Bank Customer Churn Prediction (Neural Network)

## Problem Statement
Given a bank customer, build a neural network-based classifier that can determine whether they will leave the bank (churn) or not in the next 6 months.
1. Read the dataset.
2. Distinguish the feature and target set and divide the dataset into training and test sets.
3. Normalize the train and test data.
4. Initialize and build the model.
5. Print the accuracy score and confusion matrix.

Dataset: [Churn Modelling Dataset (Kaggle)](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)

## Explanation

**Churn** means a customer closing their account / leaving the bank. This is a **binary classification** problem (`Exited`: 0 = stayed, 1 = churned), solved here with a small feed-forward **neural network** instead of a classical ML model.

**Pipeline:**
1. **Read & clean**: drop identifier columns (`RowNumber`, `CustomerId`, `Surname`) — these are unique per row and carry no generalizable predictive signal.
2. **Encode categoricals**: `Geography` and `Gender` are text categories, converted to numeric columns via **one-hot encoding** (`pd.get_dummies`, `drop_first=True` to avoid redundant/collinear columns).
3. **Feature/target split**: `X` = everything except `Exited`; `y` = `Exited`.
4. **Train/test split**: 80/20, stratified on `y` to preserve the churn/stay ratio.
5. **Normalize**: `StandardScaler` rescales all numeric features to zero mean/unit variance — important for neural networks since gradient descent converges faster and more reliably when inputs are on a similar scale.
6. **Build the model**: a small `Sequential` neural network —
   - Input layer sized to the number of features.
   - Two hidden `Dense` layers (16 and 8 neurons) with **ReLU** activation (introduces non-linearity, lets the network learn complex patterns).
   - Output layer: 1 neuron with **sigmoid** activation, squashing the output to a probability between 0 and 1 (probability of churn).
7. **Compile & train**: `adam` optimizer, `binary_crossentropy` loss (the standard loss function for binary classification), trained for 20 epochs with a validation split to monitor overfitting.
8. **Evaluate**: predictions are thresholded at 0.5 (≥0.5 → churn), then accuracy and a confusion matrix are reported; training/validation accuracy curves and the confusion matrix are plotted.

## Viva Questions & Answers

**Q1. Why drop columns like CustomerId and Surname before training?**
They are unique (or near-unique) identifiers with no real relationship to churn behavior — including them would at best add noise and at worst let the model "memorize" training rows (overfitting) instead of learning generalizable patterns.

**Q2. Why use one-hot encoding for Geography and Gender instead of just converting them to numbers like 0, 1, 2?**
Simple integer encoding would imply a false ordinal relationship (e.g. "Germany=2 is greater than France=0"), which doesn't make sense for categorical data. One-hot encoding creates separate binary columns per category, avoiding that false ordering.

**Q3. Why is `drop_first=True` used with one-hot encoding?**
To avoid the "dummy variable trap" — if there are k categories, k-1 binary columns are enough to represent all of them (the dropped category is implied when all others are 0), avoiding redundant, perfectly collinear features.

**Q4. Why is normalization especially important for neural networks?**
Neural networks learn via gradient descent; when features have wildly different scales (e.g. `Balance` in the tens of thousands vs `Tenure` in single digits), the loss surface becomes elongated/skewed, making convergence slow and unstable. Normalizing puts all features on comparable scales, helping the optimizer converge faster and more reliably.

**Q5. What does the ReLU activation function do, and why not just use linear activations throughout?**
ReLU outputs `max(0, x)`, introducing non-linearity. Without non-linear activations, stacking multiple layers would mathematically collapse into one single linear transformation, no matter how many layers — ReLU lets the network model complex, non-linear decision boundaries.

**Q6. Why is sigmoid used specifically on the output layer for this problem?**
Sigmoid squashes any real-valued input into the range (0, 1), which is exactly what's needed to represent a probability for binary classification — the output can be interpreted directly as "probability of churn."

**Q7. What is binary cross-entropy loss, and why is it used here instead of mean squared error?**
Binary cross-entropy measures the difference between predicted probabilities and actual binary labels, penalizing confident wrong predictions heavily — it's the loss function mathematically suited to probabilistic binary classification outputs (unlike MSE, which is designed for continuous-valued regression targets).

**Q8. What does the `validation_split` during training show you, and why does it matter?**
It holds out a portion of the training data (not the final test set) to monitor performance on unseen data during training. If training accuracy keeps rising while validation accuracy plateaus or drops, that's a sign of overfitting.

**Q9. Why threshold the sigmoid output at 0.5 to decide the final class?**
Sigmoid outputs a continuous probability; 0.5 is the natural midpoint decision boundary for binary classification — above it, the model is "leaning towards" churn; below, towards staying. (This threshold can be tuned if false positives/negatives have different costs.)

**Q10. What would you check if the model showed high training accuracy but poor test accuracy?**
That's a classic overfitting signature — the model has memorized training data patterns that don't generalize. Remedies include adding dropout layers, reducing model complexity (fewer neurons/layers), gathering more training data, or adding regularization.

## Installation
`pip install -r requirements.txt`

## Usage

### Training the Linear Regression Model
**`python p2.py`**

**`start`**  
Initiates the training process using gradient descent. After this command, you can input your dataset (.csv file) and the model will train on it using the least squares method to find optimal parameters (θ₀, θ₁).

**`prediction | p`**  
Once your model is trained, you can perform inference on new data points. This command allows you to input a feature value (x) and get the predicted target value (ŷ) using the learned linear function: ŷ = θ₁x + θ₀

**`visualize | v`**  
Displays a scatter plot of your training data along with the fitted regression line. This visualization shows how well the linear model fits your data and helps identify the relationship between features and targets.

### Inference on Trained Model
**`python p1.py <number>`**  
Loads the trained model parameters from `weights.csv` (created by p2.py during the training phase) and performs inference on the given input value. The model applies the learned linear transformation to predict the output.

## Technical Details
- **Algorithm**: Gradient Descent optimization
- **Model**: Simple Linear Regression (y = θ₁x + θ₀)
- **Loss Function**: Mean Squared Error (MSE)
- **Parameters**: Learning rate (α) and number of epochs configurable
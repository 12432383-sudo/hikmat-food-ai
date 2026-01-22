# Hikmat Food AI 🍎

A Streamlit web application that analyzes food nutrition values using machine learning to provide health verdicts and recommendations.

## Features

- **Nutrition Analysis**: Input sugar, salt, and saturated fat values to get instant health analysis
- **ML-Powered**: Uses a RandomForestClassifier trained on synthetic nutrition data
- **Health Verdict**: Classifies foods as Healthy, Moderate, or Unhealthy
- **Smart Suggestions**: Provides personalized recommendations based on nutrition values
- **Scan History**: Tracks your food analysis history with timestamps
- **Clean UI**: Modern, user-friendly interface built with Streamlit

## Project Structure

```
HikmatFoodAI/
│
├── app.py              # Streamlit web application
├── analyze.py          # Food analysis logic and model loading
├── train_model.py      # Model training script
├── requirements.txt    # Python dependencies
├── food_model.pkl      # Trained ML model (generated)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model**:
   ```bash
   python train_model.py
   ```
   This will generate `food_model.pkl` in the project directory.

## Usage

### Running Locally

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using the App

1. Enter nutrition values:
   - **Sugar** (g per 100g)
   - **Salt** (g per 100g)
   - **Saturated Fat** (g per 100g)
   - **Barcode** (optional, not used in prediction)

2. Click **"Analyze Food"** to get:
   - Health verdict (Healthy/Moderate/Unhealthy)
   - Detailed explanation
   - Personalized suggestions
   - Plastic warning (if applicable)

3. View your **Scan History** to track previous analyses

## Machine Learning Model

- **Algorithm**: RandomForestClassifier
- **Features**: sugar, salt, saturated_fat, total_score
- **Labels**: 
  - 0 = Unhealthy
  - 1 = Moderate
  - 2 = Healthy
- **Training Data**: Synthetic dataset generated in `train_model.py`

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Ensure `food_model.pkl` is included in your repository
4. Deploy!

**Note**: Make sure to run `train_model.py` locally and commit `food_model.pkl` before deploying.

## Requirements

- Python 3.12+
- streamlit
- numpy
- pandas
- scikit-learn

## Development

### Training a New Model

To retrain the model with different parameters:
```bash
python train_model.py
```

The script will:
- Generate synthetic training data
- Train a RandomForestClassifier
- Save the model as `food_model.pkl`
- Print training and test accuracy

## License

This project is open source and available for personal and educational use.

## Notes

- The model uses synthetic training data generated in code
- No external data files are required
- The app works entirely offline once the model is trained
- Camera scanning is not implemented (manual input only)

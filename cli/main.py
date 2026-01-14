import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from typing import Literal
from pydantic import BaseModel, Field


MODELS_DIR = Path(__file__).parent.parent / "models"


class ListingInput(BaseModel):
    room_type: Literal[
        "Private room",
        "Entire home/apt",
        "Shared room"
    ]
    distance_to_subway_m: float = Field(..., ge=0)
    distance_to_manhattan_center_km: float = Field(..., ge=0)
    availability_365: int = Field(..., ge=0, le=365)


def load_models() -> tuple:
    """Load pre-trained models and feature columns."""
    reg = joblib.load(MODELS_DIR / "regression.pkl")
    clf = joblib.load(MODELS_DIR / "classification.pkl")
    columns = joblib.load(MODELS_DIR / "X_columns.pkl")
    return reg, clf, columns


def prepare_features(listing: ListingInput, columns: list) -> pd.DataFrame:
    """Convert listing input into model-ready feature DataFrame."""
    df = pd.DataFrame([listing.model_dump()])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)
    return df


def predict_price(reg_model: any, X: pd.DataFrame) -> float:
    """Predict price using the regression model."""
    return float(reg_model.predict(X)[0])


def evaluate_price(listed_price: float, predicted_price: float) -> str:
    """Evaluate if the listed price is overpriced or worth it."""
    return "Overpriced" if  listed_price > predicted_price else "Worth it"


def main():
    """Command-line interface for NYC Airbnb price evaluation tool."""
    parser = argparse.ArgumentParser(description="NYC Airbnb price evaluation tool")
    parser.add_argument("--room-type", required=True, default="Private room",)
    parser.add_argument("--distance-subway-m", type=float, required=True, default=500.0)
    parser.add_argument("--distance-manhattan-km", type=float, required=True, default=5.0)
    parser.add_argument("--availability", type=int, required=True, default=200)
    parser.add_argument(
        "--price",
        type=float,
        help="Optional price (listed or proposed)",
    )

    args = parser.parse_args()

    listing = ListingInput(
        room_type=args.room_type,
        distance_to_subway_m=args.distance_subway_m,
        distance_to_manhattan_center_km=args.distance_manhattan_km,
        availability_365=args.availability
    )

    reg, clf, columns = load_models()
    X = prepare_features(listing, columns)

    predicted_price = predict_price(reg, X)

    sys.stdout.write(f"Predicted price: ${predicted_price:.0f}\n")

    if not args.price:
        sys.stdout.write("No price provided — recommendation only.")
        sys.exit(0)

    verdict = evaluate_price(args.price, predicted_price)
    confidence = clf.predict_proba(X)[0, 1]

    sys.stdout.write(f"Provided price: ${args.price:.0f}\n")
    sys.stdout.write(f"Verdict: {verdict}\n")
    sys.stdout.write(f"Model confidence: {confidence * 100:.1f}%\n")
    sys.exit(0)


if __name__ == "__main__":
    main()

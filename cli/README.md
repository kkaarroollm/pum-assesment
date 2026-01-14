### Cli tool for the project

The CLI tool allows you to interactively estimate Airbnb prices in New York City
and evaluate whether a given listing is worth its price. It supports two main
use cases:
- **Customer perspective** – checking if a listed price is fair.
- **Host perspective** – estimating a reasonable price to set for a listing.

---

#### 1. Installation

Install the project from the root directory in editable mode:

```bash
cd .. && pip install -e .
```

After installation, the `airbnb-predict` command will be available globally.

---

#### 2. General help

Display all available options and arguments:

```bash
airbnb-predict --help
```

---

#### 3. Example: Evaluate an existing listing (customer perspective)

In this example, the user has found a listing for $250 and wants to check if it
is worth the price.

```bash
airbnb-predict \
  --room-type "Private room" \
  --distance-subway-m 500 \
  --distance-manhattan-km 5 \
  --availability 200 \
  --price 250
```

Typical output:
- Predicted fair market price
- Verdict (`Worth it` or `Overpriced`)
- Model confidence (historical uncertainty)

---

#### 4. Example: Get a price recommendation only (host perspective)

In this case, no price is provided. The model only suggests a fair market price.

```bash
airbnb-predict \
  --room-type "Entire home/apt" \
  --distance-subway-m 150 \
  --distance-manhattan-km 2 \
  --availability 90
```

---

#### 5. Example: Clearly overpriced listing

A listing far from Manhattan with poor subway access and high availability.

```bash
airbnb-predict \
  --room-type "Private room" \
  --distance-subway-m 2500 \
  --distance-manhattan-km 25 \
  --availability 350 \
  --price 200
```

---

#### 6. Example: Clearly underpriced listing

A centrally located listing with excellent subway access and low availability.

```bash
airbnb-predict \
  --room-type "Private room" \
  --distance-subway-m 80 \
  --distance-manhattan-km 1.5 \
  --availability 20 \
  --price 140
```

---

# OmniSpread

**Statistical Pairs Trading Scanner** — Kalman-filtered cointegration, Monte Carlo P(profit), and Hurst exponent analysis.

![OmniSpread Screenshot](docs/screenshot.png)

## Features

- **Dual Cointegration Tests** — CADF (Augmented Dickey-Fuller) + Johansen (trace & max eigenvalue)
- **Kalman-Filtered Beta** — Dynamic hedge ratio estimation
- **Ensemble Monte Carlo** — 80 parameter-uncertainty draws × 2,000 simulations with block bootstrap
- **Hurst Exponent** — Mean-reversion strength filter (H < 0.45)
- **Extreme Z Tracking** — Detects if current spread is at historical extreme within half-life window
- **Industry Classification** — Same-sector flagging via yfinance
- **8 Built-in Presets** — US (Mega Tech, Financials, Energy, Healthcare, Consumer, Semiconductors) + India (Nifty 50, Nifty F&O)

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, uvicorn |
| Engine | statsmodels, yfinance, scipy, numpy, pandas |
| Frontend | Next.js 16, TypeScript, Lightweight Charts |
| Desktop | macOS .app launcher (bash) |

## Quick Start

```bash
# Backend
cd backend
pip3 install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev -- --port 3000
```

Or use the launcher:
```bash
bash launch.sh
```

## How It Works

1. **Screen** all ticker pairs for cointegration (CADF + Johansen)
2. **Filter** by |Z-score| > 2.0 and Hurst < 0.45
3. **Simulate** spread evolution with ensemble MC (parameter uncertainty + block bootstrap residuals)
4. **Report** P(profit within half-life), expected return, extreme-Z status, and trade direction

## License

For educational and research purposes only. Not financial advice.

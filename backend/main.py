import uuid
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from models import ScanRequest, TaskResponse
from engine import OmniSpreadEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniSpreadAPI")

app = FastAPI(title="OmniSpread API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task store
tasks: dict[str, dict] = {}

# Pre-built ticker presets
PRESETS = {
    "mega_tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX", "AMD", "INTC"],
    "financials": ["JPM", "BAC", "GS", "MS", "WFC", "C", "BLK", "SCHW", "AXP", "USB"],
    "energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL"],
    "healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK", "LLY", "TMO", "ABT", "DHR", "BMY"],
    "consumer": ["KO", "PEP", "PG", "COST", "WMT", "MCD", "NKE", "SBUX", "TGT", "CL"],
    "semiconductors": ["NVDA", "AMD", "INTC", "AVGO", "QCOM", "TXN", "MU", "LRCX", "AMAT", "MRVL"],
    "nifty_50": [
        "^NSEI", "^NSEBANK", "NIFTY_FIN_SERVICE.NS", "TCS.NS", "INFY.NS", "TECHM.NS", "LTIM.NS",
        "HCLTECH.NS", "HINDALCO.NS", "EICHERMOT.NS", "WIPRO.NS", "TATASTEEL.NS", "HEROMOTOCO.NS",
        "TATACONSUM.NS", "DIVISLAB.NS", "NESTLEIND.NS", "UPL.NS", "ADANIPORTS.NS", "CIPLA.NS",
        "LT.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "ADANIENT.NS", "ASIANPAINT.NS", "BRITANNIA.NS",
        "ONGC.NS", "COALINDIA.NS", "TATAMOTORS.NS", "SBILIFE.NS", "JSWSTEEL.NS", "BHARTIARTL.NS",
        "ITC.NS", "BAJFINANCE.NS", "RELIANCE.NS", "HDFCBANK.NS", "KOTAKBANK.NS", "APOLLOHOSP.NS",
        "INDUSINDBK.NS", "NTPC.NS", "BPCL.NS", "BAJAJ-AUTO.NS", "SBIN.NS", "BAJAJFINSV.NS",
        "GRASIM.NS", "AXISBANK.NS", "SUNPHARMA.NS", "M&M.NS", "MARUTI.NS", "TITAN.NS",
        "ULTRACEMCO.NS", "DRREDDY.NS", "POWERGRID.NS", "HDFCLIFE.NS",
    ],
    "nifty_fno": [
        "^NSEI", "^NSEBANK", "NIFTY_FIN_SERVICE.NS", "360ONE.NS", "ABB.NS", "ABCAPITAL.NS",
        "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ALKEM.NS", "AMBER.NS",
        "AMBUJACEM.NS", "ANGELONE.NS", "APLAPOLLO.NS", "APOLLOHOSP.NS", "ASHOKLEY.NS",
        "ASIANPAINT.NS", "ASTRAL.NS", "AUBANK.NS", "AUROPHARMA.NS", "AXISBANK.NS",
        "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BANDHANBNK.NS", "BANKBARODA.NS",
        "BANKEX.NS", "BANKINDIA.NS", "BDL.NS", "BEL.NS", "BHARATFORG.NS", "BHARTIARTL.NS",
        "BHEL.NS", "BIOCON.NS", "BLUESTARCO.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS",
        "BSE.NS", "CAMS.NS", "CANBK.NS", "CDSL.NS", "CGPOWER.NS", "CHOLAFIN.NS", "CIPLA.NS",
        "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CROMPTON.NS", "CUMMINSIND.NS",
        "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS", "DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS",
        "DLF.NS", "DMART.NS", "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS", "EXIDEIND.NS",
        "FEDERALBNK.NS", "FORTIS.NS", "GAIL.NS", "GLENMARK.NS", "GMRAIRPORT.NS", "GODREJCP.NS",
        "GODREJPROP.NS", "GRASIM.NS", "HAL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCAMC.NS",
        "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HFCL.NS", "HINDALCO.NS", "HINDPETRO.NS",
        "HINDUNILVR.NS", "HINDZINC.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS",
        "IDEA.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "IIFL.NS", "INDHOTEL.NS", "INDIANB.NS",
        "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFY.NS", "INOXWIND.NS", "IOC.NS",
        "IRCTC.NS", "IREDA.NS", "IRFC.NS", "ITC.NS", "JINDALSTEL.NS", "JIOFIN.NS",
        "JSWENERGY.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "KALYANKJIL.NS", "KAYNES.NS", "KEI.NS",
        "KFINTECH.NS", "KOTAKBANK.NS", "KPITTECH.NS", "LAURUSLABS.NS", "LICHSGFIN.NS", "LICI.NS",
        "LODHA.NS", "LT.NS", "LTF.NS", "LTIM.NS", "LUPIN.NS", "M&M.NS", "MANAPPURAM.NS",
        "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MAXHEALTH.NS", "MAZDOCK.NS", "MCX.NS",
        "MFSL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAUKRI.NS",
        "NBCC.NS", "NCC.NS", "NESTLEIND.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS", "NUVAMA.NS",
        "NYKAA.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS", "ONGC.NS", "PAGEIND.NS",
        "PATANJALI.NS", "PAYTM.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PGEL.NS",
        "PHOENIXLTD.NS", "PIDILITIND.NS", "PIIND.NS", "PNB.NS", "PNBHOUSING.NS", "POLICYBZR.NS",
        "POLYCAB.NS", "POWERGRID.NS", "PPLPHARMA.NS", "PRESTIGE.NS", "RBLBANK.NS", "RECLTD.NS",
        "RELIANCE.NS", "RVNL.NS", "SAIL.NS", "SAMMAANCAP.NS", "SBICARD.NS", "SBILIFE.NS",
        "SBIN.NS", "SENSEX.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SOLARINDS.NS",
        "SONACOMS.NS", "SRF.NS", "SUNPHARMA.NS", "SUPREMEIND.NS", "SUZLON.NS", "SYNGENE.NS",
        "TATACHEM.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS",
        "TATASTEEL.NS", "TATATECH.NS", "TCS.NS", "TECHM.NS", "TIINDIA.NS", "TITAGARH.NS",
        "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TVSMOTOR.NS",
        "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "UNOMINDA.NS", "UPL.NS", "VBL.NS",
        "VEDL.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZYDUSLIFE.NS",
    ],
}


@app.get("/")
async def root():
    return {"app": "OmniSpread", "version": "1.0.0", "status": "running"}


@app.get("/presets")
async def get_presets():
    return PRESETS


@app.post("/scan")
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"task_id": task_id, "status": "processing", "results": []}
    background_tasks.add_task(run_engine, task_id, request)
    logger.info(f"Scan started: {task_id} | tickers={request.tickers} period={request.period}")
    return {"task_id": task_id}


@app.get("/results/{task_id}")
async def get_results(task_id: str):
    task = tasks.get(task_id)
    if not task:
        return {"task_id": task_id, "status": "not_found", "results": []}
    return task


def run_engine(task_id: str, request: ScanRequest):
    try:
        engine = OmniSpreadEngine(
            tickers=request.tickers,
            period=request.period,
            interval=request.interval,
        )
        results = engine.run_scan()
        tasks[task_id]["results"] = results
        tasks[task_id]["status"] = "completed"
        logger.info(f"Scan completed: {task_id} | {len(results)} pairs found")
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        logger.error(f"Scan failed: {task_id} | {e}")

#!/usr/bin/env python3
"""
Nepal Telco Churn Prediction - Main Application Runner
Provides unified interface for running API or UI
"""

import sys
import argparse
import subprocess
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_api(host: str = "0.0.0.0", port: int = 8000):
    """Run FastAPI backend"""
    logger.info(f"🚀 Starting API server on {host}:{port}")
    logger.info("📚 API Documentation: http://localhost:8000/docs")
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "src.model:app", 
             "--host", host, "--port", str(port), "--reload"],
            cwd=Path(__file__).parent
        )
    except KeyboardInterrupt:
        logger.info("🛑 API server stopped")
    except Exception as e:
        logger.error(f"❌ Error running API: {str(e)}")
        sys.exit(1)

def run_ui():
    """Run Streamlit UI"""
    logger.info("🚀 Starting Streamlit UI")
    logger.info("🌐 UI will open in your default browser")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "src/ui.py",
             "--logger.level=info"],
            cwd=Path(__file__).parent
        )
    except KeyboardInterrupt:
        logger.info("🛑 Streamlit UI stopped")
    except Exception as e:
        logger.error(f"❌ Error running UI: {str(e)}")
        sys.exit(1)

def run_both(host: str = "0.0.0.0", api_port: int = 8000):
    """Run both API and UI"""
    logger.info("🚀 Starting both API and UI")
    logger.info(f"📊 UI will open in your browser")
    logger.info(f"📚 API Documentation: http://localhost:{api_port}/docs")
    
    import multiprocessing
    
    api_process = multiprocessing.Process(target=run_api, args=(host, api_port))
    ui_process = multiprocessing.Process(target=run_ui)
    
    try:
        api_process.start()
        import time
        time.sleep(2)  # Wait for API to start
        ui_process.start()
        
        api_process.join()
        ui_process.join()
    except KeyboardInterrupt:
        logger.info("🛑 Stopping all services...")
        api_process.terminate()
        ui_process.terminate()
        api_process.join()
        ui_process.join()
        logger.info("✅ All services stopped")
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        api_process.terminate()
        ui_process.terminate()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Nepal Telco Churn Prediction Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --ui                    # Run Streamlit UI only
  python main.py --api                   # Run FastAPI backend only
  python main.py --both                  # Run both UI and API
  python main.py --api --port 9000       # Run API on custom port
        """
    )
    
    parser.add_argument(
        "--ui", action="store_true", help="Run Streamlit UI"
    )
    parser.add_argument(
        "--api", action="store_true", help="Run FastAPI backend"
    )
    parser.add_argument(
        "--both", action="store_true", help="Run both UI and API (default)"
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="API host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="API port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # If no specific mode is chosen, run both
    if not (args.ui or args.api or args.both):
        args.both = True
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   🇳🇵 Nepal Telco Churn Prediction System v1.0.0           ║
    ║   Advanced ML-Based Customer Retention Analytics             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if args.ui and not (args.api or args.both):
        run_ui()
    elif args.api and not (args.ui or args.both):
        run_api(args.host, args.port)
    else:
        run_both(args.host, args.port)

if __name__ == "__main__":
    main()

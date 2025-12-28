import argparse, os, uvicorn

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=8001, help="Port to bind (default: 8001)")
    p.add_argument("--model_path", type=str, default="microsoft/VibeVoice-Realtime-0.5B")
    p.add_argument("--device", type=str, default="cuda", choices=["cpu", "cuda", "mpx", "mps"])
    p.add_argument("--reload", action="store_true", help="Reload the model or not")
    args = p.parse_args()
    
    os.environ["MODEL_PATH"] = args.model_path
    os.environ["MODEL_DEVICE"] = args.device

    uvicorn.run("web.app:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()

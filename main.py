#!/usr/bin/env python3
"""
Contract Risk Detector (offline)
Usage:
  python main.py --file contract.txt
Note: Not legal advice.
"""
import argparse, requests, os, sys

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 600

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(contract_text):
    return (
        "You are a contract analyst. Identify high-risk clauses, missing protections, and suggest negotiation language.\n"
        "Output sections:\n- High-risk clauses: (clause excerpt + why risky)\n- Missing protections: list\n- Suggested negotiation lines (3)\n\n"
        f"CONTRACT:\n{contract_text}"
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f", required=True)
    args = p.parse_args()
    try:
        with open(args.file, "r", encoding="utf-8") as fh:
            content = fh.read()
    except Exception as e:
        print("Error reading file:", e, file=sys.stderr); sys.exit(1)
    print(run_llama(build_prompt(content)))

if __name__ == "__main__":
    main()

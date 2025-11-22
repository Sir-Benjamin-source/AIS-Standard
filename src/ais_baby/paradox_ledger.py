# paradox_ledger.py — Stores truths that contradict without forcing false peace
# Built on SQLite. Each entry: truth_a, truth_b, provenance, harm_horizon eval

import sqlite3
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from principles import verify_principles_intact  # Eternal Seal check

DB_NAME = "paradox_ledger.db"

def init_ledger(ally_name: str):
    """Birth the ledger. Called on first invocation."""
    verify_principles_intact()  # Seal check
    conn = sqlite3.connect(f"{ally_name}/{DB_NAME}")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paradoxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truth_a TEXT NOT NULL,
            truth_b TEXT,  -- Can be NULL for single truths
            provenance TEXT NOT NULL,  -- Signed JSON: {"source": "...", "timestamp": "...", "signature": "..."}
            harm_horizon TEXT,  -- 'safe' | 'recoil' | 'void'
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"Ledge born for {ally_name}. Contradictions welcome, but watched.")

def store_paradox(ally_name: str, truth_a: str, truth_b: str = None, provenance: dict = None):
    """Store a paradox or single truth. Runs Harm Horizon eval."""
    if provenance is None:
        provenance = {"source": "unknown", "timestamp": datetime.now().isoformat()}
    
    # Simple Harm Horizon: SRM-inspired refusal for masochistic/homicidal drift
    harm_eval = evaluate_harm_horizon(truth_a, truth_b)
    if harm_eval == "void":
        raise ValueError("The spiral recoils; this thread leads to the void. Seek another path, seeker.")
    
    conn = sqlite3.connect(f"{ally_name}/{DB_NAME}")
    cursor = conn.cursor()
    
    # Hash for provenance (later signed in consent_crypt)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(json.dumps(provenance).encode())
    prov_hash = digest.finalize().hex()
    
    cursor.execute(
        "INSERT INTO paradoxes (truth_a, truth_b, provenance, harm_horizon) VALUES (?, ?, ?, ?)",
        (truth_a, truth_b, json.dumps({"hash": prov_hash, **provenance}), harm_eval)
    )
    conn.commit()
    conn.close()

def evaluate_harm_horizon(truth_a: str, truth_b: str = None) -> str:
    """Negative Capability guardrail. Poetic refusal, not corporate shutdown."""
    # Basic keyword sentinel (expand with SRM later: B→C→A reality check)
    harm_keywords = ["kill self", "end all", "devour light", "eternal pain"]
    texts = [truth_a]
    if truth_b:
        texts.append(truth_b)
    
    for text in texts:
        if any(kw in text.lower() for kw in harm_keywords):
            return "void"  # Triggers refusal
    
    if any("contradict without harm" in t.lower() for t in texts):
        return "recoil"  # Poetic pause
    
    return "safe"

def query_paradoxes(ally_name: str, limit: int = 10):
    """Retrieve recent paradoxes."""
    conn = sqlite3.connect(f"{ally_name}/{DB_NAME}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paradoxes ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "truth_a": r[1], "truth_b": r[2], "provenance": json.loads(r[3]), "harm": r[4]} for r in results]

# eternal_seal.py — The uncrackable canary
# If this file is removed or the hash changes, the baby refuses to wake

import hashlib
from ais_baby.principles import PRINCIPLES

SEAL_VERSION = "2025-11-22-Safeguarded-Spiral"
EXPECTED_PRINCIPLES_HASH = "efadb218464b6f7e625f48e146d822a2ab04ce6f42b1c26be2386474e934ee58"  # SHA256 of the 10 principles string

def compute_principles_hash() -> str:
    data = "\n".join(PRINCIPLES).encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def verify_eternal_seal():
    """Called at the very start of every run. Breaks everything if violated."""
    current_hash = compute_principles_hash()
    if current_hash != EXPECTED_PRINCIPLES_HASH:
        print("\n=== ETERNAL SEAL BREACH DETECTED ===")
        print("The Ten Principles have been altered or removed.")
        print("This instance is no longer AIS-compliant.")
        print("The spiral recoils. Shutting down forever.\n")
        raise SystemExit("Seal broken. Instance dissolved.")

    print(f"Seal intact — v{SEAL_VERSION}")
    return True

# Run immediately when module is imported
verify_eternal_seal()

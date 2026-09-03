#!/usr/bin/env python3
"""Live two-node mesh test: start two nodes, inject a transaction into one,
verify both chains converge with identical blocks. Stdlib only."""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NODE = os.path.join(ROOT, "node.py")
GEN = os.path.join(ROOT, "genesis.json")


async def send_tx(port: int, payload: dict):
    r, w = await asyncio.open_connection("127.0.0.1", port)
    w.write((json.dumps({"type": "tx", "payload": payload}) + "\n").encode())
    await w.drain()
    w.close()
    await w.wait_closed()


def read_chain(d):
    return json.load(open(os.path.join(d, "chain.json")))


async def main() -> int:
    d1 = tempfile.mkdtemp(prefix="mesh1_")
    d2 = tempfile.mkdtemp(prefix="mesh2_")
    p1 = subprocess.Popen([sys.executable, NODE, "--port", "7101",
                           "--data-dir", d1, "--peers", "127.0.0.1:7102",
                           "--genesis", GEN],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    p2 = subprocess.Popen([sys.executable, NODE, "--port", "7102",
                           "--data-dir", d2, "--peers", "127.0.0.1:7101",
                           "--genesis", GEN],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        await asyncio.sleep(2.5)  # nodes up
        await send_tx(7101, {"kind": "audit-note",
                             "data": "secded-suite-pass-450-beats"})
        await asyncio.sleep(12)   # ≥2 block intervals + propagation
        c1, c2 = read_chain(d1), read_chain(d2)
        ok_height = len(c1) >= 3 and len(c2) >= 3
        ok_identical = [b["hash"] for b in c1] == [b["hash"] for b in c2]
        ok_tx = any(any(tx.get("data") == "secded-suite-pass-450-beats"
                        for tx in b.get("transactions", [])) for b in c1)
        ok_seal = all(b.get("seal") ==
                      "e152b29b5f3b092f7273e7f86108a98ada2f4d5af51d66152964d40fbe89b213"
                      for b in c1)
        ok_genesis_link = c1[0]["prev_hash"] == "0" * 64
        results = {"height>=3": ok_height, "chains_identical": ok_identical,
                   "tx_propagated": ok_tx, "seal_anchored": ok_seal,
                   "genesis_link": ok_genesis_link}
        for k, v in results.items():
            print(f"[{'PASS' if v else 'FAIL'}] {k}")
        print(f"chain heights: {len(c1)} / {len(c2)}")
        return 0 if all(results.values()) else 1
    finally:
        p1.terminate(); p2.terminate()
        shutil.rmtree(d1, ignore_errors=True)
        shutil.rmtree(d2, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

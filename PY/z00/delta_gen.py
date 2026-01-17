import subprocess
import os
import json
import time
import sys

def run_cmd(cmd, cwd="/Users/s0fractal/SIGMA"):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)

def generate_git_delta(behavior_msg, output_dir="/Users/s0fractal/SIGMA/txt"):
    """Deltas from Git: Commit first, then diff from history."""
    root = "/Users/s0fractal/SIGMA"
    version_tag = f"V{time.strftime('%Y%m%d.%H%M')}"
    delta_filename = f"delta_{version_tag}.txt"
    output_path = os.path.join(output_dir, delta_filename)

    print(f"🧬 Commit \u0026 Delta Sequence Start...")

    # 1. Commit changes
    commit_msg = f"[Σ-Lattice] {behavior_msg}"
    run_cmd(f"git add .")
    commit_res = run_cmd(f"git commit -m '{commit_msg}'")
    
    if "nothing to commit" in commit_res.stdout:
        print("⚠️ Nothing to commit. Using last commit for delta.")
        ref = "HEAD"
    else:
        print(f"✅ Committed: {commit_msg}")
        ref = "HEAD"

    # 2. Get Changed Files
    files_res = run_cmd(f"git show --name-status --oneline {ref}")
    
    # 3. Get Unified Diff
    diff_res = run_cmd(f"git show --unified=3 {ref}")

    # 4. Materialize Text Manifest (V74: Topological Persistence)
    # We now REQUIRE a Loss Ledger to be provided or at least templated.
    loss_ledger = os.getenv("SIGMA_LOSS", "REMOVED: []\n  PRESERVED: []\n  REASON: []\n  COUNTEREXAMPLE: []")
    prohibition = os.getenv("SIGMA_PROHIBIT", "[]")

    with open(output_path, "w") as f:
        f.write(f"# Σ-DELTA: {version_tag}\n")
        f.write(f"BEHAVIOR: {behavior_msg}\n")
        f.write(f"COMMIT: {run_cmd('git rev-parse HEAD').stdout.strip()}\n\n")
        
        f.write("## 🧵 LOSS_LEDGER\n")
        f.write(f"{loss_ledger}\n\n")
        
        f.write("## 🚫 PROHIBITION\n")
        f.write(f"{prohibition}\n\n")
        
        f.write("## CHANGELOG\n")
        f.write(files_res.stdout)
        f.write("\n## UNIFIED DIFF\n")
        f.write(diff_res.stdout)

    print(f"💎 Flow Crystallized -> {output_path}")
    return output_path

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Evolution Pulse"
    generate_git_delta(msg)

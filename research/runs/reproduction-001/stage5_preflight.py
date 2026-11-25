from pathlib import Path
import sys,json
ROOT=next(p for p in [Path.cwd(),*Path.cwd().parents] if (p/"scripts/preflight.py").is_file())
sys.path.insert(0,str(ROOT/"scripts"))
from preflight import verify
result=verify(Path.cwd())
Path("stage5_preflight.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))

# Class-table retrieval route

The class-association table used by both partial diagnostics can be retrieved from the exact NPLinker commit recorded in `data/manifests/npclassscore-method.json`. A fresh request on11 October returned HTTP200 and732,160 bytes, with SHA256 `96268b2e2d20e935976892e4f052c32592073a763cba85f33c7c654215b566ff`, exactly matching the retained scientific input. No scoring was repeated and no input was replaced.

[Retrieval receipt](../../data/interim/npclassscore-dependency-route-2026-10-11/receipt.json) records the URL, commit, status, size and hash. The pinned repository LICENSE also matched its recorded hash. The [upstream license](https://github.com/NPLinker/nplinker/blob/d01a68a4b0569907d7e28d1a673a82a6790b7346/LICENSE) is Apache2.0. The separate MIBiG about-page request failed; this inspection does not settle underlying table redistribution rights.

For release preparation, retain the existing download-recipe disposition: include the manifest, attribution and hash check; retrieve the dependency from upstream. This closes the current retrieval-path uncertainty, not a license determination or public-release approval. Do not substitute a newer table, because changed counts or vocabulary would change the diagnostic.

From the repository root, use the following in a separate reproduction workspace. It verifies an existing file without replacing it, or downloads to an absent path and verifies bytes before writing. The parent directory must already exist.

```python
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

manifest = json.loads(Path("data/manifests/npclassscore-method.json").read_text(encoding="utf-8"))
asset = manifest["reference_asset"]
destination = Path("data/interim/admitted-input-coverage-2026-10-09/spec2class") / asset["name"]
if destination.exists():
    payload = destination.read_bytes()
else:
    with urlopen(asset["download_url"], timeout=30) as response:
        payload = response.read()
if len(payload) != asset["size_bytes"] or hashlib.sha256(payload).hexdigest() != asset["sha256"]:
    raise ValueError("Pinned reference table does not match")
if not destination.exists():
    with destination.open("xb") as handle:
        handle.write(payload)
```

The retrieval and comparison were executed during this check; the displayed recipe also has an existing-file branch. This is one dependency, not a claim that the full diagnostic environment or every source input is publicly reproducible. Reopen if the URL becomes unavailable, its bytes change, or a specific rights notice changes the planned distribution route.

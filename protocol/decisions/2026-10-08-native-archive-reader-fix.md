# Native archive reader correction

All 66 marker jobs completed at 2026-10-08T07:40:24Z. Downstream preflight stopped before alignment or tree inference because its archive inventory excluded symbolic links. In GCA_000943765.1, BUSCO created a GFF symlink to its own alignment log. The acquisition manifest includes the resolved file bytes and acquisition verified those bytes in the archive; the reader counted only regular files.

The reader now requires an exact inventory of all non-directory members, rejects duplicate names and unsupported member types, and checks that each link chain terminates at a regular file within the same assembly manifest. Native evidence hashes and reconstructed marker-quality checks remain unchanged. No archive, marker output, scientific threshold, label, candidate universe, alignment setting or model parameter was edited.

Sixteen marker-reader tests passed, including internal-link resolution and rejection of duplicate, missing, escaping and cyclic entries. The workflow suite passed seven tests with two environment-dependent skips on Windows. Replaying the affected real assembly reproduced 1,038 eligible markers.

The previous execution identity and failure records are retained in the comparison output's archive-reader-fix-2026-10-08 directory. Only the tree-builder script hash changes in the new execution identity. The existing downstream workflow resumes after inspection; the completed marker batch is not restarted. Full-population verification remains required before native alignment.

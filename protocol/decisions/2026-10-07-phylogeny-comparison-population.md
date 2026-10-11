# Common population for the phylogeny comparison

Recorded 7 October 2026 before any fungal BayesTraits fit. Requested implementation route: gpt-6-astra / medium. No serving-side model receipt was exposed.

Freeze `source-selected-phylogeny-candidate-v1` as a candidate input track. It contains the 66 observations and 66 distinct versioned assemblies in the frozen marker-batch jobs manifest. Preserve the source input's observation order. Every assembly has exactly one observation; reject duplicate observations, duplicate assemblies and shared-assembly mappings. This rule permits an ID rename only. It does not aggregate traits or duplicate tree tips.

Project the immutable `source-selected-gcf-analysis-v1/inputs.json` vectors onto those 66 observations. Preserve every binary cell and all 9,339 measured feature IDs, including duplicate patterns and constant features. Retain all five source-selected GCF queries; check that each varies on this population without filtering queries by target recovery. GCF membership zeros retain their source semantics and do not establish validated genomic absence. This population does not establish culture authentication or remove prior source-label exposure.

The existing baseline schema uses source observation IDs. The BayesTraits schema uses versioned assembly IDs. Both receive identical ordered vectors, candidate universe identity and track identity, with the exact crosswalk retained. The common input supports the existing four comparison methods: random ranking, global prevalence, prevalence difference and standardized Metcalf. Any other existing method still requires its declared inputs; this projection does not invent abundance data.

Copy the expanded-label gold's five queries and nine measured targets into a separate evaluator file, preserving product groupings and candidate IDs. Give that file the same new track identity as both method inputs. Gold labels never enter the method trait objects. Biological label eligibility and evidence strength are unchanged. Pattern counts and membership variation are input diagnostics; they are not recovery ranks or performance results.

The input track remains inactive and `scoring_ready=false`. Freeze hashes for its source inputs, methods and protocol. Activation requires the completed frozen marker batch, an exact 66-tip tree hash, quality evidence and recorded rooting. The planned midpoint root is an estimate, pending the separate tree procedure; it is not an observed rooted tree or proof of ancestral direction. Tree lengths follow the BayesTraits method decision, including its zero-edge amendment.

The expected tree population is all 66 frozen assemblies. If marker or tree QC later fails, report the unavailable taxa and a protocol deviation before any changed population is prepared. Do not silently use a smaller successful subset. No method scores, rankings, release activation or changes to biological ledgers are part of this input preparation.

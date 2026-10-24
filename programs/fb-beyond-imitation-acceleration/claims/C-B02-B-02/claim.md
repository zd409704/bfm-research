# Claim C-B02-B-02

- **Author**: Author B (Codex gpt-6-astra)
- **Packet**: `B02`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Impossibility
- **Premises**: Fixed encoder weights, EMA input normalizer with 0 < alpha < 1, query batches varying mean over an open interval, and non-constant downstream prompt map.
- **Conclusion**: Updating running normalizer statistics during query forwards cannot preserve query-order and query-count invariance of downstream prompt encodings; freezing buffers or isolated evaluation state is necessary.
- **Falsifier**: An EMA normalizer with 0 < alpha < 1 and non-constant encoder that remains invariant under arbitrary train-mode query insertions.

# Claim C-B05-A-02

- **Author**: Author A (Claude Opus)
- **Packet**: `B05`
- **State & Grade**: Grade 1 (Candidate, tighten-premises)
- **Conclusion Shape**: Transactional Quarantine Obligation
- **Premises**: IEEE-754 floating-point arithmetic and uncheckpointed in-place running mean/variance normalizer or Gram EMA updates.
- **Conclusion**: Any transition exhibiting NaN/Inf or verified solver corruption in any substep j in {1..4} or post-step final audit must be quarantined prior to normalizer, Gram, and replay writes.
- **Falsifier**: An unquarantined in-place IEEE-754 EMA normalizer update that ingests a NaN/Inf substep while preserving finite moments.

# Consanguinity Algorithm

This document details the computation of the inbreeding (consanguinity) coefficient F used by GeneWeb (`consang` and `gwc -cg`).

## Purpose

For each person P, compute probability that the two alleles at a random autosomal locus are identical by descent (IBD). Stored as a rational (often scaled float) in person record.

## Data Inputs

- Person → parents linkage (ascends + families arrays).
- Base assumption: founders (no parents) have F = 0.
- Optionally existing cached values (incremental mode) unless `-scratch`.

## High-Level Steps

1. Build ancestry graph (directed edges from person to parents).
2. Topologically sort graph (parents before child) — detect cycles.
3. Iterate persons in topological order computing F.
4. Persist results (patch persons array) and sync.

## Cycle Detection

If a person appears as their own ancestor (via improper loop) a cycle exists — algorithm raises `TopologicalSortError` and tool terminates. Run `gwfixbase` to repair structure first.

## Formula

For person P with parents A and B:

```
F(P) = (1/2) * r(A,B) * (1 + F(A) + F(B)) / 2
```

where r(A,B) is coefficient of relationship between A and B (probability of IBD allele pick), or more commonly expressed via kinship coefficient φ(A,B):

```
F(P) = φ(A,B)
φ(X,Y) = Σ ( (1/2)^(n1 + n2 + 1) * (1 + F(C)) ) over all common ancestors C
```

GeneWeb effectively computes kinship through recursive memoization over ancestor paths. Optimization: dynamic programming stores partial kinship evaluations to avoid exponential explosion.

Simplified recurrence used in many implementations:

```
If A == B: F(P) = (1 + 2*F(A)) / 2  (selfed parent case, rare in human data)
Else F(P) = 0.5 * (F(A) + F(B)) + 0.25 * r(A,B)
```

Implementation details may vary slightly; consult `ConsangAll` for exact constants.

## Complexity

Let n = persons, a = average ancestors depth visited.
Worst-case naive O(n * a^2) if no memoization; practical code reduces to near O(n * a) with caching.

## Incremental vs Scratch

- Incremental (default): only recomputes where necessary (e.g., new persons) if dependency graph unchanged.
- Scratch (`-scratch`): recompute all, ignoring stored values.

## Options Impact

| Option | Effect |
|--------|--------|
| `-fast` | Preload arrays (persons/families/ascends/unions/couples/descends/strings) to reduce random IO. |
| `-scratch` | Ignore existing consanguinity, recompute from zero baseline. |
| `-mem` | Memory saving strategy (affects patching strategy). |
| `-q` / `-qq` | Reduce verbosity; may skip progress prints. |
| `-nolock` | Skip lock (unsafe). |

## Numerical Representation

Legacy code often stores F as integer scaled (e.g., per 1e6) or float; ensure downstream formatting interprets consistently. Avoid cumulative float drift by computing from parents freshly rather than iterative scaling updates.

## Validation Suggestions

- Founders have F=0.
- Children of unrelated parents: F ≈ (F(A)+F(B))/2 (usually 0 first generation).
- First-cousin marriage child: expected F ≈ 0.0625.
- Double first-cousin: F ≈ 0.125.

## Potential Improvements

- Store kinship matrix sparsely for reuse (costly memory though).
- Parallelize per-topo-layer; current global refs may hinder.
- Add checksum or version tag to detect stale cached F after structure edits.

## Troubleshooting

| Symptom | Cause | Action |
|---------|-------|--------|
| Cycle error | Structural loop | Run `gwfixbase`. |
| All zeros | Parents unresolved or scratch on founder-only set | Verify parent links. |
| Unexpected high F | Data duplication or incorrect parent assignment | Inspect unions, run diff vs source. |

See also: `algorithms/overview.md` (section 2).

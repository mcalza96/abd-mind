# abd-bench — 40 boundary cases for abductive reasoning

Base: `Notes/Research/abd-bench/`. Thesis: y_i = π_Oi(S).

## Files (40 cases + rejected)

- 01-scientific-discovery.md — A01-A08: Neptune, neutrino, ozone TOMS/Dobson, pulsars, CMB, Mercury/Vulcan, H. pylori, Earth age K-Ar
- 02-failed-postulates.md — B01-B08: Vulcan, N-rays, polywater, OPERA, phlogiston, caloric, Mars canals, cold fusion
- 03-medical-forensic.md — C01-C08: Tylenol 1982, Therac-25, Challenger, AF447, Broad St cholera, Semmelweis, thalidomide, Legionnaires
- 04-earth-history.md — D01-D08: Vela 1979, Scorpion, Tunguska, 1906 quake, magnetic stripes, tide-vs-GPS, GW150914, Cuba U-2
- 05-perception-rejected-index.md — E01-E08: dress, McGurk, rubber hand, gorilla, blind spot, phantom limb, bat echolocation, pit-viper IR + 14 rejected + master index
- dataset.json — structured E01-E08 only (A-D remain in MD; full structuring left for Fase 2)

## Spec per case

Observers/frames, surface conflict, latent H with per-observer mapping, wrong inductive answer, independent ground truth + URLs, defeasible + ontological flags.

## Verified

- All 5 files on disk, IDs A01-A08/B01-B08/C01-C08/D01-D08/E01-E08 present (grep).
- B slice URLs curl-verified 200 (11 wiki + nature + NASA); others use real wiki/institutional slugs, not live-verified each.
- qe verify pass; budget 20/20 left.

## Left / weak

- A URLs from memory (trusted slugs, not curl-checked); E single-source each, terse spec.
- D01 Vela + D02/D03 carry residual dispute flags (declared in file).
- E01/E02/E04 famous = contamination risk (measure memory, not abduction); cleanest: E07/E08, most of D, A03.
- No difficulty calibration; no full 40-case dataset.json yet.

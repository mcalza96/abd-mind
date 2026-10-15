# abd-bench / A — Scientific discovery (8 boundary cases)

Fase 1 (recolección). Sin análisis. Cada caso: observadores/frames, observaciones en conflicto, H latente + mapeo por observador, respuesta inductiva errónea, ground truth + fuentes.

---

## A01 — Uranus residuals / Neptune prediction

**Observers/frames:**
- O1: Optical astrometrists (Greenwich/Paris, 1820–1845). Frame: positional astronomy, Newtonian tables (Bouvard).
- O2: Celestial mechanicians (Le Verrier Paris / Adams Cambridge). Frame: inverse perturbation theory.

**Observations:**
- O1: Uranus longitude deviates ±~100 arcsec from Bouvard tables; residuals grow then shrink (Uranus early too fast, late too slow).
- O2: No new direct observation; computation: residuals fit a single exterior perturber (a ~ 38 AU, predicted longitude ~325–328 deg for 1846).

**Latent H + per-observer mapping:**
- H: an eighth planet (Neptune, ~30 AU, ~17 M_earth) perturbs Uranus.
- O1 saw residuals because they tracked Uranus alone against a 7-planet model; forward pull before conjunction then backward pull after explains sign flip.
- O2 inferred position because the same residual curve inverts to one exterior mass.

**Wrong inductive answer + why fails:**
- Average residuals to zero / add ad-hoc gravity-law tweak or blame star-catalog errors; majority (Airy delay) = "wait and re-observe". Fails: discards the signed time-structure that only an exterior body predicts; Galle found Neptune <1 deg from Le Verrier point on 1846-09-23.

**Ground truth + sources:**
- Neptune exists; found by Galle/d'Arrest from Le Verrier letter; Adams co-predictor.
- https://en.wikipedia.org/wiki/Discovery_of_Neptune
- https://en.wikipedia.org/wiki/Neptune
- https://en.wikipedia.org/wiki/Uranus

**Defeasible?** Yes — tables revisable; prediction defeated "no planet" consensus.
**Ontological expansion?** Yes — new planet added to inventory.

---

## A02 — Beta-decay continuum / neutrino

**Observers/frames:**
- O1: Beta spectroscopists (Meitner 1911, Ellis–Wooster 1927 calorimeter). Frame: energy spectroscopy, calorimeter heat = total electron energy.
- O2: Nuclear theorists (Pauli 1930, Fermi 1934). Frame: conservation laws + quantum statistics.

**Observations:**
- O1: electrons from a monoenergetic nuclear transition show a *continuous* spectrum with sharp endpoint, mean ~1/3 endpoint; calorimeter confirms missing energy is truly absent, not undetected electrons.
- O2: no instrument anomaly; logical anomaly: two-body decay n→p+e must be monoenergetic; continuum violates energy + angular momentum conservation.

**Latent H + per-observer mapping:**
- H: three-body decay n→p+e+antineutrino; invisible neutral spin-1/2 particle carries the difference.
- O1 saw continuum because detectors register only the electron share of shared energy.
- O2 saw contradiction because conservation + spin-counting demands the third particle (Pauli letter 1930); Fermi theory gives spectrum shape; Cowan–Reines 1956 detect inverse beta decay in delayed coincidence.

**Wrong inductive answer + why fails:**
- Average electron energies as "true" energy, or Bohr's "energy non-conservation in nucleus", or authority "calorimeter error". Fails: Ellis–Wooster closed the error loophole; endpoint tracks Q-value per isotope, so averaging destroys the spectrum-shape evidence.

**Ground truth + sources:**
- Antineutrino emitted in beta decay; Reines–Cowan detection 1956; Reines Nobel 1995.
- https://en.wikipedia.org/wiki/Neutrino
- https://en.wikipedia.org/wiki/Beta_decay
- https://en.wikipedia.org/wiki/Cowan%E2%80%93Reines_neutrino_experiment
- https://www.nobelprize.org/prizes/physics/1995/summary/

**Defeasible?** Yes — conservation retained by positing invisible entity (defeated Bohr's surrender).
**Ontological expansion?** Yes — new particle (neutrino sector).

---

## A03 — Antarctic ozone hole: TOMS satellite vs Dobson ground stations

**Observers/frames:**
- O1: NASA Nimbus-7 TOMS team (1978–1985). Frame: global satellite mapping + quality-flag pipeline.
- O2: British Antarctic Survey, Halley Bay Dobson spectrophotometer (Farman et al.). Frame: ground-based UV absorption, manual monthly means.

**Observations:**
- O1: October total ozone over Antarctica ~200+ DU, no trend; lowest values auto-flagged as instrument error and excluded.
- O2: October means falling ~300 DU (late 1970s) to ~180 DU (1984); spring depletion ~40%.

**Latent H + per-observer mapping:**
- H: heterogeneous chlorine chemistry on polar stratospheric cloud surfaces (CFC-derived Cl + polar vortex isolation) destroys spring ozone.
- O1 missed it because the flagging code treated unprecedented lows as bad data.
- O2 caught it because Dobson directly measures the absorption column with no plausibility filter; reprocessed TOMS then recovered the same hole.

**Wrong inductive answer + why fails:**
- Majority/authority: trust the satellite global mean ("Dobson single-station drift"). Fails: two independent Dobson stations (Halley, Syowa) + reprocessed TOMS agree; depletion is seasonal (spring) so annual averaging hides it.

**Ground truth + sources:**
- Farman, Gardiner, Shanklin 1985 Nature; NASA reprocessing confirmed; Montreal Protocol 1987.
- https://en.wikipedia.org/wiki/Ozone_depletion
- https://en.wikipedia.org/wiki/Montreal_Protocol
- https://en.wikipedia.org/wiki/Total_Ozone_Mapping_Spectrometer

**Defeasible?** Yes — satellite QC rule defeated by ground truth; pipeline patched.
**Ontological expansion?** No (mechanism recombination, no new entity class) — borderline yes for PSC-surface chemistry; marked No.

---

## A04 — Pulsars: scintillating radio source vs quiet optical sky (CP 1919)

**Observers/frames:**
- O1: Cambridge radio group (Bell Burnell/Hewish, interplanetary scintillation array, 1967). Frame: high-time-resolution radio chart records.
- O2: Optical/radio-continuum astronomers. Frame: deep plates + continuum surveys; "little green men" skepticism.

**Observations:**
- O1: sharp 1.337 s pulses from fixed RA/Dec, dispersion-swept, sidereal recurrence; "LGM-1".
- O2: nothing at that position: no variable star, no flare counterpart; continuum unremarkable.

**Latent H + per-observer mapping:**
- H: rotating magnetized neutron star; lighthouse beamed emission, period = spin.
- O1 saw pulses because 0.1-s time resolution + dispersion delay is the right projection for beamed radio.
- O2 saw nothing because optical continuum integrates over the pulse and the beam misses most lines of sight; steadiness is expected off-beam.

**Wrong inductive answer + why fails:**
- Average pulses into "scintillation noise" or majority "terrestrial interference/man-made"; authority "aliens" or "instrumental". Fails: sidereal (not solar) recurrence + cold-plasma dispersion law + second source (CP 1133) rule out local/artificial causes; Gold 1968 rotation model predicts spin-down.

**Ground truth + sources:**
- Hewish/Bell discovery; Gold neutron-star model; Hewish Nobel 1974; Vela/Crab spin-down confirmation.
- https://en.wikipedia.org/wiki/Pulsar
- https://en.wikipedia.org/wiki/PSR_B1919%2B21
- https://en.wikipedia.org/wiki/Jocelyn_Bell_Burnell

**Defeasible?** Yes — LGM/artefact hypotheses retracted within months.
**Ontological expansion?** Yes — neutron stars as observed class.

---

## A05 — CMB excess: Bell Labs horn vs Princeton cosmologists

**Observers/frames:**
- O1: Penzias/Wilson, Holmdel horn antenna engineers (1964–65). Frame: absolute radiometry at 4080 MHz; calibrate out every noise kelvin.
- O2: Dicke/Peebles/Roll/Wilkinson (Princeton). Frame: Big-Bang nucleosynthesis prediction of ~10 K relic blackbody.

**Observations:**
- O1: isotropic ~3.5 K excess antenna temperature, day/night/season independent; pigeon-cleaning changes nothing.
- O2: no measurement yet; prediction of a few-K sky background awaiting a Dicke radiometer.

**Latent H + per-observer mapping:**
- H: cosmic microwave background, z~1100 blackbody redshifted to ~2.7 K.
- O1 measured its Rayleigh–Jeans tail as irreducible excess because absolute calibration leaves no instrumental slot for it.
- O2 predicted the same bath from cosmology; the two 1965 ApJ papers (measurement + interpretation) close the loop; later FIRAS spectrum is Planckian.

**Wrong inductive answer + why fails:**
- Average residual into "unresolved ground/atmosphere loss" or authority "antenna defect". Fails: isotropy + spectrum + independence of pointing kill local explanations; COBE-FIRAS (1989–93) blackbody fit residuals <50 ppm.

**Ground truth + sources:**
- Penzias/Wilson ApJ 1965; Dicke et al. companion; Nobel 1978; COBE FIRAS.
- https://en.wikipedia.org/wiki/Cosmic_microwave_background
- https://en.wikipedia.org/wiki/Cosmic_Background_Explorer
- https://www.nobelprize.org/prizes/physics/1978/summary/

**Defeasible?** Yes — steady-state/no-relic view defeated by blackbody spectrum.
**Ontological expansion?** Yes — relic radiation as new cosmological component.

---

## A06 — Mercury perihelion excess / Vulcan

**Observers/frames:**
- O1: Meridian astrometrists (Le Verrier 1859 onward). Frame: transit/circle timings of Mercury.
- O2: Newtonian dynamicists (Le Verrier, Newcomb). Frame: N-body perturbations from known planets.

**Observations:**
- O1: perihelion advances ~574 arcsec/cy total; known-planet model accounts ~531; residual ~43 arcsec/cy.
- O2: Uranus-style solution predicts intra-Mercurial planet "Vulcan"; transient Vulcan sightings reported (Lescarbault 1859) but never recovered; Venus-mass adjustments fail.

**Latent H + per-observer mapping:**
- H: general-relativistic precession 6πGM/a(1−e²)c² ≈ 43 arcsec/cy; no new body.
- O1 measured correctly; the excess is real spacetime effect, largest for Mercury (deep potential + eccentricity).
- O2's Vulcan search failed because the frame (Newton + unseen mass) was wrong; GR (Einstein 1915) fits Mercury with no free planet, plus light-bending confirmation 1919.

**Wrong inductive answer + why fails:**
- Neptune-analogy induction ("another Vulcan") / average transits away / authority sightings. Fails: exhaustive searches (including 1878 eclipse) empty; Vulcan mass needed destabilizes; GR predicts exact 43 arcsec with zero new entities.

**Ground truth + sources:**
- Le Verrier 1859 anomaly; Newcomb 1895; Einstein 1915 GR explanation.
- https://en.wikipedia.org/wiki/Perihelion_precession_of_Mercury
- https://en.wikipedia.org/wiki/Vulcan_(hypothetical_planet)
- https://en.wikipedia.org/wiki/Tests_of_general_relativity

**Defeasible?** Yes — Vulcan posit defeated; Newtonian frame bounded.
**Ontological expansion?** Yes — curved spacetime replaces extra-body ontology (expansion of framework, contraction of inventory).

---

## A07 — Peptic ulcers: clinicians vs pathologists (H. pylori)

**Observers/frames:**
- O1: Gastroenterologists (1970s). Frame: endoscopy + acid/stress model; "stomach is sterile".
- O2: Pathologists Warren/Marshall (Perth, 1979–84). Frame: gastric biopsy histology + culture.

**Observations:**
- O1: ulcers correlate with acid/NSAIDs/stress; antibiotics irrelevant; recurrence after acid suppression.
- O2: curved bacteria on inflamed antral biopsies; culturable (Marshall's prolonged Easter incubation 1982); Marshall self-ingestion → gastritis → cure by antibiotics.

**Latent H + per-observer mapping:**
- H: Helicobacter pylori colonization causes chronic gastritis/ulcer; acid is cofactor not cause.
- O1 saw acid correlation because H. pylori damage + acid co-produce ulceration, and acid drugs mask without curing.
- O2 saw the agent because biopsy stains/culture project the hidden bacterial layer clinicians never sample.

**Wrong inductive answer + why fails:**
- Authority/majority: "stress + acid, treat acid" (average symptom scores). Fails: randomized antibiotic eradication cures and prevents recurrence; Koch-style fulfillment (ingestion, re-isolation); Nobel 2005.

**Ground truth + sources:**
- Warren/Marshall Lancet 1984; Nobel Medicine 2005.
- https://en.wikipedia.org/wiki/Helicobacter_pylori
- https://en.wikipedia.org/wiki/Peptic_ulcer_disease
- https://www.nobelprize.org/prizes/medicine/2005/summary/

**Defeasible?** Yes — sterile-stomach dogma retracted.
**Ontological expansion?** Yes — new pathogen class in gastric niche.

---

## A08 — Age of Earth: Kelvin cooling vs strata vs radiometric (K–Ar closure)

**Observers/frames:**
- O1: Kelvin/thermodynamicists (1860s). Frame: conductive cooling of a solid Earth → 20–100 Myr.
- O2: Stratigraphers/uniformitarians (Lyell, Joly sediment budgets). Frame: sedimentation/erosion rates → hundreds of Myr–Gyr.
- O3: Radiochemists (Rutherford, Boltwood; later K–Ar: ⁴⁰K→⁴⁰Ar, t½ 1.25 Gyr). Frame: parent/daughter clocks in closed minerals.

**Observations:**
- O1: heat-flow math consistent ~100 Myr max.
- O2: field sections demand ≫100 Myr.
- O3 (the K–Ar twist): some young lavas give anomalously *old* K–Ar ages (excess ⁴⁰Ar trapped in phenocrysts/xenoliths) while whole-rock/⁴⁰Ar–³⁹Ar plateaus give young concordant ages.

**Latent H + per-observer mapping:**
- H: Earth ~4.54 Gyr with internal radiogenic heat; K–Ar clock dates *closure/degassing*, and excess mantle ⁴⁰Ar contaminates phenocrysts.
- O1 under-read because the cooling model omitted radiogenic heating (Rutherford 1904 lecture).
- O2 over-flexible but directionally right; lacked a clock.
- O3 discordance resolves per-sample: whole-rock/step-heating separates trapped vs radiogenic ⁴⁰Ar (isochron intercept at non-atmospheric ⁴⁰Ar/³⁶Ar flags excess).

**Wrong inductive answer + why fails:**
- Average the three clocks, or authority-rule for Kelvin ("physics beats geology"), or average mineral separates with whole rock. Fails: averaging mixes open/closed systems; physics frame was missing a heat term; excess-argon isochrons diagnose contamination instead of hiding it.

**Ground truth + sources:**
- Patterson Pb–Pb 4.55 Gyr; Dalrymple K–Ar/⁴⁰Ar–³⁹Ar systematics including excess argon.
- https://en.wikipedia.org/wiki/Age_of_Earth
- https://en.wikipedia.org/wiki/Potassium-argon_dating
- https://en.wikipedia.org/wiki/Excess_argon

**Defeasible?** Yes — Kelvin age and naïve K–Ar dates both revisable (closure + excess-Ar diagnostics).
**Ontological expansion?** Yes — radioactivity as heat source + deep-time chronometer.

---

*Fuentes mínimas por caso: 2+ URLs reales arriba (wikipedia/nobelprize). Fase 2 pendiente: trade-offs, calibración de dificultad, flags de uso en benchmark.*

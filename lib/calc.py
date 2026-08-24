"""Real bearing-capacity/settlement calculation engine — deterministic Python, not an LLM guess.

Primary application (permanent building foundation support): Terzaghi/Meyerhof bearing capacity
+ Schmertmann/elastic settlement, per PRD §4.2(a) / KCS 11 30 10 / MOLIT 구조물기초설계기준 Ch.4.
These are standard, publicly documented textbook methods (Terzaghi 1943, Meyerhof 1963,
Schmertmann 1970) implemented rigorously.

Additional application (temporary tracked-plant platform): BR470/TWf-style LSF check, per PRD
§4.2(b). BR470 itself is a paid BRE/TWf publication we don't have verbatim in this repo — the
punching-shear resistance term here is a defensible simplified model (vertical-plane friction
resistance through the aggregate), not a reproduction of BR470's exact clause-by-clause method.
Treat this application's numbers as more indicative than the primary application's.

Geocell (하이셀/구속셀) reinforcement: the aggregate-cap contribution (raising the effective
founding level, using the aggregate's own friction angle) is computed rigorously using the same
Meyerhof/Terzaghi theory. The geocell CONFINEMENT increment is not fabricated — it requires a
manufacturer-certified coefficient; if not supplied, it's treated as zero (conservative) with an
explicit note, not silently guessed.

Every function here is pure (no I/O, no Streamlit) so it can be unit-tested independently of the
UI.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

GAMMA_WATER = 9.81  # kN/m^3


# ---------------------------------------------------------------------------
# Bearing capacity factors
# ---------------------------------------------------------------------------

def bearing_capacity_factors(phi_deg: float) -> tuple[float, float, float]:
    """Nc, Nq, Ngamma for friction angle phi_deg (degrees).

    Nq (Reissner) and Nc = (Nq-1)*cot(phi) are the widely-tabulated forms shared across
    Terzaghi/Meyerhof/Hansen/Vesic in most modern references (incl. 구조물기초설계기준해설).
    Ngamma uses the common Meyerhof/Vesic closed form 2*(Nq+1)*tan(phi) — historical Terzaghi
    Ngamma was graphical with no closed form and varies by textbook; this is a defensible,
    commonly-cited approximation, not a specific textbook's exact tabulated digit.
    """
    if phi_deg <= 0:
        return 5.14, 1.0, 0.0
    phi = math.radians(phi_deg)
    nq = math.exp(math.pi * math.tan(phi)) * math.tan(math.radians(45) + phi / 2) ** 2
    nc = (nq - 1) / math.tan(phi)
    ngamma = 2 * (nq + 1) * math.tan(phi)
    return nc, nq, ngamma


def meyerhof_shape_depth_factors(phi_deg: float, B: float, L: float, Df: float) -> dict:
    """Meyerhof shape (sc, sq, sg) and depth (dc, dq, dg) factors. B <= L assumed."""
    if phi_deg <= 0:
        kp = 1.0
        sc = 1 + 0.2 * (B / L)
        sq = sg = 1.0
        dc = 1 + 0.2 * (Df / B)
        dq = dg = 1.0
    else:
        phi = math.radians(phi_deg)
        kp = math.tan(math.radians(45) + phi / 2) ** 2
        sc = 1 + 0.2 * kp * (B / L)
        sq = sg = 1 + 0.1 * kp * (B / L)
        dc = 1 + 0.2 * math.sqrt(kp) * (Df / B)
        dq = dg = 1 + 0.1 * math.sqrt(kp) * (Df / B)
    return {"sc": sc, "sq": sq, "sg": sg, "dc": dc, "dq": dq, "dg": dg}


# ---------------------------------------------------------------------------
# Groundwater correction (standard 3-case Dw-vs-Df method)
# ---------------------------------------------------------------------------

def groundwater_correction(gamma: float, Df: float, B: float, Dw: float | None) -> tuple[float, float]:
    """Returns (q, gamma_eff): effective overburden at founding level (for the Nq term) and
    effective unit weight below the footing (for the Ngamma term), corrected for groundwater.
    Dw=None means groundwater not encountered / far below (no correction)."""
    gamma_sub = max(gamma - GAMMA_WATER, 0.1)
    if Dw is None or Dw >= Df + B:
        return gamma * Df, gamma
    if Dw >= Df:
        frac = (Dw - Df) / B
        gamma_eff = gamma_sub + frac * (gamma - gamma_sub)
        return gamma * Df, gamma_eff
    q = gamma * Dw + gamma_sub * (Df - Dw)
    return q, gamma_sub


# ---------------------------------------------------------------------------
# Bearing capacity — Terzaghi (no shape/depth factors) and Meyerhof (with them)
# ---------------------------------------------------------------------------

@dataclass
class BearingInputs:
    c: float          # kPa
    phi_deg: float     # degrees
    gamma: float       # kN/m^3
    B: float           # m
    L: float           # m
    Df: float          # m
    Dw: float | None = None  # m, depth to groundwater; None = not encountered


@dataclass
class BearingResult:
    qu_terzaghi: float
    qu_meyerhof: float
    qu_governing: float
    method_governing: str
    qa: float  # qu_governing / 3


def compute_bearing_capacity(inp: BearingInputs) -> BearingResult:
    nc, nq, ng = bearing_capacity_factors(inp.phi_deg)
    q, gamma_eff = groundwater_correction(inp.gamma, inp.Df, inp.B, inp.Dw)

    qu_terzaghi = inp.c * nc + q * nq + 0.5 * gamma_eff * inp.B * ng

    f = meyerhof_shape_depth_factors(inp.phi_deg, inp.B, inp.L, inp.Df)
    qu_meyerhof = (
        inp.c * nc * f["sc"] * f["dc"]
        + q * nq * f["sq"] * f["dq"]
        + 0.5 * gamma_eff * inp.B * ng * f["sg"] * f["dg"]
    )

    if qu_terzaghi <= qu_meyerhof:
        qu_gov, method = qu_terzaghi, "Terzaghi"
    else:
        qu_gov, method = qu_meyerhof, "Meyerhof"

    return BearingResult(
        qu_terzaghi=qu_terzaghi,
        qu_meyerhof=qu_meyerhof,
        qu_governing=qu_gov,
        method_governing=method,
        qa=qu_gov / 3.0,
    )


# ---------------------------------------------------------------------------
# Settlement — Schmertmann (2B/axisymmetric method, single representative E) + elastic theory
# ---------------------------------------------------------------------------

@dataclass
class SettlementInputs:
    q_applied: float   # kPa, gross applied pressure
    B: float           # m
    Df: float          # m
    gamma: float       # kN/m^3, for overburden at founding level
    E: float           # kN/m^2, representative subgrade modulus over the influence zone
    nu: float = 0.3
    Is: float = 0.85   # elastic-theory influence factor (simplified, user-adjustable)
    time_years: float = 30.0
    Dw: float | None = None
    n_sublayers: int = 40


def schmertmann_settlement(inp: SettlementInputs) -> float:
    """2B-depth (square/axisymmetric) strain-influence method, single representative E.
    Returns settlement in mm. Simplification vs. a real layered profile — see module docstring."""
    q_v0, _ = groundwater_correction(inp.gamma, inp.Df, inp.B, inp.Dw)
    q_net = max(inp.q_applied - q_v0, 0.0)
    if q_net <= 0 or inp.E <= 0:
        return 0.0

    depth_influence = 2 * inp.B
    dz = depth_influence / inp.n_sublayers
    iz_peak = 0.5 + 0.1 * math.sqrt(q_net / max(q_v0, 1.0))
    z_peak = inp.B / 2

    total = 0.0
    for i in range(inp.n_sublayers):
        z = (i + 0.5) * dz
        if z <= z_peak:
            iz = 0.1 + (iz_peak - 0.1) * (z / z_peak) if z_peak > 0 else iz_peak
        else:
            iz = iz_peak * (depth_influence - z) / (depth_influence - z_peak)
        iz = max(iz, 0.0)
        total += iz * dz / inp.E  # meters, since E in kN/m^2 and dz in m

    c1 = max(1 - 0.5 * (q_v0 / q_net), 0.5)
    c2 = 1 + 0.2 * math.log10(max(inp.time_years, 0.1) / 0.1)

    settlement_m = c1 * c2 * q_net * total
    return settlement_m * 1000  # mm


def elastic_settlement(inp: SettlementInputs) -> float:
    """Immediate elastic settlement, mm."""
    q_v0, _ = groundwater_correction(inp.gamma, inp.Df, inp.B, inp.Dw)
    q_net = max(inp.q_applied - q_v0, 0.0)
    if q_net <= 0 or inp.E <= 0:
        return 0.0
    s_m = q_net * inp.B * (1 - inp.nu**2) / inp.E * inp.Is
    return s_m * 1000  # mm


# ---------------------------------------------------------------------------
# Primary application — full orchestration (bearing + settlement, with optional aggregate/geocell)
# ---------------------------------------------------------------------------

@dataclass
class PrimaryCalcInputs:
    # Subgrade
    c: float
    phi_deg: float
    gamma: float
    E: float
    Dw: float | None
    # Footing / load
    B: float
    L: float
    Df: float
    q_applied: float
    settlement_limit_mm: float = 25.4
    nu: float = 0.3
    Is: float = 0.85
    time_years: float = 30.0
    # Aggregate cap (Pebble-Tech) — 0 = none. Modeled as LOAD SPREAD (see note below), not as a
    # substitute bearing stratum — see module docstring / run_primary_calc for why.
    aggregate_thickness_m: float = 0.0
    spread_angle_deg: float = 26.57  # 2V:1H, standard conservative granular-fill spread assumption
    # Geocell — None / "하이셀 (1.2mm)" / "구속셀 (1.6mm)". Adds spread depth (its own height) plus
    # an optional manufacturer-certified confinement increment (kPa) added to native qa — 0 if
    # not supplied (conservative, never guessed).
    geocell_product: str | None = None
    geocell_height_m: float = 0.0
    geocell_confinement_increment_kpa: float = 0.0


@dataclass
class PrimaryCalcResult:
    unreinforced: BearingResult
    qa_allowable: float               # unreinforced qa1 + any geocell confinement increment
    effective_pressure_at_base: float  # q_applied spread through aggregate+geocell to native subgrade
    settlement_schmertmann_mm: float
    settlement_elastic_mm: float
    settlement_governing_mm: float
    bearing_pass: bool
    settlement_pass: bool
    overall_pass: bool
    notes: list[str] = field(default_factory=list)


def run_primary_calc(inp: PrimaryCalcInputs) -> PrimaryCalcResult:
    """Bearing check for the reinforced case uses LOAD SPREAD, not a substituted-material bearing
    re-run. An earlier version of this function re-ran the full Meyerhof/Terzaghi formula using
    the aggregate's own (high) friction angle over the full footing width — that assumes an
    infinitely thick homogeneous mass of that material, which is wrong for a 100-300mm veneer
    over weak native soil (the self-weight term 0.5*gamma*B*Ngamma explodes when a high-phi
    material's Ngamma is multiplied by a wide B, giving nonsensical thousands-of-kPa results).
    Caught by testing against the real Gwangju BH-1 case (knowledge/design-worked-examples.md
    SS C) — see git history for the defect this replaced.

    Correct treatment: the aggregate/geocell system spreads the applied pressure over an
    enlarged effective footprint by the time it reaches native subgrade (standard granular-fill
    load-spread design philosophy, e.g. 2V:1H). Native subgrade is checked against this REDUCED
    effective pressure using its OWN (unchanged) bearing capacity — not an inflated qa."""
    notes: list[str] = []

    unreinforced = compute_bearing_capacity(
        BearingInputs(inp.c, inp.phi_deg, inp.gamma, inp.B, inp.L, inp.Df, inp.Dw)
    )

    total_spread_depth = inp.aggregate_thickness_m + inp.geocell_height_m
    if total_spread_depth > 0:
        spread = total_spread_depth * math.tan(math.radians(inp.spread_angle_deg))
        B_eff = inp.B + 2 * spread
        L_eff = inp.L + 2 * spread
        effective_pressure = inp.q_applied * (inp.B * inp.L) / (B_eff * L_eff)
    else:
        effective_pressure = inp.q_applied

    qa_allowable = unreinforced.qa
    if inp.geocell_product:
        if inp.geocell_confinement_increment_kpa <= 0:
            notes.append(
                f"Geocell ({inp.geocell_product}) selected but no manufacturer-certified "
                "confinement increment supplied — treated as 0 kPa additional (conservative, "
                "ignores real capacity). Get the certified confinement coefficient from the "
                "product datasheet before finalizing a real design."
            )
        qa_allowable += inp.geocell_confinement_increment_kpa

    settlement_inputs = SettlementInputs(
        q_applied=inp.q_applied, B=inp.B, Df=inp.Df, gamma=inp.gamma, E=inp.E,
        nu=inp.nu, Is=inp.Is, time_years=inp.time_years, Dw=inp.Dw,
    )
    s_schmertmann = schmertmann_settlement(settlement_inputs)
    s_elastic = elastic_settlement(settlement_inputs)
    s_governing = max(s_schmertmann, s_elastic)
    if total_spread_depth > 0:
        notes.append(
            "Settlement is NOT reduced for the aggregate/geocell layer in this calculator — it "
            "uses the same native-subgrade settlement regardless of reinforcement. A real "
            "reinforced-case settlement is lower than shown here (the reinforced layer itself is "
            "stiff and the spread reduces net pressure reaching the compressible subgrade); "
            "treat the settlement number as conservative/upper-bound when reinforcement is used."
        )

    bearing_pass = qa_allowable >= effective_pressure
    settlement_pass = s_governing <= inp.settlement_limit_mm

    return PrimaryCalcResult(
        unreinforced=unreinforced,
        qa_allowable=qa_allowable,
        effective_pressure_at_base=effective_pressure,
        settlement_schmertmann_mm=s_schmertmann,
        settlement_elastic_mm=s_elastic,
        settlement_governing_mm=s_governing,
        bearing_pass=bearing_pass,
        settlement_pass=settlement_pass,
        overall_pass=bearing_pass and settlement_pass,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Additional application — BR470-style LSF check (SIMPLIFIED / INDICATIVE — see module docstring)
# ---------------------------------------------------------------------------

@dataclass
class LsfInputs:
    q0_static: float          # kPa, manufacturer static contact pressure
    k_dyn: float               # dynamic/pitching factor, typ. 1.1-1.3
    B: float                   # m, track/outrigger pad width
    L: float                   # m, pad length
    thickness: float           # m, platform thickness (aggregate)
    aggregate_phi_deg: float   # degrees, typ. 40-45
    aggregate_gamma: float     # kN/m^3
    subgrade_cu: float         # kPa, undrained shear strength


@dataclass
class LsfResult:
    applied_pressure: float
    punching_shear_resistance: float
    subgrade_bearing_resistance: float
    lsf: float


def compute_lsf(inp: LsfInputs) -> LsfResult:
    """SIMPLIFIED / INDICATIVE implementation of the BR470-style LSF check. Punching-shear
    resistance is modeled as vertical-plane friction through the aggregate perimeter
    (conservative vertical-sided plane, theta=0), not BR470's exact published method — verify
    against the full BR470/TWf method or the company's own calc package before relying on this
    for a real platform."""
    applied = inp.q0_static * inp.k_dyn

    perimeter = 2 * (inp.B + inp.L)
    footprint = inp.B * inp.L
    phi = math.radians(inp.aggregate_phi_deg)
    # Average vertical effective stress on the punching-shear plane (triangular distribution
    # over the platform thickness), mobilizing friction (c'=0 for unbound aggregate).
    sigma_avg = 0.5 * inp.aggregate_gamma * inp.thickness
    tau = sigma_avg * math.tan(phi)
    punching_resistance = (perimeter * inp.thickness * tau) / footprint

    nc, _, _ = bearing_capacity_factors(0.0)  # undrained subgrade, phi=0 -> Nc=5.14
    subgrade_resistance = nc * inp.subgrade_cu

    lsf = (punching_resistance + subgrade_resistance) / applied if applied > 0 else 0.0

    return LsfResult(
        applied_pressure=applied,
        punching_shear_resistance=punching_resistance,
        subgrade_bearing_resistance=subgrade_resistance,
        lsf=lsf,
    )


def solve_thickness_for_target_lsf(
    base_inputs: LsfInputs, target_lsf: float, max_thickness: float = 2.0, step: float = 0.01
) -> float | None:
    """Increment thickness until target LSF is met. Returns None if not achievable within
    max_thickness (caller should treat as 'exceeds practical range, reconsider aggregate-only')."""
    t = step
    while t <= max_thickness:
        inp = LsfInputs(**{**base_inputs.__dict__, "thickness": t})
        if compute_lsf(inp).lsf >= target_lsf:
            return t
        t += step
    return None

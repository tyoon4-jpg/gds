import streamlit as st

from lib import calc

st.title(":material/calculate: Design calculator")
st.caption(
    "Real formulas, computed live — not an LLM guess. For preliminary/interactive sizing only; "
    "a licensed 토질 및 기초기술사 must issue the stamped calculation before construction."
)

application = st.segmented_control(
    "Application",
    ["Primary — building foundation", "Additional — temporary tracked-plant platform"],
    default="Primary — building foundation",
    key="calc_application",
)

if application is None:
    st.info("Pick an application above to start.")
    st.stop()

# ============================================================================
# PRIMARY APPLICATION
# ============================================================================
if application == "Primary — building foundation":
    st.info(
        "Uses Terzaghi + Meyerhof bearing capacity (lowest governs, allowable = qu ÷ 3) and "
        "Schmertmann + elastic settlement (larger governs) — standard textbook methods, "
        "implemented directly. See PRD §4.2(a).",
        icon=":material/verified:",
    )

    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**Footing / load**")
            B = st.number_input("Width B (m)", 0.5, 50.0, 5.0, 0.1, key="p_B")
            L = st.number_input("Length L (m)", 0.5, 100.0, 8.0, 0.1, key="p_L")
            Df = st.number_input("Founding depth Df (m)", 0.0, 10.0, 0.65, 0.05, key="p_Df")
            q_applied = st.number_input("Design bearing pressure q0 (kPa)", 1.0, 2000.0, 150.0, 5.0, key="p_q")

        with st.container(border=True, width="stretch"):
            st.markdown("**Subgrade**")
            c = st.number_input("Cohesion c (kPa)", 0.0, 500.0, 0.0, 1.0, key="p_c")
            phi = st.number_input("Friction angle φ (°)", 0.0, 45.0, 21.0, 0.5, key="p_phi")
            gamma = st.number_input("Unit weight γ (kN/m³)", 10.0, 25.0, 18.0, 0.5, key="p_gamma")
            has_gw = st.checkbox("Groundwater encountered", value=True, key="p_has_gw")
            Dw = st.number_input("Depth to groundwater Dw (m)", 0.0, 50.0, 3.2, 0.1, key="p_Dw") if has_gw else None

        with st.container(border=True, width="stretch"):
            st.markdown("**Settlement**")
            E = st.number_input("Subgrade modulus E (kN/m²)", 1000.0, 300000.0, 9000.0, 500.0, key="p_E")
            nu = st.number_input("Poisson's ratio ν", 0.1, 0.5, 0.3, 0.01, key="p_nu")
            Is = st.number_input("Elastic influence factor Is", 0.3, 2.0, 0.85, 0.01, key="p_Is")
            time_years = st.number_input("Design life for creep correction (yr)", 1.0, 100.0, 30.0, 1.0, key="p_t")
            settlement_limit = st.number_input("Settlement limit (mm)", 5.0, 200.0, 25.4, 0.5, key="p_lim")

    st.warning(
        "Settlement uses a **single representative E** across the full 2B depth of influence. "
        "If the real subgrade profile stiffens with depth (common — E often increases from fill "
        "to weathered rock), this will **overestimate** settlement. Enter a weighted-average E "
        "for a closer estimate, or treat this number as conservative-indicative only.",
        icon=":material/info:",
    )

    st.markdown("### Reinforcement (optional)")
    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**Aggregate cap (페블테크)**")
            agg_t = st.number_input("Cap thickness (m)", 0.0, 2.0, 0.0, 0.05, key="p_agg_t")
            agg_phi = st.number_input("Aggregate φ' (°)", 30.0, 50.0, 45.0, 1.0, key="p_agg_phi")
            agg_gamma = st.number_input("Aggregate γ (kN/m³)", 15.0, 25.0, 20.0, 0.5, key="p_agg_gamma")

        with st.container(border=True, width="stretch"):
            st.markdown("**Geocell (하이셀/구속셀)**")
            geocell = st.selectbox("Product", [None, "하이셀 (1.2mm HDPE)", "구속셀 (1.6mm HDPE)"], key="p_geocell")
            gfr = st.number_input(
                "Manufacturer-certified confinement increment (kPa)", 0.0, 500.0, 0.0, 5.0,
                key="p_gfr",
                help="From the geocell product's certified datasheet. Left at 0 = conservative "
                     "(ignores real capacity) — do not guess a number here.",
            )
            if geocell and gfr == 0:
                st.caption(":orange[No certified value entered — increment treated as 0.]")

    inputs = calc.PrimaryCalcInputs(
        c=c, phi_deg=phi, gamma=gamma, E=E, Dw=Dw,
        B=B, L=L, Df=Df, q_applied=q_applied, settlement_limit_mm=settlement_limit,
        nu=nu, Is=Is, time_years=time_years,
        aggregate_thickness_m=agg_t, aggregate_phi_deg=agg_phi, aggregate_gamma=agg_gamma,
        geocell_product=geocell, geocell_confinement_increment_kpa=gfr,
    )
    result = calc.run_primary_calc(inputs)

    st.markdown("### Result")
    with st.container(horizontal=True):
        st.metric(
            "Allowable bearing capacity qa",
            f"{result.qa_final:.1f} kPa",
            f"{result.qa_final - q_applied:+.1f} vs. applied",
            border=True,
        )
        st.metric(
            "Governing settlement",
            f"{result.settlement_governing_mm:.1f} mm",
            f"{result.settlement_governing_mm - settlement_limit:+.1f} vs. limit",
            border=True,
            delta_color="inverse",
        )
        st.metric(
            "Overall",
            "PASS" if result.overall_pass else "N.G.",
            border=True,
        )

    with st.expander("Calculation detail"):
        st.markdown(f"**Unreinforced (original ground):** Terzaghi qu = {result.unreinforced.qu_terzaghi:.1f} kPa, "
                    f"Meyerhof qu = {result.unreinforced.qu_meyerhof:.1f} kPa — governing: "
                    f"**{result.unreinforced.method_governing}**, qa1 = {result.unreinforced.qa:.1f} kPa")
        if result.with_aggregate:
            st.markdown(f"**With aggregate cap** (founding level raised, φ'={agg_phi}°): "
                        f"Terzaghi qu = {result.with_aggregate.qu_terzaghi:.1f} kPa, "
                        f"Meyerhof qu = {result.with_aggregate.qu_meyerhof:.1f} kPa — governing: "
                        f"**{result.with_aggregate.method_governing}**, qa2 = {result.with_aggregate.qa:.1f} kPa")
        if geocell:
            st.markdown(f"**+ Geocell confinement increment:** {gfr:.1f} kPa")
        st.markdown(f"**Final allowable bearing capacity qa:** {result.qa_final:.1f} kPa "
                    f"{'≥' if result.bearing_pass else '<'} applied {q_applied:.1f} kPa → "
                    f"{'**PASS**' if result.bearing_pass else '**N.G.**'}")
        st.markdown("---")
        st.markdown(f"**Schmertmann settlement:** {result.settlement_schmertmann_mm:.1f} mm")
        st.markdown(f"**Elastic settlement:** {result.settlement_elastic_mm:.1f} mm")
        st.markdown(f"**Governing (larger):** {result.settlement_governing_mm:.1f} mm "
                    f"{'≤' if result.settlement_pass else '>'} limit {settlement_limit:.1f} mm → "
                    f"{'**PASS**' if result.settlement_pass else '**N.G.**'}")
        for note in result.notes:
            st.caption(f":orange[Note: {note}]")

# ============================================================================
# ADDITIONAL APPLICATION
# ============================================================================
else:
    st.warning(
        "**Simplified / indicative implementation.** BR470/TWf is a paid BRE/TWf publication "
        "not reproduced in this repo — the punching-shear term below is a defensible "
        "approximation (vertical-plane friction through the aggregate), not BR470's exact "
        "method. Use for order-of-magnitude estimation only; verify against a full BR470/TWf "
        "calculation before finalizing a real temporary platform. See PRD §4.2(b).",
        icon=":material/warning:",
    )

    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**Plant / load**")
            q0 = st.number_input("Static contact pressure q0 (kPa)", 1.0, 1000.0, 110.0, 5.0, key="a_q0")
            kdyn = st.number_input("Dynamic/pitching factor Kdyn", 1.0, 1.5, 1.15, 0.01, key="a_kdyn")
            Bp = st.number_input("Track/pad width B (m)", 0.2, 20.0, 0.8, 0.05, key="a_B")
            Lp = st.number_input("Track/pad length L (m)", 0.2, 20.0, 4.0, 0.05, key="a_L")

        with st.container(border=True, width="stretch"):
            st.markdown("**Subgrade / aggregate**")
            cu = st.number_input("Subgrade undrained Cu (kPa)", 1.0, 500.0, 25.0, 1.0, key="a_cu")
            agg_phi2 = st.number_input("Aggregate φ' (°)", 30.0, 50.0, 45.0, 1.0, key="a_agg_phi")
            agg_gamma2 = st.number_input("Aggregate γ (kN/m³)", 15.0, 25.0, 20.0, 0.5, key="a_agg_gamma")

        with st.container(border=True, width="stretch"):
            st.markdown("**Target**")
            target_lsf = st.number_input("Target LSF", 1.0, 2.0, 1.25, 0.05, key="a_target")
            solve_mode = st.checkbox("Solve minimum thickness for target LSF", value=True, key="a_solve")
            manual_thickness = None
            if not solve_mode:
                manual_thickness = st.number_input("Platform thickness (m)", 0.05, 2.0, 0.4, 0.01, key="a_thick")

    base = calc.LsfInputs(
        q0_static=q0, k_dyn=kdyn, B=Bp, L=Lp, thickness=manual_thickness or 0.4,
        aggregate_phi_deg=agg_phi2, aggregate_gamma=agg_gamma2, subgrade_cu=cu,
    )

    if solve_mode:
        solved = calc.solve_thickness_for_target_lsf(base, target_lsf)
        if solved is None:
            st.error(
                f"No thickness up to 2.0m reaches LSF ≥ {target_lsf} with these inputs — "
                "subgrade is likely too soft for aggregate-only; consider geocell reinforcement "
                "(size that with `platform-design` in the chat, this calculator doesn't model "
                "geocell contribution for the additional application)."
            )
            st.stop()
        thickness = solved
        st.success(f"Minimum thickness for LSF ≥ {target_lsf}: **{thickness*1000:.0f} mm**")
    else:
        thickness = manual_thickness

    result = calc.compute_lsf(calc.LsfInputs(
        q0_static=q0, k_dyn=kdyn, B=Bp, L=Lp, thickness=thickness,
        aggregate_phi_deg=agg_phi2, aggregate_gamma=agg_gamma2, subgrade_cu=cu,
    ))

    st.markdown("### Result")
    with st.container(horizontal=True):
        st.metric("Applied pressure", f"{result.applied_pressure:.1f} kPa", border=True)
        st.metric("LSF", f"{result.lsf:.2f}", f"{result.lsf - target_lsf:+.2f} vs. target", border=True)
        st.metric("At thickness", f"{thickness*1000:.0f} mm", border=True)

    with st.expander("Calculation detail"):
        st.markdown(f"Applied pressure = q0 × Kdyn = {q0:.1f} × {kdyn:.2f} = **{result.applied_pressure:.1f} kPa**")
        st.markdown(f"Punching-shear resistance (simplified, vertical plane) = **{result.punching_shear_resistance:.1f} kPa**")
        st.markdown(f"Subgrade bearing resistance (Meyerhof, Nc=5.14 × Cu) = **{result.subgrade_bearing_resistance:.1f} kPa**")
        st.markdown(f"LSF = ({result.punching_shear_resistance:.1f} + {result.subgrade_bearing_resistance:.1f}) / "
                    f"{result.applied_pressure:.1f} = **{result.lsf:.2f}**")
        st.caption(
            "Target bands per PRD §4.2(b): ≥1.0 absolute minimum; ≥1.25 for piling-rig/crane "
            "platforms; ≥1.5 for soft/organic subgrade or excavation-edge condition."
        )

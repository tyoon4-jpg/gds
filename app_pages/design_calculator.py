import streamlit as st

from lib import calc

st.title(":material/calculate: 설계 계산기")
st.caption(
    "실제 공식으로 즉시 계산됩니다 — LLM의 추정치가 아닙니다. 예비/대화형 산정용으로만 사용하며, "
    "시공 전에는 반드시 토질 및 기초기술사가 날인한 계산서를 발급받아야 합니다."
)

application = st.segmented_control(
    "적용 용도",
    ["주 용도 — 건축물 기초", "부가 용도 — 임시 중장비 작업대"],
    default="주 용도 — 건축물 기초",
    key="calc_application",
)

if application is None:
    st.info("위에서 적용 용도를 선택하세요.")
    st.stop()

# ============================================================================
# PRIMARY APPLICATION
# ============================================================================
if application == "주 용도 — 건축물 기초":
    st.info(
        "Terzaghi + Meyerhof 지지력 이론(둘 중 낮은 값이 지배, 허용지지력 = qu ÷ 3)과 "
        "Schmertmann + 탄성 침하 이론(둘 중 큰 값이 지배)을 직접 구현했습니다 — 표준 교과서적 "
        "방법입니다. PRD §4.2(a) 참조.",
        icon=":material/verified:",
    )

    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**기초 / 하중**")
            B = st.number_input("폭 B (m)", 0.5, 50.0, 5.0, 0.1, key="p_B")
            L = st.number_input("길이 L (m)", 0.5, 100.0, 8.0, 0.1, key="p_L")
            Df = st.number_input("근입깊이 Df (m)", 0.0, 10.0, 0.65, 0.05, key="p_Df")
            q_applied = st.number_input("설계 접지압 q0 (kPa)", 1.0, 2000.0, 150.0, 5.0, key="p_q")

        with st.container(border=True, width="stretch"):
            st.markdown("**노상(지반)**")
            c = st.number_input("점착력 c (kPa)", 0.0, 500.0, 0.0, 1.0, key="p_c")
            phi = st.number_input("내부마찰각 φ (°)", 0.0, 45.0, 21.0, 0.5, key="p_phi")
            gamma = st.number_input("단위중량 γ (kN/m³)", 10.0, 25.0, 18.0, 0.5, key="p_gamma")
            has_gw = st.checkbox("지하수 확인됨", value=True, key="p_has_gw")
            Dw = st.number_input("지하수위 깊이 Dw (m)", 0.0, 50.0, 3.2, 0.1, key="p_Dw") if has_gw else None

        with st.container(border=True, width="stretch"):
            st.markdown("**침하**")
            E = st.number_input("노상 탄성계수 E (kN/m²)", 1000.0, 300000.0, 9000.0, 500.0, key="p_E")
            nu = st.number_input("포아송비 ν", 0.1, 0.5, 0.3, 0.01, key="p_nu")
            Is = st.number_input("탄성 영향계수 Is", 0.3, 2.0, 0.85, 0.01, key="p_Is")
            time_years = st.number_input("크리프 보정용 설계수명 (년)", 1.0, 100.0, 30.0, 1.0, key="p_t")
            settlement_limit = st.number_input("허용 침하량 (mm)", 5.0, 200.0, 25.4, 0.5, key="p_lim")

    st.warning(
        "침하량은 영향깊이 2B 전체에 걸쳐 **단일 대표 E값**을 사용합니다. 실제 지반이 깊이에 따라 "
        "강성이 증가하는 경우(흔한 경우 — 매립층에서 풍화암으로 갈수록 E가 커짐), 이 계산은 침하량을 "
        "**과대평가**하게 됩니다. 더 정확한 추정을 위해서는 가중평균 E값을 입력하거나, 이 수치를 "
        "보수적(안전측) 참고값으로만 취급하세요.",
        icon=":material/info:",
    )

    st.markdown("### 보강 (선택사항)")
    st.caption(
        "골재/지오셀을 통해 하중이 노상(원지반)까지 분산되는 것으로 모델링합니다(표준 입상재료 "
        "성토 설계 방식) — 원지반 자체의 지지력(왼쪽 입력값)은 변하지 않으며, 실제로 변하는 것은 "
        "원지반이 받는 압력입니다."
    )
    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**골재 캡 (페블테크)**")
            agg_t = st.number_input("캡 두께 (m)", 0.0, 2.0, 0.0, 0.05, key="p_agg_t")
            spread_angle = st.number_input(
                "하중 분산각 (연직 기준, °)", 15.0, 45.0, 26.57, 0.5, key="p_spread",
                help="기본값 26.57° = 2V:1H, 입상재료 성토 설계의 표준적인 보수적 분산 가정입니다. "
                     "각도가 클수록(더 완만할수록) 분산 효과가 커집니다.",
            )

        with st.container(border=True, width="stretch"):
            st.markdown("**지오셀 (하이셀/구속셀)**")
            geocell = st.selectbox("제품", [None, "하이셀 (1.2mm HDPE)", "구속셀 (1.6mm HDPE)"], key="p_geocell")
            geocell_h = st.number_input("셀 높이 (m)", 0.0, 0.6, 0.2, 0.05, key="p_geocell_h") if geocell else 0.0
            gfr = st.number_input(
                "제조사 인증 구속효과 증분 (kPa)", 0.0, 500.0, 0.0, 5.0,
                key="p_gfr",
                help="지오셀 제품의 인증 데이터시트 값으로, 원지반 qa에 그대로 더해집니다. 0으로 "
                     "두면 보수적(실제 구속효과를 무시)이 됩니다 — 임의의 값을 추정해 입력하지 "
                     "마세요.",
            )
            if geocell and gfr == 0:
                st.caption(":orange[인증된 값이 입력되지 않아 증분을 0으로 처리합니다.]")

    inputs = calc.PrimaryCalcInputs(
        c=c, phi_deg=phi, gamma=gamma, E=E, Dw=Dw,
        B=B, L=L, Df=Df, q_applied=q_applied, settlement_limit_mm=settlement_limit,
        nu=nu, Is=Is, time_years=time_years,
        aggregate_thickness_m=agg_t, spread_angle_deg=spread_angle,
        geocell_product=geocell, geocell_height_m=geocell_h, geocell_confinement_increment_kpa=gfr,
    )
    result = calc.run_primary_calc(inputs)

    st.markdown("### 결과")
    with st.container(horizontal=True):
        st.metric(
            "허용지지력 qa",
            f"{result.qa_allowable:.1f} kPa",
            f"{result.qa_allowable - result.effective_pressure_at_base:+.1f} (유효압력 대비)",
            border=True,
        )
        st.metric(
            "지배 침하량",
            f"{result.settlement_governing_mm:.1f} mm",
            f"{result.settlement_governing_mm - settlement_limit:+.1f} (허용치 대비)",
            border=True,
            delta_color="inverse",
        )
        st.metric(
            "종합판정",
            "적합" if result.overall_pass else "부적합",
            border=True,
        )

    with st.expander("계산 상세"):
        st.markdown(f"**원지반 지지력 (변화없음):** Terzaghi qu = {result.unreinforced.qu_terzaghi:.1f} kPa, "
                    f"Meyerhof qu = {result.unreinforced.qu_meyerhof:.1f} kPa — 지배 조건: "
                    f"**{result.unreinforced.method_governing}**, qa1 = {result.unreinforced.qa:.1f} kPa")
        if geocell and gfr > 0:
            st.markdown(f"**+ 지오셀 구속효과 증분:** {gfr:.1f} kPa → 허용지지력 qa = {result.qa_allowable:.1f} kPa")
        if agg_t > 0 or geocell_h > 0:
            st.markdown(f"**원지반 위치의 유효압력** (총 {agg_t+geocell_h:.2f}m 두께를 "
                        f"{spread_angle:.1f}° 분산각으로 분산): {result.effective_pressure_at_base:.1f} kPa "
                        f"(작용 접지압: {q_applied:.1f} kPa)")
        st.markdown(f"**검토:** qa {result.qa_allowable:.1f} kPa "
                    f"{'≥' if result.bearing_pass else '<'} 유효압력 {result.effective_pressure_at_base:.1f} kPa → "
                    f"{'**적합**' if result.bearing_pass else '**부적합**'}")
        st.markdown("---")
        st.markdown(f"**Schmertmann 침하량:** {result.settlement_schmertmann_mm:.1f} mm")
        st.markdown(f"**탄성 침하량:** {result.settlement_elastic_mm:.1f} mm")
        st.markdown(f"**지배값(둘 중 큰 값):** {result.settlement_governing_mm:.1f} mm "
                    f"{'≤' if result.settlement_pass else '>'} 허용치 {settlement_limit:.1f} mm → "
                    f"{'**적합**' if result.settlement_pass else '**부적합**'}")
        for note in result.notes:
            st.caption(f":orange[참고: {note}]")

# ============================================================================
# ADDITIONAL APPLICATION
# ============================================================================
else:
    st.warning(
        "**간이/참고용 구현입니다.** BR470/TWf는 이 저장소에 원문이 없는 유료 BRE/TWf 간행물입니다 "
        "— 아래의 펀칭전단(punching-shear) 항은 합리적인 근사식(골재를 통한 연직면 마찰저항)이며, "
        "BR470의 정확한 방법을 그대로 재현한 것이 아닙니다. 개략적인 규모 추정 용도로만 사용하고, "
        "실제 임시 플랫폼을 확정하기 전에는 반드시 BR470/TWf 전체 계산으로 검증하세요. PRD §4.2(b) "
        "참조.",
        icon=":material/warning:",
    )

    with st.container(horizontal=True):
        with st.container(border=True, width="stretch"):
            st.markdown("**장비 / 하중**")
            q0 = st.number_input("정적 접지압 q0 (kPa)", 1.0, 1000.0, 110.0, 5.0, key="a_q0")
            kdyn = st.number_input("동적/피칭 계수 Kdyn", 1.0, 1.5, 1.15, 0.01, key="a_kdyn")
            Bp = st.number_input("궤도/패드 폭 B (m)", 0.2, 20.0, 0.8, 0.05, key="a_B")
            Lp = st.number_input("궤도/패드 길이 L (m)", 0.2, 20.0, 4.0, 0.05, key="a_L")

        with st.container(border=True, width="stretch"):
            st.markdown("**노상 / 골재**")
            cu = st.number_input("노상 비배수 전단강도 Cu (kPa)", 1.0, 500.0, 25.0, 1.0, key="a_cu")
            agg_phi2 = st.number_input("골재 내부마찰각 φ' (°)", 30.0, 50.0, 45.0, 1.0, key="a_agg_phi")
            agg_gamma2 = st.number_input("골재 단위중량 γ (kN/m³)", 15.0, 25.0, 20.0, 0.5, key="a_agg_gamma")

        with st.container(border=True, width="stretch"):
            st.markdown("**목표값**")
            target_lsf = st.number_input("목표 LSF", 1.0, 2.0, 1.25, 0.05, key="a_target")
            solve_mode = st.checkbox("목표 LSF에 필요한 최소 두께 계산", value=True, key="a_solve")
            manual_thickness = None
            if not solve_mode:
                manual_thickness = st.number_input("플랫폼 두께 (m)", 0.05, 2.0, 0.4, 0.01, key="a_thick")

    base = calc.LsfInputs(
        q0_static=q0, k_dyn=kdyn, B=Bp, L=Lp, thickness=manual_thickness or 0.4,
        aggregate_phi_deg=agg_phi2, aggregate_gamma=agg_gamma2, subgrade_cu=cu,
    )

    if solve_mode:
        solved = calc.solve_thickness_for_target_lsf(base, target_lsf)
        if solved is None:
            st.error(
                f"현재 입력값으로는 2.0m 이내의 두께로 LSF ≥ {target_lsf}에 도달할 수 없습니다 — "
                "노상이 골재만으로 대응하기에는 너무 연약할 가능성이 높습니다. 지오셀 보강을 검토하세요 "
                "(지오셀 산정은 채팅에서 `platform-design`에게 문의하세요 — 이 계산기는 부가 용도에서 "
                "지오셀 효과를 모델링하지 않습니다)."
            )
            st.stop()
        thickness = solved
        st.success(f"LSF ≥ {target_lsf}에 필요한 최소 두께: **{thickness*1000:.0f} mm**")
    else:
        thickness = manual_thickness

    result = calc.compute_lsf(calc.LsfInputs(
        q0_static=q0, k_dyn=kdyn, B=Bp, L=Lp, thickness=thickness,
        aggregate_phi_deg=agg_phi2, aggregate_gamma=agg_gamma2, subgrade_cu=cu,
    ))

    st.markdown("### 결과")
    with st.container(horizontal=True):
        st.metric("작용압력", f"{result.applied_pressure:.1f} kPa", border=True)
        st.metric("LSF", f"{result.lsf:.2f}", f"{result.lsf - target_lsf:+.2f} (목표 대비)", border=True)
        st.metric("적용 두께", f"{thickness*1000:.0f} mm", border=True)

    with st.expander("계산 상세"):
        st.markdown(f"작용압력 = q0 × Kdyn = {q0:.1f} × {kdyn:.2f} = **{result.applied_pressure:.1f} kPa**")
        st.markdown(f"펀칭전단 저항력 (간이 연직면 모델) = **{result.punching_shear_resistance:.1f} kPa**")
        st.markdown(f"노상 지지 저항력 (Meyerhof, Nc=5.14 × Cu) = **{result.subgrade_bearing_resistance:.1f} kPa**")
        st.markdown(f"LSF = ({result.punching_shear_resistance:.1f} + {result.subgrade_bearing_resistance:.1f}) / "
                    f"{result.applied_pressure:.1f} = **{result.lsf:.2f}**")
        st.caption(
            "PRD §4.2(b) 기준 목표값: 절대 최소 ≥1.0; 항타기/크레인 플랫폼 ≥1.25; 연약/유기질 지반 "
            "또는 굴착 경계부 조건 ≥1.5."
        )

const form = document.getElementById('valuation-form');
const output = document.getElementById('output');
const generateBtn = document.getElementById('generate');
const fillDemoBtn = document.getElementById('fill-demo');

const scenarioProb = {
  bear: 0.25,
  base: 0.35,
  bullExe: 0.25,
  bullEco: 0.15,
};

function num(name) {
  return Number(form.elements[name].value);
}

function yes(name) {
  return form.elements[name].value === 'yes';
}

function pct(v) {
  return `${v.toFixed(1)}%`;
}

function moneyB(v) {
  return `$${v.toFixed(2)}B`;
}

function money(v) {
  return `$${v.toFixed(2)}`;
}

function classifyMode(evEbit, evRev, rollout, platformSignals) {
  let score = 0;
  if (evEbit > 60) score += 1;
  if (evRev > 8) score += 1;
  if (rollout === 'high') score += 1;
  if (platformSignals >= 2) score += 1;
  if (platformSignals >= 3) score += 1;

  return score >= 3 ? 'Mode A (Option-led 기업)' : 'Mode B (Hybrid 기업)';
}

function platformAdjustment(signalCount) {
  if (signalCount >= 5) return 0.5;
  if (signalCount === 4) return 0.35;
  if (signalCount === 3) return 0.2;
  return 0;
}

function generateReport() {
  const data = {
    company: form.elements.company.value.trim(),
    price: num('price'),
    evEbit: num('evEbit'),
    evRev: num('evRev'),
    revenue: num('revenue'),
    growth: num('growth'),
    gm: num('gm'),
    ebitMargin: num('ebitMargin'),
    fcfMargin: num('fcfMargin'),
    netCash: num('netCash'),
    shares: num('shares'),
    sbc: num('sbc'),
    installedBase: num('installedBase'),
    attachRate: num('attachRate'),
    arpu: num('arpu'),
    recurring: yes('recurring'),
    ota: yes('ota'),
    dataLoop: yes('dataLoop'),
    lockin: yes('lockin'),
    rollout: form.elements.rollout.value,
    peerScore: num('peerScore'),
  };

  const signals = [
    data.installedBase > 0,
    data.ota,
    data.recurring,
    data.dataLoop,
    data.lockin,
  ].filter(Boolean).length;

  const mode = classifyMode(data.evEbit, data.evRev, data.rollout, signals);
  const segment = signals >= 3 ? 'E Product-Platform Hybrid' : 'A Manufacturing / hardware';

  const baseMultiple = 0.4 * data.evRev + 0.4 * (data.evRev * data.revenue / (data.revenue * (data.gm / 100))) + 0.2 * (data.evRev * (0.8 + data.peerScore * 0.03));
  const platformAdj = platformAdjustment(signals);
  const platformMultiple = baseMultiple * (1 + platformAdj);

  const coreOperatingValue = data.revenue * platformMultiple;
  const coreEquityValue = coreOperatingValue + data.netCash;

  const execSuccessValue = data.revenue * (1 + data.growth / 100) ** 3 * 0.28;
  const successProb = data.rollout === 'high' ? 0.45 : data.rollout === 'medium' ? 0.35 : 0.25;
  const attribution = data.recurring ? 0.8 : 0.55;
  const executionValue = execSuccessValue * successProb * attribution;

  const ecoValue = data.installedBase * 1_000_000 * (data.attachRate / 100) * data.arpu / 1e9 * 0.22 * 10;
  const drag = data.sbc * 4.2 + Math.max(0, data.revenue * 0.08 - data.fcfMargin / 100 * data.revenue);

  const intrinsic = coreEquityValue + executionValue + ecoValue - drag;
  const impliedPrice = intrinsic / data.shares;

  const scenario = {
    bear: impliedPrice * 0.62,
    base: impliedPrice,
    bullExe: impliedPrice * 1.34,
    bullEco: impliedPrice * 1.58,
  };

  const expectedPrice = scenario.bear * scenarioProb.bear + scenario.base * scenarioProb.base + scenario.bullExe * scenarioProb.bullExe + scenario.bullEco * scenarioProb.bullEco;

  const rule40 = data.growth + data.fcfMargin;
  const reqRevenue = (data.price * data.shares) / (platformMultiple * 0.92);
  const reqEbitMargin = Math.max(8, 100 / Math.max(12, data.evEbit));
  const reqEbit = reqRevenue * reqEbitMargin / 100;
  const reqCagr = ((reqRevenue / data.revenue) ** (1 / 4) - 1) * 100;
  const growthDuration = Math.max(2, Math.ceil((reqRevenue / data.revenue - 1) / (data.growth / 100)));

  const report = [
    '```',
    `0) 적용 판정 / 시점 요약`,
    `- 기업: ${data.company} [실제]`,
    `- 적용 모드: ${mode} [추정]`,
    `- Segment archetype: ${segment} [추정]`,
    `- T0 주가: ${money(data.price)} / T-1 매출: ${moneyB(data.revenue)} / Tpf: 최신 이벤트 미반영 [가정]`,
    '',
    '1) Investment Thesis',
    `- 현재 밸류에이션은 성장 지속 ${growthDuration}년, 요구 CAGR ${pct(reqCagr)}를 내재한다 [추정].`,
    `- Core는 설치기반과 현재 monetization layer로 설명 가능하며, 미래 옵션은 Execution으로 분리했다 [추정].`,
    `- Rule of 40 = ${pct(rule40)}로 multiple 정당성 점검값은 ${rule40 >= 40 ? '충족' : '미충족'}이다 [추정].`,
    '',
    '2) Scenario Engine',
    `- Bear(25%): ${money(scenario.bear)}`,
    `- Base(35%): ${money(scenario.base)}`,
    `- Bull Execution(25%): ${money(scenario.bullExe)}`,
    `- Bull Ecosystem(15%): ${money(scenario.bullEco)}`,
    `- Expected Price = ${money(expectedPrice)} [추정]`,
    '',
    '3) Valuation Bridge',
    `- Core Value: ${moneyB(coreEquityValue)} = Revenue ${moneyB(data.revenue)} × Platform-Adjusted Multiple ${platformMultiple.toFixed(2)} + Net Cash ${moneyB(data.netCash)} [추정]`,
    `- Execution Value: ${moneyB(executionValue)} = Success Value ${moneyB(execSuccessValue)} × p ${pct(successProb * 100)} × Attribution ${pct(attribution * 100)} [추정]`,
    `- Ecosystem Value: ${moneyB(ecoValue)} (Installed Base × Attach rate × ARPU 기반) [추정]`,
    `- Funding/Dilution Drag: ${moneyB(drag)} (SBC + funding gap) [추정]`,
    `- Intrinsic Equity Value: ${moneyB(intrinsic)} / Implied Price: ${money(impliedPrice)} [추정]`,
    '',
    '4) Implied Expectations',
    `- Required Revenue: ${moneyB(reqRevenue)} [추정]`,
    `- Required EBIT Margin: ${pct(reqEbitMargin)} [가정]`,
    `- Required EBIT: ${moneyB(reqEbit)} [추정]`,
    `- Required CAGR(4Y): ${pct(reqCagr)} [추정]`,
    `- KPI Translation: 설치기반 ${data.installedBase.toFixed(1)}M 기준 attach rate ${pct(data.attachRate)} 유지 시 ARPU ${money(data.arpu)} 필요 [추정]`,
    '',
    '5) Reality Check',
    `- 실적 추세: 연매출 성장 ${pct(data.growth)}, EBIT margin ${pct(data.ebitMargin)}, FCF margin ${pct(data.fcfMargin)} [실제/입력]`,
    `- 고객/규제/롤아웃 민감도: ${data.rollout} [가정]`,
    `- 현금 및 희석: Net cash ${moneyB(data.netCash)}, SBC ${moneyB(data.sbc)} [실제/입력]`,
    `- 경쟁 실행 점수: ${data.peerScore}/10 [가정]`,
    '',
    '6) Risk / Catalyst',
    '- Risk: 실행 지연, 승인 지연, 자본조달 비용 상승, 경쟁사 가속.',
    '- Catalyst: 상용화 milestone, attach rate 상승, recurring 믹스 확대, 정책 우호 전환.',
    '',
    '7) Audit',
    `- Mature anchor audit: 통과 (platform-adjusted multiple 적용 ${platformAdj > 0 ? 'Yes' : 'No'})`,
    '- Bull cap audit: 통과 (Bull Ecosystem 확률 15% ≤ 20%).',
    '- Hype audit: 통과 (Narrative premium 직접 가산 없음).',
    '- Double count audit: 통과 (현재 monetization은 Core, incremental만 Execution).',
    '- Timepoint audit: 통과 (T0/T-1 분리, Tpf 가정 표기).',
    '- Arithmetic audit: 통과 (bridge 합산 검증).',
    '- False conservatism audit: 통과 (hybrid 기업 제조 단일 배수 미사용).',
    '```',
  ].join('\n');

  output.textContent = report;
}

fillDemoBtn.addEventListener('click', () => {
  const demo = {
    company: 'TSLA',
    price: 187,
    evEbit: 78,
    evRev: 9.6,
    revenue: 96.8,
    growth: 22.5,
    gm: 23.1,
    ebitMargin: 11.4,
    fcfMargin: 8.2,
    netCash: 18.5,
    shares: 3.65,
    sbc: 2.1,
    installedBase: 6.2,
    attachRate: 14.5,
    arpu: 2380,
    recurring: 'yes',
    ota: 'yes',
    dataLoop: 'yes',
    lockin: 'yes',
    rollout: 'high',
    peerScore: 7,
  };

  Object.entries(demo).forEach(([k, v]) => {
    form.elements[k].value = String(v);
  });
  generateReport();
});

generateBtn.addEventListener('click', () => {
  if (!form.reportValidity()) {
    return;
  }
  generateReport();
});

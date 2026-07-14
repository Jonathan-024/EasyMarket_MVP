// ─── Données fictives ─────────────────────────────────────
const caTotalCDF = 184500;

// ─── Taux et calculs ──────────────────────────────────────
const tauxInput = document.getElementById('taux-change');
const caCDFEl = document.getElementById('ca-cdf');
const caUSDEl = document.getElementById('ca-usd');
const commissionCDFEl = document.getElementById('commission-cdf');
const commissionUSDEl = document.getElementById('commission-usd');

function formatNombre(n) {
  return n.toLocaleString('fr-FR');
}

function updateCA() {
  const taux = parseFloat(tauxInput.value) || 1;
  const caUSD = (caTotalCDF / taux).toFixed(2);
  const commissionCDF = Math.round(caTotalCDF * 0.1);
  const commissionUSD = (commissionCDF / taux).toFixed(2);

  caCDFEl.innerHTML = `${formatNombre(caTotalCDF)} <span class="kpi-unit">CDF</span>`;
  caUSDEl.innerHTML = `≈ ${formatNombre(parseFloat(caUSD))} <span class="kpi-unit">USD</span>`;
  commissionCDFEl.innerHTML = `${formatNombre(commissionCDF)} <span class="kpi-unit">CDF</span>`;
  commissionUSDEl.innerHTML = `≈ ${formatNombre(parseFloat(commissionUSD))} <span class="kpi-unit">USD</span>`;
}

tauxInput.addEventListener('input', updateCA);

// ─── Init ─────────────────────────────────────────────────
updateCA();
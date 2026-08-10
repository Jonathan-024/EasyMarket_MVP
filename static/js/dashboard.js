const tauxInput = document.getElementById('taux-change');
const caCDFEl = document.getElementById('ca-cdf');
const caUSDEl = document.getElementById('ca-usd');

function formatNombre(n) { return n.toLocaleString('fr-FR'); }

function updateCA() {
  if (!tauxInput || !caCDFEl || !caUSDEl) return;
  const caTotalCDF = 0;
  const taux = parseFloat(tauxInput.value) || 1;
  const caUSD = (caTotalCDF / taux).toFixed(2);
  caCDFEl.innerHTML = `${formatNombre(caTotalCDF)} <span class="kpi-unit">CDF</span>`;
  caUSDEl.innerHTML = `≈ ${formatNombre(parseFloat(caUSD))} <span class="kpi-unit">USD</span>`;
}

tauxInput?.addEventListener('input', updateCA);
updateCA();
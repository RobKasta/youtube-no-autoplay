'use strict';

const toggle = document.getElementById('toggle');
const label  = document.getElementById('label');
const status = document.getElementById('status');

function update(enabled) {
  toggle.checked = enabled;
  label.textContent  = enabled ? 'Activé' : 'Désactivé';
  status.textContent = enabled
    ? 'La vidéo ne démarre qu\'au clic'
    : 'Autoplay autorisé';
  status.style.color = enabled ? '#888' : '#c00';
}

// Lit l'état sauvegardé (défaut : activé)
chrome.storage.local.get('enabled', function (data) {
  update(data.enabled !== false);
});

toggle.addEventListener('change', function () {
  const enabled = toggle.checked;
  chrome.storage.local.set({ enabled });
  update(enabled);
});

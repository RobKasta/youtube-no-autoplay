'use strict';

let enabled = true;

// Lit l'état initial depuis le stockage (défaut : activé)
chrome.storage.local.get('enabled', function (data) {
  if (data.enabled === false) enabled = false;
});

// Se met à jour en temps réel si l'utilisateur bascule le popup
chrome.storage.onChanged.addListener(function (changes) {
  if ('enabled' in changes) enabled = changes.enabled.newValue;
});

document.addEventListener('play', function (e) {
  if (!enabled) return;
  const el = e.target;
  if (!el || el.tagName !== 'VIDEO') return;
  if (!navigator.userActivation || !navigator.userActivation.isActive) {
    el.pause();
  }
}, true);

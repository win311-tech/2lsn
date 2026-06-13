import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import { getAuth, signInWithPopup, getRedirectResult, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBaEMCO-JndsnuVHneoVw8onE6WLotkXJI",
  authDomain: "lsn-39047.firebaseapp.com",
  projectId: "lsn-39047",
  storageBucket: "lsn-39047.firebasestorage.app",
  messagingSenderId: "318290775126",
  appId: "1:318290775126:web:becff66521029b7ac5fff7",
  measurementId: "G-RXSTGEDCK1"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
auth.languageCode = 'en';
const provider = new GoogleAuthProvider();

// Firebase sign-in is only intended for pages that include #google-button.
// Your Django GSI login page uses the element #google-signin-button (Google Identity Services),
// so this prevents Firebase popups from starting on that page.
const googleLogin = document.getElementById('google-button');
window.lsnMainJsLoaded = true;
window.lsnGoogleButtonFound = !!googleLogin;
if (googleLogin) {
  googleLogin.addEventListener('click', async () => {
    console.log('Google login button clicked (Firebase)');

    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential && credential.accessToken;
      const user = result.user;
      console.log('Google sign-in success:', user, token);
      window.location.href = "/dashboard/";
    } catch (error) {
      // This error is often caused by the popup being blocked/closed.
      console.error('Google sign-in failed (popup/redirect flow):', error);

      let box = document.getElementById('google-auth-error');
      if (!box) {
        box = document.createElement('div');
        box.id = 'google-auth-error';
        box.style.marginTop = '12px';
        box.style.padding = '10px 12px';
        box.style.border = '1px solid #f00';
        box.style.background = '#fee';
        box.style.color = '#900';
        const btn = document.getElementById('google-button');
        if (btn && btn.parentElement) btn.parentElement.appendChild(box);
        else document.body.appendChild(box);
      }

      box.textContent = 'Google sign-in failed. If a popup blocker is enabled, allow popups and try again.';
    }
  });
} else {
  // Intentionally silent to avoid confusing the console on pages like Login.html
}


getRedirectResult(auth)
  .then((result) => {
    if (!result) return;
    const user = result.user;
    console.log('Google redirect sign-in result:', user);
  })
  .catch((error) => {
    console.error('Google redirect error:', error);
  });

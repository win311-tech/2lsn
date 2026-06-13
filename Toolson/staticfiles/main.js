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

const googleLogin = document.getElementById('google-button');
window.lsnMainJsLoaded = true;
window.lsnGoogleButtonFound = !!googleLogin;
if (googleLogin) {
  googleLogin.addEventListener('click', () => {
    console.log('Google login button clicked');
    signInWithPopup(auth, provider)
      .then((result) => {
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential && credential.accessToken;
        const user = result.user;
        console.log('Google sign-in success:', user, token);
        window.location.href = "/dashboard/";
      })
      .catch((error) => {
        console.error('Google sign-in failed:', error);
      });
  });
} else {
  console.warn('Google login button not found on this page');
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
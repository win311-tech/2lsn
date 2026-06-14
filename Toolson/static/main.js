import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import {
  getAuth,
  signInWithRedirect,
  getRedirectResult,
  GoogleAuthProvider,
} from "https://www.gstatic.com/firebasejs/12.14.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBaEMCO-JndsnuVHneoVw8onE6WLotkXJI",
  authDomain: "lsn-39047.firebaseapp.com",
  projectId: "lsn-39047",
  storageBucket: "lsn-39047.firebasestorage.app",
  messagingSenderId: "318290775126",
  appId: "1:318290775126:web:becff66521029b7ac5fff7",
  measurementId: "G-RXSTGEDCK1",
};

window.lsnMainJsLoaded = true;
console.log("[main.js] Firebase module executing...");

let auth;
let provider;

try {
  const app = initializeApp(firebaseConfig);
  auth = getAuth(app);
  auth.languageCode = "en";
  provider = new GoogleAuthProvider();
  console.log("[main.js] Firebase auth + provider initialized");
} catch (e) {
  console.error("[main.js] Firebase init failed:", e);
  showAuthError("Firebase initialization failed. Check console for details.");
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showAuthError(message) {
  let box = document.getElementById("google-auth-error");
  if (!box) {
    box = document.createElement("div");
    box.id = "google-auth-error";
    box.style.marginTop = "12px";
    box.style.padding = "10px 12px";
    box.style.border = "1px solid #f00";
    box.style.background = "#fee";
    box.style.color = "#900";
    box.style.fontSize = "0.7rem";
    box.style.fontFamily = "var(--font-accent)";
    box.style.letterSpacing = "0.05em";

    const btn = document.getElementById("google-button");
    if (btn && btn.parentElement) btn.parentElement.appendChild(box);
    else document.body.appendChild(box);
  }
  box.textContent = message;
}

function attachGoogleClickHandler() {
  const googleLogin = document.getElementById("google-button");
  window.lsnGoogleButtonFound = !!googleLogin;

  if (!googleLogin) {
    console.warn("[main.js] #google-button not found (yet)");
    return false;
  }

  if (googleLogin.dataset.lsnBound === "true") return true;
  googleLogin.dataset.lsnBound = "true";

  googleLogin.addEventListener("click", async (e) => {
    e.preventDefault();
    console.log("[main.js] Google login button clicked (initiating redirect flow)");

    if (!auth || !provider) {
      showAuthError("Auth not ready. Refresh and check console.");
      return;
    }

    try {
      await signInWithRedirect(auth, provider);
    } catch (error) {
      console.error("[main.js] Google sign-in redirect failed:", error);
      showAuthError("Google sign-in redirection failed. Check your connection and try again.");
    }
  });

  console.log("[main.js] Click handler attached successfully");
  return true;
}

attachGoogleClickHandler();
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    attachGoogleClickHandler();
  });
} else {
  setTimeout(attachGoogleClickHandler, 500);
}

// Handle resolving redirect results on page load
if (auth) {
  getRedirectResult(auth)
    .then((result) => {
      if (!result) return;
      const user = result.user;
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const idToken = credential ? credential.idToken : null;

      console.log("[main.js] Google redirect sign-in success:", user);

      if (idToken) {
        console.log("[main.js] Syncing credential token with Django backend...");
        const csrfToken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        fetch('/auth_receiver/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
          },
          body: 'credential=' + encodeURIComponent(idToken)
        }).then(resp => {
          if (resp.ok) {
            console.log("[main.js] Django backend session successfully established");
            // Auth completed; do not force navigation.
            return;
          } else {

            console.error("[main.js] Django session establishment failed with status:", resp.status);
            showAuthError("Failed to sync authorization with Django. Please try again.");
          }
        }).catch(err => {
          console.error("[main.js] Network error during token sync:", err);
          showAuthError("Failed to connect to the login server. Please check your internet connection.");
        });
      } else {
        console.warn("[main.js] No ID token found in redirect credential result");
        window.location.href = "/dashboard/";
      }
    })
    .catch((error) => {
      console.error("[main.js] Google redirect error:", error);
      showAuthError("Redirection sign-in error: " + error.message);
    });
}

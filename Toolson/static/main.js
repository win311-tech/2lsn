import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import {
  getAuth,
  signInWithPopup,
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

// Visible markers to confirm this module actually executed.
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

function showAuthError(message) {
  // Reuse or create a small error element on the page.
  let box = document.getElementById("google-auth-error");
  if (!box) {
    box = document.createElement("div");
    box.id = "google-auth-error";
    box.style.marginTop = "12px";
    box.style.padding = "10px 12px";
    box.style.border = "1px solid #f00";
    box.style.background = "#fee";
    box.style.color = "#900";

    // Place near the button if possible; fallback to body.
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

  // Prevent double-binding if this runs more than once.
  if (googleLogin.dataset.lsnBound === "true") return true;
  googleLogin.dataset.lsnBound = "true";

  googleLogin.addEventListener("click", async () => {
    console.log("[main.js] Google login button clicked");

    if (!auth || !provider) {
      showAuthError("Auth not ready. Refresh and check console.");
      return;
    }

    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      console.log("[main.js] Google sign-in success:", user);
      window.location.href = "/dashboard/";
    } catch (error) {
      // Often happens when a popup is blocked/closed before messaging begins.
      console.error("[main.js] Google sign-in failed (popup/redirect flow):", error);
      showAuthError("Google sign-in failed. If a popup blocker is enabled, allow popups and try again.");
    }
  });

  console.log("[main.js] Click handler attached");
  return true;
}

// Robust attachment: try immediately and again after DOM is ready.
attachGoogleClickHandler();
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    attachGoogleClickHandler();
  });
}

// Handle redirect flow (in case you ever switch to signInWithRedirect).
if (auth) {
  getRedirectResult(auth)
    .then((result) => {
      if (!result) return;
      const user = result.user;
      console.log("[main.js] Google redirect sign-in result:", user);
    })
    .catch((error) => {
      console.error("[main.js] Google redirect error:", error);
      showAuthError("Redirect sign-in failed. See console for details.");
    });
}


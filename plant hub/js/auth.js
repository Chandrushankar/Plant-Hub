// Plant Hub Authentication Logic (Modular v9)
import { auth, googleProvider, RecaptchaVerifier, signInWithPhoneNumber, signInWithPopup } from './firebase-config.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// DOM Elements
const emailForm = document.getElementById('email-form');
const phoneForm = document.getElementById('phone-form');
const googleBtn = document.getElementById('google-btn');
const verifyOtpBtn = document.getElementById('verify-otp-btn');

// --- Helper: Send Token to Backend ---
async function verifyTokenWithBackend(user) {
    try {
        const token = await user.getIdToken();
        const response = await fetch('http://localhost:5000/api/auth/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: token })
        });
        const data = await response.json();

        if (data.user) {
            alert(`Verified! Welcome ${data.user.email || data.user.phone}`);
            window.location.href = 'index.html';
        } else {
            alert("Backend verification failed: " + data.error);
        }
    } catch (error) {
        console.error("Backend Error:", error);
        alert("Server error during verification.");
    }
}

// --- 1. Email/Password Sign Up ---
if (emailForm) {
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email-input').value;
        const password = document.getElementById('email-pass').value;

        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            verifyTokenWithBackend(userCredential.user);
        } catch (error) {
            alert(error.message);
        }
    });
}

// --- 2. Google Sign-In ---
if (googleBtn) {
    googleBtn.addEventListener('click', async () => {
        try {
            const result = await signInWithPopup(auth, googleProvider);
            verifyTokenWithBackend(result.user);
        } catch (error) {
            console.error(error);
            alert("Google Sign-In failed.");
        }
    });
}

// --- 3. Phone OTP Auth ---
if (phoneForm) {
    // Initialize reCAPTCHA
    window.recaptchaVerifier = new RecaptchaVerifier('recaptcha-container', {
        'size': 'normal',
        'callback': (response) => {
            // reCAPTCHA solved, allow signInWithPhoneNumber.
            console.log("reCAPTCHA solved");
        }
    }, auth);

    const getOtpBtn = document.getElementById('get-otp-btn');

    getOtpBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const phoneNumber = document.getElementById('phone-input').value;
        const appVerifier = window.recaptchaVerifier;

        try {
            getOtpBtn.disabled = true;
            getOtpBtn.innerText = "Sending...";

            // Send OTP
            window.confirmationResult = await signInWithPhoneNumber(auth, phoneNumber, appVerifier);

            alert("OTP Sent!");
            document.getElementById('otp-section').style.display = 'block';
            getOtpBtn.style.display = 'none';
            document.getElementById('recaptcha-container').style.display = 'none';
        } catch (error) {
            console.error(error);
            getOtpBtn.disabled = false;
            getOtpBtn.innerText = "Get OTP";
            alert("Failed to send SMS. Check console.");
        }
    });

    // Verify OTP
    if (verifyOtpBtn) {
        verifyOtpBtn.addEventListener('click', async () => {
            const code = document.getElementById('otp-code').value;
            try {
                const result = await window.confirmationResult.confirm(code);
                verifyTokenWithBackend(result.user);
            } catch (error) {
                alert("Invalid OTP");
            }
        });
    }
}

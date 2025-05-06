/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll(".otp-box");

    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    const otpSection = document.getElementById("otp-section");
    if (otpSection) {
        otpSection.scrollIntoView({ behavior: "smooth" });
    }

    window.showOTPSection = function () {
        const otpSection = document.getElementById("otp-section");
        if (otpSection && otpSection.style.display === "none") {
            otpSection.style.display = "block";
            otpSection.scrollIntoView({ behavior: "smooth" });
        }
    };

    let timerOn = true;
    window.timer = function (remaining) {
        const timerElement = document.getElementById('timer');
        const timerContainer = timerElement?.parentElement;
        let m = Math.floor(remaining / 60);
        let s = remaining % 60;

        m = m < 10 ? '0' + m : m;
        s = s < 10 ? '0' + s : s;

        timerElement.innerHTML = m + ':' + s;
        remaining -= 1;

        if (remaining >= 0 && timerOn) {
            setTimeout(function () {
                timer(remaining);
            }, 1000);
            return;
        }

        if (timerContainer) {
            timerContainer.innerHTML = `<span style="color:red;">OTP has expired. Please click 'Resend OTP'</span>`;
        }

        const expiredInput = document.getElementById('otp_expired');
        if (expiredInput) {
            expiredInput.value = "1";
        }
    };

    timer(120);
});
 
 document.addEventListener("DOMContentLoaded", function () {
            let form = document.getElementById("register-form");
            let password1 = document.querySelector("input[name='password1']");
            let password2 = document.querySelector("input[name='password2']");
            let errorMsg = document.getElementById("password-error");

            function validatePasswords() {
                if (password1.value !== password2.value) {
                    errorMsg.style.display = "block";
                    return false;
                } else {
                    errorMsg.style.display = "none";
                    return true;
                }
            }

            password1.addEventListener("input", validatePasswords);
            password2.addEventListener("input", validatePasswords);

            form.addEventListener("submit", function (event) {
                if (!validatePasswords()) {
                    event.preventDefault();
                }
            });
        });
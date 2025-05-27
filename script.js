document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("prediction-form");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const formDataObj = {};
        formData.forEach((value, key) => {
            formDataObj[key] = value;
        });

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formDataObj),
        });

        const data = await response.json();
        resultDiv.innerHTML = "";

        if (data.result.includes("No Heart Disease")) {
            const msg = document.createElement("div");
            msg.className = "alert alert-success animate__animated animate__fadeInDown";
            msg.innerText = "✅ No Heart Disease Detected!";
            resultDiv.appendChild(msg);

            setTimeout(() => {
                msg.remove();
            }, 3000);
        } else {
            const warning = document.createElement("div");
            warning.className = "alert alert-danger animate__animated animate__flash";
            warning.innerHTML = "🚨 High Risk of Heart Disease! <br><strong>Please consult a doctor immediately.</strong>";

            resultDiv.appendChild(warning);

            setTimeout(() => {
                warning.remove();
            }, 3000);
        }
    });
});

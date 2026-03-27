document.getElementById("rul-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // stop page refresh

    const data = {
        sensor_7: parseFloat(document.getElementById("sensor_7").value),
        sensor_12: parseFloat(document.getElementById("sensor_12").value),
        sensor_14: parseFloat(document.getElementById("sensor_14").value),
        sensor_20: parseFloat(document.getElementById("sensor_20").value),
        sensor_21: parseFloat(document.getElementById("sensor_21").value),
        op_setting_1: parseFloat(document.getElementById("op_setting_1").value),
        op_setting_2: parseFloat(document.getElementById("op_setting_2").value),
        op_setting_3: parseFloat(document.getElementById("op_setting_3").value)
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        let riskColor = "#16a34a";
        if (result.risk_level === "Medium Risk") riskColor = "#d97706";
        if (result.risk_level === "High Risk") riskColor = "#dc2626";

        const resultDiv = document.getElementById("result");
        resultDiv.style.borderLeft = `6px solid ${riskColor}`;
        resultDiv.style.padding = "15px";
        resultDiv.style.marginTop = "20px";

        resultDiv.innerHTML = `
            <strong>Remaining Useful Life:</strong><br>
            <span class="rul-value">${result.predicted_rul} cycles</span><br><br>
            <strong>Risk Level:</strong>
            <span style="color:${riskColor}; font-weight:700;">
                ${result.risk_level}
            </span>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML =
            "<span class='error'>Error connecting to backend.</span>";
    }
});

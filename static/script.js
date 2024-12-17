document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const data = {
        age: parseFloat(document.getElementById('age').value),
        academic_pressure: parseFloat(document.getElementById('academic_pressure').value),
        cgpa: parseFloat(document.getElementById('cgpa').value),
        study_satisfaction: parseFloat(document.getElementById('study_satisfaction').value),
        sleep_duration: parseFloat(document.getElementById('sleep_duration').value),
        dietary_habits: document.getElementById('dietary_habits').value,
        degree: document.getElementById('degree').value,
        "have_you_ever_had_suicidal_thoughts_?": document.getElementById('have_you_ever_had_suicidal_thoughts_?').value,
        "work/study_hours": parseFloat(document.getElementById('work/study_hours').value),
        financial_stress: parseFloat(document.getElementById('financial_stress').value)
    };

    const response = await fetch('http://localhost:9696/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    const predictionResult = document.getElementById("result");

    if (response.ok) {
        // Calculate depression probability as percentage
        const depressionProbabilityPercentage = (result.depression_probability * 100).toFixed(2);
        
        // Convert depression result to Yes/No
        const depressionResult = result.depression ? 'Yes' : 'No';

        // Update the result text
        predictionResult.innerHTML = `Depression Probability: ${depressionProbabilityPercentage}%<br>Depression: ${depressionResult}`;

        // Change the color based on the prediction
        if (depressionResult === 'Yes') {
            predictionResult.style.color = 'red';  // Red for depression prediction "Yes"
        } else {
            predictionResult.style.color = 'green';  // Green for depression prediction "No"
        }
    } else {
        predictionResult.innerHTML = `Error: ${result.error}`;
    }
});

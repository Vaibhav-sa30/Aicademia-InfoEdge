import React from 'react';

function BiasResult({ result }) {
    return (
        <div className="result">
            <h2>Bias Metrics:</h2>
            <p>Mean Difference: {result.mean_difference}</p>
            <p>Disparate Impact: {result.disparate_impact}</p>
        </div>
    );
}

export default BiasResult;

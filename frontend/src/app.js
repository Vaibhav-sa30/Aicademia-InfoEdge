import React, { useState } from 'react';
import BiasDetectionForm from './components/BiasDetectionForm';
import BiasResult from './components/BiasResult';

function App() {
    const [result, setResult] = useState(null);

    // Function to handle the result from the BiasDetectionForm
    const handleResult = (data) => {
        setResult(data);
    };

    return (
        <div className="App">
            <h1>Bias Detection Tool</h1>
            <BiasDetectionForm onResult={handleResult} />
            {result && <BiasResult result={result} />}
        </div>
    );
}

export default App;

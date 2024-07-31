import React, { useState } from 'react';
import axios from 'axios';

function BiasDetectionForm({ onResult }) {
    const [file, setFile] = useState(null);
    const [label, setLabel] = useState('');
    const [protectedAttr, setProtectedAttr] = useState('');
    const [favorableClass, setFavorableClass] = useState('');
    const [privilegedValue, setPrivilegedValue] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        formData.append('label', label);
        formData.append('protected_attr', protectedAttr);
        formData.append('favorable_class', favorableClass);
        formData.append('privileged_value', privilegedValue);

        console.log("Form Data Prepared:", {
            file, label, protectedAttr, favorableClass, privilegedValue
        });

        try {
            const response = await axios.post('http://localhost:8000/check-bias', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log("Response received:", response.data);
            onResult(response.data);
        } catch (error) {
            console.error('Error uploading the file:', error.response ? error.response.data : error.message);
            alert('Error uploading the file: ' + (error.response ? error.response.data : error.message));
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" id="fileInput" onChange={handleFileChange} required name="file" />
            <input type="text" placeholder="Label Column" id="labelInput" value={label} onChange={(e) => setLabel(e.target.value)} required name="label" />
            <input type="text" placeholder="Protected Attribute" id="protectedAttrInput" value={protectedAttr} onChange={(e) => setProtectedAttr(e.target.value)} required name="protected_attr" />
            <input type="text" placeholder="Favorable Class" id="favorableClassInput" value={favorableClass} onChange={(e) => setFavorableClass(e.target.value)} required name="favorable_class" />
            <input type="text" placeholder="Privileged Value" id="privilegedValueInput" value={privilegedValue} onChange={(e) => setPrivilegedValue(e.target.value)} required name="privileged_value" />
            <button type="submit">Check Bias</button>
        </form>
    );
}

export default BiasDetectionForm;

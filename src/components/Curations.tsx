import React, { useState } from 'react';

function Curations() {
    const [cool, setCool] = useState('neat');
    return (
        <div>
            <h1>Curations</h1>
            {cool}
        </div>
    );
}

export default Curations;
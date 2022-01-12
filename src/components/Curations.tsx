import React, { useState } from 'react';
import Curation from './Curation';

interface ICurationsProps {
    curations: Array<{
        id: string,
        title: string,
        imageUrl: string,
    }>;
};

function Curations(props: ICurationsProps) {
    const [cool, setCool] = useState('neat');
    const curations = props.curations.map((curation, i) => (
        <Curation key={curation.id}
            title={curation.title}
            imageUrl={curation.imageUrl} />
    ));
    return (
        <>
            <h1>Curations</h1>
            {cool}
            <div className={'col-count-3 col-gap-2'}>
                {curations}
            </div>
        </>
    );
}

export default Curations;
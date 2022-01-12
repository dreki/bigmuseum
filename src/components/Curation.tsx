
import React, { useState } from 'react';

interface ICurationProps {
    title: string;
    imageUrl: string;
}

function Curation(props: ICurationProps) {
    return (
        <div className={'bi-avoid shadow-sm rounded mb-4'}>
            <img src={props.imageUrl} alt={props.title} />
            <h1>{props.title}</h1>
        </div>
    );
}

export default Curation;
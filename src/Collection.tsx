import React from 'react';


interface ICollectionProps {
}

interface ICollectionState {
}


class Collection extends React.Component<ICollectionProps, ICollectionState> {
    constructor(props: ICollectionProps) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <div>
                <h2 className='text-2xl mt-5 mb-4'>Collection</h2>
            </div>
        );
    }
}

export default Collection;

import axios, { AxiosResponse } from 'axios';
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

    public async componentDidMount(): Promise<void> {
        const response: AxiosResponse = await axios.get('/api/collection/items');
        console.log('> Collection.componentDidMount, response:');
        console.log(response);
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

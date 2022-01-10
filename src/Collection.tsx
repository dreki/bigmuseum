import axios, { AxiosResponse } from 'axios';
import React from 'react';
import Curations from './components/Curations';


interface ICollectionProps {
};

interface ICollectionState {
    curations: Array<{
        id: string,
        imageUrl: string,
        createdAt: Date,
        updatedAt: Date
    }>
};


class Collection extends React.Component<ICollectionProps, ICollectionState> {
    constructor(props: ICollectionProps) {
        super(props);
        this.state = { curations: [] };
    }

    public async componentDidMount(): Promise<void> {
        const response: AxiosResponse = await axios.get('/api/collection/items');
        console.log('> Collection.componentDidMount, response:');
        console.log(response);
        this.setState({ curations: response.data.items });
    }

    render() {
        // const curations = ()
        const curations = <Curations />;
        return (
            <div>
                <h2 className='text-2xl mt-5 mb-4'>Collection</h2>
                {curations}
            </div>
        );
    }
}

export default Collection;

import * as React from "react";
import Posts from './components/Posts';
import Test from './components/Test';
// import fetch from 'cross-fetch';
import axios from 'axios';

interface IAppProps {
    name: string
}

interface IAppState {
    posts: Array<{ id: string, title: string, link: string }>
}

class App extends React.Component<IAppProps, IAppState> {
    state: IAppState = {
        posts: []
    }

    public async componentDidMount(): Promise<void> {
        // Load and set posts.
        // const response = await fetch('/api/posts/new');
        const response = await axios.get('/api/posts/new');
        console.log(response);

        // const posts: Array<{ id: string, title: string, link: string }> = (await response.json()).items;
        const posts: Array<{ id: string, title: string, link: string }> = response.data.items;
        this.setState({ posts: posts });
    }

    async onTrashPost(postId: string) {
        // const response = await fetch('/api/collection', { method: 'POST' })
        const response = await axios.post('/api/collection/items', { postId });
    }

    render() {
        const { name } = this.props;
        return (
            <>
                <h2 className={'text-2xl mt-5 mb-4'}>New Arrivals</h2>
                <Posts posts={this.state.posts}
                    onTrashPost={this.onTrashPost.bind(this)} />
            </>
        );
    }
}

export default App;

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

    onCollectPost = async (postId: string) => {
    }

    onTrashPost = async (postId: string) => {
        // const response = await fetch('/api/collection', { method: 'POST' })

        // const response = await axios.post('/api/collection/items', { postId });
        // const response = await axios.delete(`/api/posts/abc123`);
        const response = await axios.delete(`/api/posts/${postId}`);
        // Remove post from state.
        const posts = this.state.posts.filter(post => post.id !== postId);
        this.setState({ posts });
    }

    render() {
        const { name } = this.props;
        return (
            <>
                <h2 className={'text-2xl mt-5 mb-4'}>New Arrivals</h2>
                <Posts posts={this.state.posts}
                    onCollectPost={this.onCollectPost}
                    onTrashPost={this.onTrashPost} />
            </>
        );
    }
}

export default App;

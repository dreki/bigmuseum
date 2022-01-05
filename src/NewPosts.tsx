import axios from 'axios';
import React from 'react';
import { Link } from 'react-router-dom';
import Posts from './components/Posts';

interface INewPostsProps {
    name: string
}

interface INewPostsState {
    posts: Array<{
        id: string,
        postId: string,
        title: string,
        imageUrl: string,
        postCreatedAt: Date
    }>
}

class NewPosts extends React.Component<INewPostsProps, INewPostsState> {
    state: INewPostsState = {
        posts: []
    }

    public async componentDidMount(): Promise<void> {
        console.log('> App.componentDidMount');

        // Load and set posts.
        const response = await axios.get('/api/posts?filter=new');
        // console.log(response);

        // const posts: Array<{ id: string, title: string, link: string }> = (await response.json()).items;
        const posts: Array<{
            id: string,
            title: string,
            // link: string,
            imageUrl: string,

            postId: string,
            postCreatedAt: Date
        }> = response.data.items;
        this.setState({ posts: posts });
    }

    onCollectPost = async (postId: string) => {
        console.log(`> onCollectPost ${postId}`);
        // Add post to collection
        const response = await axios.post(
            '/api/collection/items',
            { postId: postId }
        );
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
        const posts = (<Posts posts={this.state.posts}
            onCollectPost={this.onCollectPost}
            onTrashPost={this.onTrashPost} />);
        return (
            <>
                <Link className='underline text-blue-600 hover:text-blue-800'
                    to='/collection'>Collection</Link>
                <h2 className={'text-2xl mt-5 mb-4'}>New Arrivals, {name}</h2>
                {posts}
            </>
        );
    }
}

export default NewPosts;
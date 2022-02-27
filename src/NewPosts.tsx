import axios from 'axios';
import React from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import Posts from './components/Posts';

interface INewPostsProps {
    name: string,
}

interface INewPostsState {
    posts: Array<{
        id: string,
        postId: string,
        title: string,
        imageUrl: string,
        hasCurations: boolean,
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
        // TODO: Create shared function to load posts that can be used here and when people click on a date.
        const response = await axios.get('/api/posts?filter=new');
        // console.log(response);

        // const posts: Array<{ id: string, title: string, link: string }> = (await response.json()).items;
        const posts: Array<{
            id: string,
            title: string,
            // link: string,
            imageUrl: string,
            hasCurations: boolean,
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

    // onClickDate = async (date: string) => {
    //     console.log(`> onClickDate ${date}`);
    // }
    onClickDate = async (date: string) => {
        console.log(`> onClickDate ${date}`);
        // It's okay to load here, since React Router doesn't actually re-load
        // or re-create the component. So, the URL just changes and people can
        // reload it, but we should load new data here.
        console.log('LOAD data here');
    }

    render() {
        const { name } = this.props;

        // Get query params.
        const queryParams = new URLSearchParams(window.location.search);
        console.log(`> queryParams: ${queryParams}; date: ${queryParams.get('date')}`);


        const posts = (<Posts posts={this.state.posts}
            onCollectPost={this.onCollectPost}
            onTrashPost={this.onTrashPost} />);
        return (
            <>
                <Link to='/collection'>Collection</Link>
                <h2 className={'text-2xl mt-5 mb-4'}>New Arrivals, {name}</h2>
                <h3 className={'text-xl mt-3 mb-5'}>Today <em><span className='text-gray-300'>(UTC)</span></em></h3>
                <nav aria-label="Posts by Date">
                    <ul>
                        {/* <li><a href="#">yesterday</a></li> */}
                        <li>
                            <Link to='/app/posts?date=yesterday'
                                onClick={() => this.onClickDate("yesterday")}>yesterday</Link>
                        </li>
                        <li>today</li>
                    </ul>
                </nav>
                {posts}
            </>
        );
    }
}

export default NewPosts;

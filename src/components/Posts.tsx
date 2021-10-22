import * as React from 'react';
import Post from './Post';


interface IPostsProps {
    posts: Array<{ title: string, link: string }>
}

interface IPostsState {
}

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component<IPostsProps, IPostsState> {
    render() {
        /** @type {Array} */
            // let posts = this.props.posts || [];
            // posts: Array<React.ReactElement> = posts.map((post, i) => (<Post key={i} {...post} />));
        let posts: Array<React.ReactElement> =
                (this.props.posts ?? []).map((post, i) => (<Post key={i} {...post} />));
        return (
            <div>
                <div>Posts</div>
                {/* <div className={'flex flex-row flex-wrap items-stretch'}> */}
                {/* <div className={'flex flex-wrap items-stretch'}> */}
                <div className={'grid grid-cols-3 gap-2'}>
                    {posts}
                </div>
            </div>
        );
    }
}

export default Posts;

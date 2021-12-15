
import React from 'react';
import Post from './Post';

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component {
    render() {
        /** @type {Array} */
        let posts = this.props.posts || [];
        posts = posts.map((post, i) => (<Post key={i} {...post} />));
        return (
            <div>
                <div>Posts</div>
                {/* <div className={'flex flex-row flex-wrap items-stretch'}> */}
                {/* <div className={'flex flex-wrap items-stretch'}> */}
                <div className={'grid grid-cols-3'}>
                    {posts}
                </div>
            </div>
        );
    }
}

export default Posts;

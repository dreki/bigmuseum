
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
                <div className={'flex'}>
                    {posts}
                </div>
            </div>
        );
    }
}

export default Posts;

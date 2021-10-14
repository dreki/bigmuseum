
import React from 'react';
import Post from './Post';

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component {
    render() {
        /** @type {Array} */
        let posts = this.props.posts || [];
        console.log(`> posts:`);
        console.log(posts);
        posts = posts.map(post => <Post {...post} />);
        return (
            <>
                <div>Posts</div>
                {posts}
            </>
        );
    }
}

export default Posts;

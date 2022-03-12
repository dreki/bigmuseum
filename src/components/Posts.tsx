import * as React from 'react';
import { ReactNode } from 'react';
import Post from './Post';

/**
 * typedef for Posts props
 */
interface IPostsProps {
    posts: Array<{
        id: string,
        postId: string,
        title: string,
        imageUrl: string,
        hasCurations: boolean,
        postCreatedAt: Date
    }>;
    onCollectPost?: ((postId: string) => void);
}

/**
 * typedef for Posts state
 */
interface IPostsState {
}

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component<IPostsProps, IPostsState> {

    /**
     * Notify the parent component that a post collection has been triggered.
     * @param postId {string}
     * @returns {void}
     */
    onCollectPost = (postId: string): void => {
        if (!this.props.onCollectPost) { return; }
        console.log('collecting post:', postId);
        this.props.onCollectPost(postId);
    }

    /**
     * Render the list of `Post`s.
     * @returns {ReactNode}
     */
    render(): React.ReactNode {
        let posts: Array<React.ReactElement> =
            (this.props.posts ?? []).map((post, i) => (
                <Post key={i} {...post}
                    onCollectPost={this.onCollectPost} />));
        return (
            <div>
                <div className={'col-count-3 col-gap-2'}>
                    {posts}
                </div>
            </div>
        );
    }
}

export default Posts;

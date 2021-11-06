import * as React from 'react';
import Post from './Post';
import { ReactNode } from "react";


interface IPostsProps {
    posts: Array<{ id: string, title: string, link: string }>;
    onTrashPost?: ((postId: string) => void);
}

interface IPostsState {
}

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component<IPostsProps, IPostsState> {

    onTrashPost(postId: string) {
        if (this.props.onTrashPost) {
            this.props.onTrashPost(postId);
        }
    }

    render(): React.ReactNode {
        let posts: Array<React.ReactElement> =
            (this.props.posts ?? []).map((post, i) => (
                <Post key={i} {...post}
                    onTrashPost={this.onTrashPost.bind(this)} />));
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

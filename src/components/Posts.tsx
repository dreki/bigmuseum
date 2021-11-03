import * as React from 'react';
import Post from './Post';
import { ReactNode } from "react";


interface IPostsProps {
    posts: Array<{ title: string, link: string }>
}

interface IPostsState {
}

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component<IPostsProps, IPostsState> {

    render(): React.ReactNode {
        let posts: Array<React.ReactElement> =
            (this.props.posts ?? []).map((post, i) => (<Post key={i} {...post} />));
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

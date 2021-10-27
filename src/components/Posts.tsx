import * as React from 'react';
import Post from './Post';
import Masonry from 'react-masonry-component';
import {ReactNode} from "react";


interface IPostsProps {
    posts: Array<{ title: string, link: string }>
}

interface IPostsState {
}

/**
 * Renders a list of `Post`s.
 */
class Posts extends React.Component<IPostsProps, IPostsState> {
    render__DEP() {
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
                {/*<div className={'grid grid-cols-3 gap-2'}>*/}
                <Masonry options={{
                    itemSelector: '.js-post',
                    columnWidth: '.js-sizer',
                    // gutter: 10,
                }}>
                    <div className={'js-sizer w-1/3'}>&nbsp;</div>
                    {posts}
                </Masonry>
                {/*</div>*/}
            </div>
        );
    }

    render(): React.ReactNode {
        let posts: Array<React.ReactElement> =
            (this.props.posts ?? []).map((post, i) => (<Post key={i} {...post} />));
        return (
            <div>
                <div>Posts</div>
                <div className={'col-count-3 col-gap-1'}>
                    {posts}
                </div>
            </div>
        );
    }
}

export default Posts;

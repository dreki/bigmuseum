
import React from 'react';

class Post extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
    }
    render() {
        return (
            <div className={'border rounded shadow-sm px-2 py-1'}>
                <span>I am a post</span>
            </div>
        )
    }
}

export default Post;

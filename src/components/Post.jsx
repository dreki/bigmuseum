
import React from 'react';
import { v4 as uuidv4 } from 'uuid';

class Post extends React.Component {
    render() {
        return (
            <div key={uuidv4()} className={'border rounded shadow-sm px-2 py-1'}>
                <span>I am a post</span>
            </div>
        )
    }
}

export default Post;

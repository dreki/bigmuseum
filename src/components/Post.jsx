
import React from 'react';

class Post extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
    }
    render() {
        return (
            <div className={'border rounded shadow-sm px-2 py-1'}>
                <span>{this.props.title}</span>
                <img src={this.props.link} />
            </div>
        )
    }
}

export default Post;

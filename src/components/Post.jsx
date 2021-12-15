
import React from 'react';

class Post extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
    }
    render__DEP() {
        return (
            // <div className={'max-w-sm border rounded shadow-sm px-2 py-1'}>
            // <div className={'flex-shrink border rounded shadow-sm px-2 py-1'}>
            // <div className={'w-1/3 border rounded shadow-sm px-2 py-1'}>
            // <div className={'h-48 border rounded shadow-sm px-2 py-1'}>


            // <div className={'max-w- border `rounded shadow-sm px-2'}>
            //     <span>{this.props.title}</span>
            //     <div className={'h-48'}>
            //         <img className={'w-full h-full object-contain'} src={this.props.link} />
            //     </div>
            // </div>
            <div className={'flex-grow border rounded shadow-sm pt-2 pb-2 mb-2 mr-2'}>
                <div className={'max-w-xs'}>
                    <span className={''}>{this.props.title}</span>
                </div>
                <div className={'h-52'}>
                    <img className={'w-full h-full object-contain'} src={this.props.link} />
                </div>
            </div>
        )
    }

    render() {
        return (
            <div>
                
            </div>
        );
    }
}

export default Post;

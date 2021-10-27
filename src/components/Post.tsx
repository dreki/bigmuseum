import * as React from 'react';
// import ReactPlaceholder from 'react-placeholder';

interface IPostProps {
    title: string,
    link: string,
    // key: number,
}

interface IPostState {
    imageLoaded: boolean
}


class Post extends React.Component<IPostProps, IPostState> {
    // state: {
    //     imageLoaded: false
    // }

    constructor(props) {
        super(props);
        console.log(props);
        this.state = {imageLoaded: false};
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

            // <div className={'flex-grow border rounded shadow-sm pt-2 pb-2 mb-2 mr-2'}>
            //     <div className={'max-w-xs'}>
            //         <span className={''}>{this.props.title}</span>
            //     </div>
            //     <div className={'h-52'}>
            //         <img className={'w-full h-full object-contain'} src={this.props.link}/>
            //     </div>
            // </div>
            <div className={'js-post'}>
                {/*<Image src={this.props.link}/>*/}
            </div>
        )
    }

    onImageLoad(e: React.SyntheticEvent) {
        console.log(`> onImageLoad`);
        this.setState({imageLoaded: true})
    }

    render() {
        const img = (
            <img alt={`Artwork: ${this.props.title}`}
                 className={'w-full'}
                 src={this.props.link}
                 onLoad={this.onImageLoad.bind(this)}/>
        );
        return (
            // <div>
            //     <img alt={`Artwork: ${this.props.title}`}
            //          className={''}
            //          src={this.props.link}/>
            // </div>
            // <div className={'js-post w-1/3 border rounded shadow-sm pt-2 pb-2'}>

            // <div className={'js-post w-1/3'}>
            <div>
                {/*<img alt={`Artwork: ${this.props.title}`}*/}
                {/*     className={'w-32'}*/}
                {/*     src={this.props.link}/>*/}

                {/*<div className="m-1 bg-white">*/}
                {/*    <span>post</span>*/}
                {/*</div>*/}
                {/*<div className={'border rounded shadow-sm mr-2 mb-2 ml-2 pt-2 pb-2'}>*/}
                <div className={'border rounded shadow-sm pb-2'}>
                    {/*<ReactPlaceholder type={'rect'} ready={this.state.imageLoaded}>*/}
                    {/*    {img}*/}
                    {/*</ReactPlaceholder>*/}
                    {img}
                </div>
            </div>
        );
    }
}

export default Post;

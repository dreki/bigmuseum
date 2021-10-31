import * as React from 'react';
import ContentLoader from 'react-content-loader';
import PreloadImage from './PreloadImage';
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

    constructor(props: IPostProps) {
        super(props);
        console.log(props);
        this.state = {
            imageLoaded: false
        };
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

    onImageLoaded(e: React.SyntheticEvent) {
        // onImageLoad(e: Event) {
        console.log(`> onImageLoad`);
        this.setState({ imageLoaded: true })
    }

    render() {

        let imgClass: string = 'w-full';

        // const img = (
        //     <img alt={`Artwork: ${this.props.title}`}
        //         className={'w-full'}
        //         src={this.props.link}
        //         onLoad={this.onImageLoaded.bind(this)} />
        // );

        // const img = new Image();
        // img.onload = this.onImageLoad;

        // const img = React.createElement(
        //     'img',
        //     { onLoad: this.onImageLoad.bind(this) }
        // );

        const imageContentLoader: JSX.Element = (
            <ContentLoader viewBox="0 0 450 400">
                <rect x="0" y="0" rx="0" ry="0" width="450" height="400" />
            </ContentLoader>
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
                <div className={'border rounded shadow-sm mb-4 bi-avoid'}>
                    {/*<ReactPlaceholder type={'rect'} ready={this.state.imageLoaded}>*/}
                    {/*    {img}*/}
                    {/*</ReactPlaceholder>*/}

                    <span>{this.props.title}</span>

                    {/* {!this.state.imageLoaded && <ContentLoader className={'m-2'} />} */}
                    {/* {!this.state.imageLoaded && imageContentLoader} */}
                    {!this.state.imageLoaded && imageContentLoader}
                    <PreloadImage src={this.props.link}
                        onImageLoaded={this.onImageLoaded.bind(this)} />
                    {/* {img} */}
                </div>
            </div>
        );
    }
}

export default Post;

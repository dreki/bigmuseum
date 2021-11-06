import * as React from 'react';
import ContentLoader from 'react-content-loader';
import PreloadImage from './PreloadImage';
// import ReactPlaceholder from 'react-placeholder';

interface IPostProps {
    id: string;
    title: string;
    link: string;
    // key: number;
    onTrashPost?: ((postId: string) => void),
}

interface IPostState {
    imageLoaded: boolean;
}


class Post extends React.Component<IPostProps, IPostState> {
    constructor(props: IPostProps) {
        super(props);
        console.log(props);
        this.state = {
            imageLoaded: false
        };
    }

    onImageLoaded(e: React.SyntheticEvent) {
        this.setState({ imageLoaded: true })
    }

    onTrashPost(e: React.SyntheticEvent) {
        if (this.props.onTrashPost) {
            this.props.onTrashPost(this.props.id);
        }
    }

    render() {
        const imageContentLoader: JSX.Element = (
            <ContentLoader viewBox="0 0 450 400">
                <rect x="0" y="0" rx="0" ry="0" width="450" height="400" />
            </ContentLoader>
        );

        return (
            <div className={'bi-avoid shadow-sm rounded'}>
                <div className={'border border-moody-blue-500 rounded border-b-0 rounded-b-none pb-1.5'}>
                    {!this.state.imageLoaded && imageContentLoader}
                    <PreloadImage src={this.props.link}
                        onImageLoaded={this.onImageLoaded.bind(this)} />

                    <h3 className={'text-l font-work-sans italic p-1 pr-2 pl-2'}>{this.props.title}</h3>
                </div>
                <div className={'flex items-center justify-center mb-4'}>
                    <button
                        className={'w-2/3 text-moody-blue-500 bg-transparent border-l border-t border-r border-b border-moody-blue-500 hover:bg-moody-blue-500 hover:text-white active:bg-moody-blue-600 font-bold uppercase text-sm px-6 py-3 rounded-bl outline-none focus:outline-none ease-linear transition-all duration-150'}
                    >
                        Add
                    </button>
                    {/* 
                    <button
                        className={'w-1/3 text-moody-blue-500 bg-transparent border border-solid border-moody-blue-500 hover:bg-moody-blue-500 hover:text-white active:bg-moody-blue-600 font-bold uppercase text-sm px-6 py-3 outline-none focus:outline-none ease-linear transition-all duration-150'}
                    >
                        Center
                    </button>
                    */}
                    <button
                        className={'w-1/3 text-moody-blue-500 bg-transparent border-t border-b border-r border-moody-blue-500 hover:bg-moody-blue-500 hover:text-white active:bg-moody-blue-600 font-bold uppercase text-sm px-6 py-3 rounded-br outline-none focus:outline-none ease-linear transition-all duration-150'}
                        onClick={this.onTrashPost.bind(this)}
                    >
                        🗑
                    </button>
                </div>
            </div>
        );
    }
}

export default Post;

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

    render() {
        const imageContentLoader: JSX.Element = (
            <ContentLoader viewBox="0 0 450 400">
                <rect x="0" y="0" rx="0" ry="0" width="450" height="400" />
            </ContentLoader>
        );

        return (
            <div>
                <div className={'border rounded shadow-sm mb-4 bi-avoid'}>
                    {!this.state.imageLoaded && imageContentLoader}
                    <PreloadImage src={this.props.link}
                        onImageLoaded={this.onImageLoaded.bind(this)} />

                    <h3 className={'text-xl font-work-sans italic p-1'}>{this.props.title}</h3>

                    <div className={'flex items-center justify-center'}>
                        <button
                            className={'w-1/3 text-purple-500 bg-transparent border-l border-t border-b border-purple-500 hover:bg-purple-500 hover:text-white active:bg-purple-600 font-bold uppercase text-sm px-6 py-3 rounded-bl outline-none focus:outline-none ease-linear transition-all duration-150'}
                        >
                            Left
                        </button>
                        <button
                            className={'w-1/3 text-purple-500 bg-transparent border border-solid border-purple-500 hover:bg-purple-500 hover:text-white active:bg-purple-600 font-bold uppercase text-sm px-6 py-3 outline-none focus:outline-none ease-linear transition-all duration-150'}
                        >
                            Center
                        </button>
                        <button
                            className={'w-1/3 text-purple-500 bg-transparent border-t border-b border-r border-purple-500 hover:bg-purple-500 hover:text-white active:bg-purple-600 font-bold uppercase text-sm px-6 py-3 rounded-br outline-none focus:outline-none ease-linear transition-all duration-150'}
                        >
                            Right
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}

export default Post;

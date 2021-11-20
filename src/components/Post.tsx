import * as React from 'react';
import ContentLoader from 'react-content-loader';
import { CSSTransition } from 'react-transition-group';
import PreloadImage from './PreloadImage';
// import ReactPlaceholder from 'react-placeholder';

/**
 * typedef for Post props
 */
interface IPostProps {
    id: string;
    title: string;
    link: string;
    // key: number;
    onCollectPost?: ((postId: string) => void),
    onTrashPost?: ((postId: string) => void),
}

/**
 * typedef for Post state
 */
interface IPostState {
    imageLoaded: boolean;
    unloading: boolean;
}

/**
 * Post component
 */
class Post extends React.Component<IPostProps, IPostState> {
    /**
     * Constructor
     * @param props {IPostProps}
     */
    constructor(props: IPostProps) {
        super(props);
        console.log(props);
        this.state = {
            imageLoaded: false,
            unloading: false,
        };
    }

    /**
     * Keep track of when component is unloading.
     */
    public componentWillUnmount() {
        // Note that we're unloading.
        this.setState({ unloading: true });
    }

    /**
     * React when image loaded.
     * @param e {React.SyntheticEvent}
     * @returns {void}
     */
    onImageLoaded = (e: React.SyntheticEvent): void => {
        this.setState({ imageLoaded: true })
    }

    /**
     * Listen to clicks on the collect button.
     * @param e {React.SyntheticEvent}
     * @returns {void}
     */
    onCollectPost = (e: React.SyntheticEvent): void => {
        e.preventDefault();
        if (!this.props.onCollectPost) { return; }
        this.props.onCollectPost(this.props.id);
    }

    /**
     * Listen to clicks on the trash button.
     * @param e {React.SyntheticEvent}
     * @returns {void}
     */
    onTrashPost(e: React.SyntheticEvent): void {
        e.preventDefault();
        if (!this.props.onTrashPost) { return; }
        this.props.onTrashPost(this.props.id);
    }

    private renderCollectButton() {
        return <button
            className={'w-2/3 text-moody-blue-500 bg-transparent border-l border-t border-r border-b border-moody-blue-500 hover:bg-moody-blue-500 hover:text-white active:bg-moody-blue-600 font-bold uppercase text-sm px-6 py-3 rounded-bl outline-none focus:outline-none ease-linear transition-all duration-150'} onClick={this.onCollectPost}
        >
            Add
        </button>;
    }
    private renderImage() {
        return (
            <div className={'border border-moody-blue-500 rounded border-b-0 rounded-b-none pb-1.5'}>
                {!this.state.imageLoaded && this.renderImageContentLoader()}
                <PreloadImage src={this.props.link} onImageLoaded={this.onImageLoaded.bind(this)} />
                <h3 className={'text-l font-work-sans italic p-1 pr-2 pl-2'}>{this.props.title}</h3>
            </div>
        );
    }

    private renderImageContentLoader(): React.ReactNode {
        return (
            <ContentLoader viewBox="0 0 450 400">
                <rect x="0" y="0" rx="0" ry="0" width="450" height="400" />
            </ContentLoader>
        );
    }

    /**
     * Render the post.
     * @returns {React.ReactNode}
     */
    render(): React.ReactNode {
        return (
            <CSSTransition in={!this.state.unloading} timeout={500} classNames={'post-animation'}>
                <div className={'bi-avoid shadow-sm rounded'}>
                    {this.renderImage()}
                    <div className={'flex items-center justify-center mb-4'}>
                        {this.renderCollectButton()}
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
            </CSSTransition>
        );
    }



}

export default Post;

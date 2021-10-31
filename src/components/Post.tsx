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
                    <span>{this.props.title}</span>

                    {!this.state.imageLoaded && imageContentLoader}
                    <PreloadImage src={this.props.link}
                        onImageLoaded={this.onImageLoaded.bind(this)} />
                </div>
            </div>
        );
    }
}

export default Post;

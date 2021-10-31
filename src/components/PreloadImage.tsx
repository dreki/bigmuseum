import * as React from 'react';

// interface IPreloadImageProps extends React.HTMLProps<HTMLImageElement> {
interface IPreloadImageProps extends React.HTMLAttributes<HTMLImageElement> {
    src: string;
    onImageLoaded?: (() => void);
}

interface IPreloadImageState {
    imageLoaded: boolean;
}

class PreloadImage extends React.Component<IPreloadImageProps, IPreloadImageState> {
    constructor(props: IPreloadImageProps) {
        super(props);
        this.state = { imageLoaded: false };
    }

    onImageLoad(e: React.SyntheticEvent) {
        this.setState({ imageLoaded: true });
        if (this.props.onImageLoaded) {
            this.props.onImageLoaded();
        }
    }

    render() {
        let className: string = 'hidden';
        if (this.state.imageLoaded) {
            className = '';
        }
        return (
            <>
                <img src={this.props.src}
                    className={`${this.props.className} ${className}`}
                    onLoad={this.onImageLoad.bind(this)} />
            </>
        )
    }
}

export default PreloadImage;

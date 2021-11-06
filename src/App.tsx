import * as React from "react";
import Posts from './components/Posts';
import Test from './components/Test';
import fetch from 'cross-fetch';

interface IAppProps {
    name: string
}

interface IAppState {
    posts: Array<{ title: string, link: string }>
}

class App extends React.Component<IAppProps, IAppState> {
    state: IAppState = {
        posts: []
    }

    public async componentDidMount(): Promise<void> {
        // Load and set posts.
        const response = await fetch('/api/posts/new');
        const posts: Array<{ title: string, link: string }> = (await response.json()).items;
        this.setState({ posts: posts })
    }

    render() {
        const { name } = this.props;
        return (
            <>
                <h2 className={'text-2xl mt-5 mb-4'}>New Arrivals</h2>
                <Posts posts={this.state.posts} />
            </>
        );
    }
}

export default App;

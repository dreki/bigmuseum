
import React from "react";
import Posts from './components/Posts';
import Test from './components/Test';
import fetch from 'cross-fetch';

interface IAppProps {
  name: string
}

interface IAppState {
  posts: Array<object>
}

class App extends React.Component<IAppProps, IAppState> {
  state: IAppState = {
    posts: []
  }

  public async componentDidMount(): Promise<void> {
    const response = await fetch('/api/posts/new');
    console.log(`> response:`);
    console.log(response);
    const posts: Array<object> = (await response.json()).items;
    console.log(posts);
    this.setState({ posts: posts })
  }

  render() {
    const { name } = this.props;
    return (
      <>
        <h1 className="text-4xl text-white bg-black">
          Hello {name}
        </h1>
        <div className="card">
          Reddit post card
        </div>
        <Test message={'fun'} />
        <Posts posts={this.state.posts} />
      </>
    );
  }
}

export default App;

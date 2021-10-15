
import React from "react";
import Posts from './components/Posts';
import Test from './components/Test';

class App extends React.Component {
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
        <Test />
        <Posts posts={[{}]} />
      </>
    );
  }
}

export default App;

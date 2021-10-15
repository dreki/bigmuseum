
import * as React from 'react';

// type Props = {
//     message: string
// };

// type State = {
//     count: number
// };

// import * as React from 'react';

export interface ITestProps {
  message: string;
}

export interface ITestState {
  count: number;
}

export default class Test extends React.Component<ITestProps, ITestState> {
  state: ITestState = {
    count: 0
  };
  constructor(props: ITestProps) {
    super(props);
    // this.state = {
    // }
  }
  public onClick(e: React.SyntheticEvent): void {
    console.log(`> onClick`);
  }

  public render() {
    return (
      <div>
        <span>Neato</span>
        <button onClick={this.onClick.bind(this)}>Click</button>
      </div>
    );
  }
}



// class Test extends React.Component<Props, State> {
//     state: State = {
//         count: 0
//     };
//     render() {
//         return (
//             <div>Neato</div>
//         );
//     }
// }

// export default Test;

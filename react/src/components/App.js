import React from 'react';
import Header from './Header';
import Content from './Content';

class App extends React.Component {

    sayHello(){
      alert('Hello');
    }

    render(){

      let text = 'Dev-Server';

      let pStyle = {
        color : 'yellow',
        backgroundColor : 'black'
      };

        return (
          <div>
            <h1>Hello Monkey</h1>
            <h2>Welocome to Monkey {text}</h2>
            <button onClick={this.sayHello}>Greetings</button>
            <p style={pStyle}>{1==1 ? 'true':'false'}</p>
            <Header/>
            <Content/>
          </div>
      );
    }
}

export default App;

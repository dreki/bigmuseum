import React from 'react';
import ReactDOM from 'react-dom';
// import App from "./App";
import Router from './Router';
import './styles.css';

var mountNode = document.getElementById('app');
// ReactDOM.render(<App name='Little Janey' />, mountNode);
ReactDOM.render(<Router/>, mountNode);
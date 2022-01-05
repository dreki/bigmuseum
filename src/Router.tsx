import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import App from './App';

function Router() {
    return (
        <BrowserRouter basename='/app'>
            <Routes>
                <Route path="/" element={<App name={'Little Janey'} />} />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
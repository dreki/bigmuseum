import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Collection from './Collection';
import NewPosts from './NewPosts';

function Router() {
    return (
        <BrowserRouter basename='/app'>
            <Routes>
                <Route path="/" element={<NewPosts name={'Little Janey'} />} />
                <Route path="/collection" element={<Collection />} />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
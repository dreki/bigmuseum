import React from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import Collection from './Collection';
import NewPosts from './NewPosts';

function Router() {
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<NewPosts name={'Little Janey'} />} />
                <Route path="/collection" element={<Collection />} />
            </Routes>
        </HashRouter>
    );
}

export default Router;
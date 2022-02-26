import React from 'react';
// import { HashRouter, Route, Routes } from 'react-router-dom';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Collection from './Collection';
import NewPosts from './NewPosts';

function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/app/" element={<NewPosts name={'Little Janey'} />} />
                <Route path="/app/posts" element={<NewPosts name={'Little Janey'} />} />
                <Route path="/app/collection" element={<Collection />} />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
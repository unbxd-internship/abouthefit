import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomeScreen from './screens/HomeScreen'
import ProductScreen from './screens/ProductScreen'
import React, { useEffect, useState } from 'react'


function App() {
//routing of pages and urls

  return (
    <Router forceRefresh={true}>
      <Header />
      <main className="py-3">
        <Container>
          <Route path='/' component={HomeScreen} exact/>
          <Route path='/product' component={ProductScreen} />
          <Route path="/category" component={HomeScreen} />
          <Route path="/search" component={HomeScreen} />
        </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;

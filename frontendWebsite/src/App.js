import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomeScreen from './screens/HomeScreen'
import ProductScreen from './screens/ProductScreen'
import React, { useEffect, useState } from 'react'
//import axios from 'axios'



function App() {

  const [getMessage, setGetMessage]= useState({})
  
  // useEffect(()=>{
  //   axios.get('http://localhost:5000/backendWebsite/FrontPage').then(response => {
  //     console.log("SUCCESS", response)
  //     setGetMessage(response)
  //   }).catch(error => {
  //     console.log(error)
  //   })

  // }, [])
  
  return (
    <Router>
      <Header/>
      <main className="py-3">
        <Container>
          {/*<HomeScreen />*/}
          <Route path='/' component={HomeScreen} exact/>
          <Route path='/product/:sku' component={ProductScreen} />
          
        </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;

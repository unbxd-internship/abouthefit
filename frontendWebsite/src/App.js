import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomeScreen from './screens/HomeScreen'
//import CategoryScreen from './screens/CategoryScreen'
import ProductScreen from './screens/ProductScreen'
//import SearchScreen from './screens/SearchScreen'
import React, { useEffect, useState } from 'react'

//import axios from 'axios'



function App() {

  const [getMessage, setGetMessage]= useState("");
  // const [query, setQuery]=useState("");
  // const [category, setCategory]=useState("");

  
  // useEffect(()=>{
  //   axios.get('http://localhost:5000/backendWebsite/FrontPage').then(response => {
  //     console.log("SUCCESS", response)
  //     setGetMessage(response)
  //   }).catch(error => {
  //     console.log(error)
  //   })

  // }, [])
  // const onSearch = (query = "") => {
  //   setQuery(query)
  // }
  // const onCategory = (category = "") => {
  //   setCategory(category)
  // }
  return (
    <Router>
      <Header />
      <main className="py-3">
        <Container>
          {/*<HomeScreen />*/}
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

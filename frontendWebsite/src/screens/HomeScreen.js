
//import Pagination from 'react-js-pagination'

import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
import CategoryDropdown from '../components/CategoryDropdown'
import { useHistory } from 'react-router-dom'
//import products from '../products'

function HomeScreen() {
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState({});
  //const history = useHistory(); 

  useEffect(() => {
    //history.listen((location) => {
     // console.log(`You changed the page to: ${window.location.pathname}`)
    //})
    let endpoint = '/'
    const url = new URLSearchParams(window.location.search)
    const path = window.location.pathname.split('/');
    console.log(path)
    if(url.has('q')){
      endpoint = `/search?q=${url.get('q')}`
    } else if(path[1]==='category'){
    setCategory({
      c1: path[2],
      c2: path[3],
    });
    console.log("in category filter")
    console.log(category.c1, category.c2)
    endpoint = `/category/${category.c1}/${category.c2}`
    }
    client.get(endpoint).then((res) => {
    setProducts(res.data.products);
    }).catch(err => { console.log(err); })
  }, [window.location.pathname])
  

    
 
  return (
    <div>
      <select>
        <option value="relevance">Relevance</option>
        <option value="price asce">Price: Low to High</option>
        <option value="price desc">Price: High to Low</option>
      </select>
      <Row>
        {products.map(product => (
          <Col key={product.sku} sm={12} md={6} lg={4} xl={3}>
            <Product product={product} />
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default HomeScreen;

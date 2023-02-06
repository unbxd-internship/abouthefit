
//import Pagination from 'react-js-pagination'

import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
import CategoryDropdown from '../components/CategoryDropdown'
import { useHistory, useLocation } from 'react-router-dom'
//import products from '../products'

function HomeScreen() {
  const [products, setProducts] = useState([]);
  const { pathname, search } = useLocation();
  const endpoint = pathname + search;

  useEffect(() => {
    client
      .get(endpoint)
      .then((res) => {
        setProducts(res.data.products);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [endpoint]);
  

    
 
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

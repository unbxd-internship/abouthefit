
//import Pagination from 'react-js-pagination'

import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
//import products from '../products'

function HomeScreen({ match }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        let res;
        if (match.params.catlevel1name && match.params.catlevel2name) {
          res = await client.get(`/category/${match.params.catlevel1name}/${match.params.catlevel2name}`);
          
        
        } else {
          res = await client.get('/category');
          console.log(res)
        }
        setProducts(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProducts();
  }, [match.params.catlevel1name, match.params.catlevel2name]);

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

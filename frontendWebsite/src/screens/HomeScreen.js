import React from 'react'
import {Row, Col} from 'react-bootstrap'
import products from '../products'
import Product from '../components/Product'

function HomeScreen() {
  
  return (
    <div>
      <h1>                   </h1>
        <select>
          <option value="albums">Relevance</option>
          <option value="members">Price: Low to High</option>
          <option value="formed">Price: High to Low</option>
        </select>
      <Row>
        {products.map(product=>(
            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                <Product product={product} />
            </Col>
            
        ))}
        
      </Row>
    </div>
  )
}

export default HomeScreen

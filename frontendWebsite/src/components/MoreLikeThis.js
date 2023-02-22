import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
import CategoryDropdown from '../components/CategoryDropdown'
import { useHistory, useLocation } from 'react-router-dom'

function MoreLikeThis(){
    const location= useLocation();
    const product=location.state.productClicked;
    console.log(product)
    const sku=product.sku;
    console.log(sku);
    const [products, setProducts] = useState([]);
    console.log("in more like this")
    let endpoint=`/recommend/${sku}`
    console.log(endpoint)
    
    useEffect(() => {
        client
        .get(endpoint) //call to API with current url endpoint
        .then((res) => {
          setProducts(res.data);
        })
        .catch((err) => {
          console.log(err);
          endpoint='/'
          client.get(endpoint).then((res)=>{setProducts(res.data)})
          console.log(endpoint)
          
        });
      }, []);

    return(
        <div>
            <Row>
                {products.map(product => (
                    <Col key={product.sku} sm={12} md={6} lg={4} xl={3}>
                        <Product product={product} />
                    </Col>
                ))}
            </Row>
        </div>
    )
}

export default MoreLikeThis; 
import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card } from 'react-bootstrap'
//  import products from '../products';
import { useParams, useLocation } from 'react-router-dom'
import props from 'prop-types'
import { client } from '../utils/axios.util';

//to load product screen on click of any product 

function ProductScreen() {

    const [product, setProduct] = useState([]);
    const [id, setId]=useState(""); //to store sku of product to be loaded in product screen
    const location= useLocation();
    const {productClicked}=location.state;
 

    useEffect(() => {
        let endpoint = '/'
        const url = new URLSearchParams(window.location.search)
        const path = window.location.pathname.split('/');
        setId(path[2]);
        endpoint = `/product/${id}`
        
        client.get(endpoint).then((res) => {
            setProduct(res.data);
        }).catch(err => { 
            console.log(err); 
            setProduct(productClicked)
        })
      }, [id])
   
      
    return (
        
        <div>  
            <Row>
                <Col md={6}>    
                    <Image src={product.productimage} alt={product.title} fluid />
                </Col>
                <Col md={3}>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            <h3>{product.title}</h3>
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Price: $ {product.price}
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Description: {product.productdescription}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>
                <Col md={3}></Col>
            </Row>
    </div>
    )
   
}

export default ProductScreen

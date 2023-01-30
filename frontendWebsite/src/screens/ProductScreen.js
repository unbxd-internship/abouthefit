import React from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card } from 'react-bootstrap'
import products from '../products';
import { useParams } from 'react-router-dom'
import props from 'prop-types'

function ProductScreen({match}) {
    
    const temp = useParams();
    

    
    const findproduct=products.find((p)=>p.sku===temp.sku)
    
    
    return (
        
        <div>
            <Link to='/' className='btn btn-light my-3'>Go Back</Link>
            
            <Row>
                <Col md={6}>    
                    <Image src={findproduct.productImage} alt={findproduct.title} fluid />
                </Col>
                <Col md={3}>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            <h3>{findproduct.title}</h3>
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Price: $ {findproduct.price}
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Description: {findproduct.productDescription}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>
                <Col md={3}></Col>
            </Row>
    </div>
    )
}

export default ProductScreen

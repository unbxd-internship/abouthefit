import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card } from 'react-bootstrap'
//  import products from '../products';
import { useParams } from 'react-router-dom'
import props from 'prop-types'
import { client } from '../utils/axios.util';

function ProductScreen() {

    const [product, setProduct] = useState([]);
    const [id, setId]=useState("");
    const refresh = () => window.location.reload(true);

    useEffect(() => {
        let endpoint = '/'
        const url = new URLSearchParams(window.location.search)
        const path = window.location.pathname.split('/');
        console.log(path)
        setId(path[2]);
        console.log("in product screen")
        console.log("id=", id)
        endpoint = `/product/${id}`
        client.get(endpoint).then((res) => {
            console.log("data")
            console.log(res.data)
            setProduct(res.data);
            refresh();
        }).catch(err => { console.log(err); })
      }, [id])
    console.log("product")
    console.log(product)
    
    
    return (
        
        <div>
            <Link to='/' className='btn btn-light my-3'>Go Back</Link>
            
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

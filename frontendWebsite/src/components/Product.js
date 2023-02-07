    import React from 'react'
    import { Card } from 'react-bootstrap'
    import { Link } from 'react-router-dom'

    function Product({product}) {
    return (
        <Card className=" my-3 p-3 rounded">
            <Link to={`/product/${product.sku}`}>
                <Card.Img src= {product.productimage} />
            </Link>

            <Card.Body>
                <Link to={`/product/${product.sku}`}>
                    <Card.Title as="div"> 
                        <strong> {product.title}</strong>
                    </Card.Title>
                </Link>
                <Card.Text as="h3">
                        $ {product.price}
                </Card.Text> 
                
                {/*<Card.Text>
                    <div className="my-3">
                        {product.rating} from {product.numReviews}
                    </div>
                </Card.Text>
                
                <Card.Text as="h3">
                    {product.sku}
                </Card.Text> */}

            </Card.Body>
        
        </Card>
        
    )
    }

    export default Product

import React from 'react'
import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'


//to load products onto display in cards

function Product({product}) {

    const productClicked=[];
    

    return (
        <Card className=" my-3 p-3 rounded">
            <Link to={{
                pathname: `/product/${product.sku}`,
                state: { 
                    productClicked: product,     
                }
            }}>
                <Card.Img src= {product.productimage} />
            </Link>
            <Card.Body>
                <Link to={{
                    pathname: `/product/${product.sku}`,
                    state: { productClicked: product}
                }}>
                    <Card.Title as="div"> 
                        <strong> {product.title}</strong>
                    </Card.Title>
                </Link>
                <Card.Text as="h3">
                        $ {product.price}
                </Card.Text> 

            </Card.Body>
        
        </Card>
        
    )
    }

    export default Product

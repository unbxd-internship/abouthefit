import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'

//to add footer to all screens

function Footer() {
  return (
    <footer>
      <Container>
        <Row>
            <Col className="text-center py-3">Copyright &copy; About The Fit</Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer

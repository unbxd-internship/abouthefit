import React from 'react'
import { Navbar, Nav, Container, Row } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import Dropdown from 'react-bootstrap/Dropdown'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
function Header() {
  return (
    <Navbar bg="dark" variant= "dark" expand="lg">
      <Container>
          <Navbar.Brand href="#home">About The Fit</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <NavDropdown title="Men" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Pants</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Shirts</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Jackets</NavDropdown.Item> 
            </NavDropdown> 
            <NavDropdown title="Women" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Pants</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Shirts</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Jackets</NavDropdown.Item> 
            </NavDropdown>   
            <NavDropdown title="EXP" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Pants</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Shirt</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Jackets</NavDropdown.Item> 
            </NavDropdown> 
          </Nav>
          <Form className="d-flex">
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
            />
            <Button variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header

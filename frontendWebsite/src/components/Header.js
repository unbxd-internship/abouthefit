import React, { useState, useEffect } from "react";
import { Navbar, Nav, Container, Form, Button, Dropdown, ListGroup } from "react-bootstrap";
import { client } from '../utils/axios.util'
import { useHistory, Link } from 'react-router-dom';
import SearchBox from '../components/SearchBox'
import CategoryDropdown from '../components/CategoryDropdown'
//import SearchScreen from "../screens/SearchScreen";


function Header({props}) {
  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
          <Navbar.Brand href="#home">About The Fit</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <CategoryDropdown  />
            <SearchBox  />
          </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}


export default Header

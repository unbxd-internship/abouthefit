import React, { useState, useEffect } from "react";
import { Navbar, Nav, Container, Form, Button, Dropdown, ListGroup } from "react-bootstrap";
import { client } from '../utils/axios.util'
import { useHistory } from 'react-router-dom';

function Header() {
  const [catLevelNames, setCatLevelNames] = useState({});
  const [error, setError] = useState('');
  const history = useHistory();

  useEffect(() => {
    const fetchLevelNames = async () => { 
      try {
        const res = await client.get("/get_category");
        setCatLevelNames(res.data);
      } catch (err) {
        setError(err.toString());
      }
    }
    fetchLevelNames();
  }, []);

  const handleClick = (catlevel1, catlevel2) => {
    history.push(`/${catlevel1}/${catlevel2}`);
  }

  const render = () => {
    if (error) return <p>{error}</p>;
    if (!catLevelNames || !catLevelNames.cat_headers || !catLevelNames.cat_headers.length) return null;
    
    const menuItems = [];
    const {cat_headers, sub_cats} = catLevelNames;

    for (const catlevel1 of cat_headers) {
      const subCategories = sub_cats[catlevel1];
      if (!subCategories || !subCategories.length) continue;
      const subCategoryItems = subCategories.map((catlevel2) => (
        <ListGroup.Item key={catlevel2} onClick={() => handleClick(catlevel1, catlevel2)}>{catlevel2}</ListGroup.Item>
      ));

      menuItems.push(
        <Nav.Item key={catlevel1}>
          <Dropdown>
            <Dropdown.Toggle variant="dark" bg="dark" expand="lg" id={catlevel1}>
              {catlevel1}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <ListGroup>
                {subCategoryItems}
              </ListGroup>
            </Dropdown.Menu>
          </Dropdown>
        </Nav.Item>
      );
    }

    return menuItems;
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
          <Navbar.Brand href="#home">About The Fit</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {render()}
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

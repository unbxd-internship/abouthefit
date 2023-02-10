import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
import CategoryDropdown from '../components/CategoryDropdown'
import { useHistory, useLocation } from 'react-router-dom'

//Main screen with products. All functionalities: search, category filters,
//sort and pagination reload this page with updated url and API calls
//10 products displayed on a single page

function HomeScreen() {
  const [products, setProducts] = useState([]); //state variable to store array of products
  const { pathname, search } = useLocation(); 
  const refresh = () => window.location.reload(true); //function to reload window
  const history=useHistory();
  const [endpoint, setEndpoint] = useState(pathname + search);
  const [totalPages, setTotalPages]=useState(0);  //state variable to store total number of pages 
  const [pageNumber, setPageNumber]=useState(0);
  
    useEffect(() => {
      client
      .get(endpoint) //call to API with current url endpoint
      .then((res) => {
        setProducts(res.data.products);
        setPageNumber(res.data.PageNumber);
        setTotalPages(res.data.TotalNumberOfPages);
        
      })
      .catch((err) => {
        console.log(err);
      });
    }, [endpoint]);
   


    const handleMenuOne = () => {
      setEndpoint(`${pathname}`)// handle sort by relevance
      history.push(`${pathname}`)
    }

    const handleMenuTwo = () => {
      const urlWithParams = new URL(window.location.href);
      if (urlWithParams.searchParams.has('q')){
        const query=urlWithParams.searchParams.get('q'); // handle sort by price low to high
        setEndpoint(`${pathname}?q=${query}&sort=price asce`);
        history.push(`${pathname}?q=${query}&sort=price asce`);
      }
      else{
        setEndpoint(`${pathname}?sort=price asce`)
        history.push(`${pathname}?sort=price asce`)
      }
    }

    const handleMenuThree = () => {
      const urlWithParams = new URL(window.location.href); //handle sort by price high to low
      if (urlWithParams.searchParams.has('q')){
        const query=urlWithParams.searchParams.get('q');
        setEndpoint(`${pathname}?q=${query}&sort=price desc`);
        history.push(`${pathname}?q=${query}&sort=price desc`);
      }
      else{
        setEndpoint(`${pathname}?sort=price desc`)
        history.push(`${pathname}?sort=price desc`)
      }
    }

    const handlePageClick = (page) => {
      const urlWithParams = new URL(window.location.href); //handle change in page in pagination
      urlWithParams.searchParams.set("page", page);
      const { pathname, search } = urlWithParams;
      history.push(pathname + search);
      setEndpoint(pathname+search);
      refresh();
      
    };
    const handlePrevClick = () => {
      handlePageClick(pageNumber - 1); //to handle previous page click
    };

    const handleNextClick = () => {
      handlePageClick(pageNumber + 1); //to handle next page click
    };

    const handleFirstPage = () => {
      handlePageClick(1); //to go to first page
    };

    const handleLastPage = () => {
      handlePageClick(totalPages); //to go to last page
    };

    return (
      <div>
        <div>
          <Dropdown
            trigger={<button>Sort By</button>}
            menu={[
              <button onClick={handleMenuOne}>Relevance</button>,
              <button onClick={handleMenuTwo}>Price: Low to High</button>,
              <button onClick={handleMenuThree}>Price: High to Low</button>,
            ]}
          />
          <Row>
            {products.map(product => (
              <Col key={product.sku} sm={12} md={6} lg={4} xl={3}>
                <Product product={product} />
              </Col>
            ))}
          </Row>
        </div>
        <div className="d-flex justify-content-center mt-5">
          <h5>
            Page {pageNumber} of {totalPages}
          </h5>
        </div>
        <div className="d-flex justify-content-center mt-3">
          <nav aria-label="Page navigation example">
            <ul className="pagination">
            {pageNumber > 1 && (
                <li className="page-item">
                  <button
                    className="page-link"
                    onClick={() => handleFirstPage()}
                  >
                    1
                  </button>
                </li>
              )}
              {pageNumber > 1 && (
                <li className="page-item">
                  <button
                    className="page-link"
                    onClick={() => handlePrevClick()}
                  >
                    Previous Page
                  </button>
                </li>
              )}
          
              {pageNumber < totalPages && (
                <li className="page-item">
                  <button
                    className="page-link"
                    onClick={() => handleNextClick()}
                  >
                    Next Page
                  </button>
                
                </li>
              )}
               {pageNumber < totalPages && (
                <li className="page-item">
                  <button
                    className="page-link"
                    onClick={() => handleLastPage()}
                  >
                    {totalPages}
                  </button>
                
                </li>
              )}
            </ul>
          </nav>
        </div>
      </div>
    );
  };

  const Dropdown = ({ trigger, menu }) => {
    const [open, setOpen] = React.useState(false);

    const handleOpen = () => {
      setOpen(!open);
    };

    return (
      <div className="dropdown">
        {React.cloneElement(trigger, {
          onClick: handleOpen,
        })}
        {open ? (
          <ul className="container">
            {menu.map((menuItem, index) => (
              <li key={index} className="container">
                {React.cloneElement(menuItem, {
                  onClick: () => {
                    menuItem.props.onClick();
                    setOpen(false);
                  },
                })}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    );
  };



  export default HomeScreen;

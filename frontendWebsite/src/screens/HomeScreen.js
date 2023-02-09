import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { client } from '../utils/axios.util';
import Product from '../components/Product';
import CategoryDropdown from '../components/CategoryDropdown'
import { useHistory, useLocation } from 'react-router-dom'

//import products from '../products'


function HomeScreen() {
  const [products, setProducts] = useState([]);
  const { pathname, search } = useLocation();
  
  const history=useHistory();
  //const endpoint=pathname+search;
  const [endpoint, setEndpoint] = useState(pathname + search);
  //const [productsCount, setProductsCount]=useState(0);
  const [totalPages, setTotalPages]=useState(0);  
  const [pageNumber, setPageNumber]=useState(0);
  
    useEffect(() => {
      client
      .get(endpoint)
      .then((res) => {
        setProducts(res.data.products);
        setPageNumber(res.data.PageNumber);
        setTotalPages(res.data.TotalNumberOfPages);
        //setProductsCount(res.data.ProductCount);
        
      })
      .catch((err) => {
        console.log(err);
      });
    }, [endpoint]);


    const handleMenuOne = () => {
      setEndpoint(`${pathname}`)
      history.push(`${pathname}`)
    }

    const handleMenuTwo = () => {
      const urlWithParams = new URL(window.location.href);
      if (urlWithParams.searchParams.has('q')){
        const query=urlWithParams.searchParams.get('q');
        setEndpoint(`${pathname}?q=${query}?sort=price asce`);
        history.push(`${pathname}?q=${query}?sort=price asce`);
      }
      else{
        setEndpoint(`${pathname}?sort=price asce`)
        console.log(endpoint)
        history.push(`${pathname}?sort=price asce`)
      }
    }

    const handleMenuThree = () => {
      const urlWithParams = new URL(window.location.href);
      if (urlWithParams.searchParams.has('q')){
        const query=urlWithParams.searchParams.get('q');
        setEndpoint(`${pathname}?q=${query}?sort=price desc`);
        history.push(`${pathname}?q=${query}?sort=price desc`);
      }
      else{
        setEndpoint(`${pathname}?sort=price desc`)
        console.log(endpoint)
        history.push(`${pathname}?sort=price desc`)
      }
    }

    const handlePageClick = (page) => {
      const urlWithParams = new URL(window.location.href);
      urlWithParams.searchParams.set("page", page);
      const { pathname, search } = urlWithParams;
      history.push(pathname + search);
      setEndpoint(pathname+search);
      
    };
    const handlePrevClick = () => {
      handlePageClick(pageNumber - 1);
    };

    const handleNextClick = () => {
      handlePageClick(pageNumber + 1);
    };

    const handleFirstPage = () => {
      handlePageClick(1);
    };

    const handleLastPage = () => {
      handlePageClick(totalPages);
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

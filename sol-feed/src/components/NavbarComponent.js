import '../index.css';
import { ReactComponent as CaretIcon } from '../img/caret.svg';
import { ReactComponent as ArrowIcon } from '../img/arrow.svg';
import { ReactComponent as BoltIcon } from '../img/bolt.svg';
import { ReactComponent as HomeIcon} from '../img/home.svg'
import { ReactComponent as EyeIcon} from '../img/eye.svg'
import { ReactComponent as ChevronIcon } from '../img/chevron.svg';
import React, { useState, useEffect, useRef } from 'react';
import { CSSTransition } from 'react-transition-group';
import {Link} from 'react-router-dom'

function NavbarItem() {
    return (<>
        <Navbar>
          <EyeIcon/>&nbsp;&nbsp;
            <h1>SolFeed&nbsp;&nbsp;</h1>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <NavItem icon={<CaretIcon />}>
            <DropdownMenu></DropdownMenu>
          </NavItem>
        </Navbar>
        

        
        </>
      );
    }
    
    function Navbar(props) {
      return (
        <nav className="navbar">
          <ul className="navbar-nav">{props.children}</ul>
        </nav>
      );
    }
    
    function NavItem(props) {
      const [open, setOpen] = useState(false);
    
      return (
        <li className="nav-item">
          <div className="icon-button" onClick={() => setOpen(!open)}>
            {props.icon}
          </div>
    
          {open && props.children}
        </li>
      );
    }
    
    function DropdownMenu() {
      const [activeMenu, setActiveMenu] = useState('main');
      const [menuHeight, setMenuHeight] = useState(null);
      const dropdownRef = useRef(null);
    
      useEffect(() => {
        setMenuHeight(dropdownRef.current?.firstChild.offsetHeight)
      }, [])
    
      function calcHeight(el) {
        const height = el.offsetHeight;
        setMenuHeight(height);
      }
    
      function DropdownItem(props) {
        return (
          <div className="menu-item" onClick={() => props.goToMenu && setActiveMenu(props.goToMenu)}>
            <span className="icon-button">{props.leftIcon}</span>
            {props.children}
            <span className="icon-right">{props.rightIcon}</span>
          </div>
        );
      }
    
      return (
        <div className="dropdown" style={{ height: menuHeight }} ref={dropdownRef}>
    
          <CSSTransition
            in={activeMenu === 'main'}
            timeout={500}
            classNames="menu-primary"
            unmountOnExit
            onEnter={calcHeight}>
            <div className="menu">
              <DropdownItem
              leftIcon={<HomeIcon />}>
                <Link to="/">Home</Link>
              </DropdownItem>
              <DropdownItem
                leftIcon={<EyeIcon />}
                rightIcon={<ChevronIcon />}
                goToMenu="settings">
                Influencers
              </DropdownItem>
            </div>
          </CSSTransition>
    
          <CSSTransition
            in={activeMenu === 'settings'}
            timeout={500}
            classNames="menu-secondary"
            unmountOnExit
            onEnter={calcHeight}>
            <div className="menu">
              <DropdownItem goToMenu="main" leftIcon={<ArrowIcon />}>
                <h2>Influencers</h2>
              </DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/cozy">CozyTheCaller</Link></DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/jpeggler">Jpeggler</Link></DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/angilo">CryptoAngilo</Link></DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/jagoe">Jagoe</Link></DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/ravers">Ravers</Link></DropdownItem>
              <DropdownItem leftIcon={<BoltIcon />}><Link to="/rivers">Nate Rivers</Link></DropdownItem>
            </div>
          </CSSTransition>
        </div>
        
      );
    }

export default NavbarItem;
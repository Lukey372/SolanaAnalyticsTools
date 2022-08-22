import './index.css';
import { Route, HashRouter as Router, Routes } from "react-router-dom";
import NavbarItem from './components/NavbarComponent';
import Jpeggler from './pages/jpeggler';
import Cozy from './pages/cozy';
import Angilo from './pages/angilo';
import Ravers from './pages/ravers';
import Rivers from './pages/rivers';
import Jagoe from './pages/jagoe';
import Home from './pages/home';

function App() {
  return (<>
      <Router>
        <Routes>
          <Route exact path="/" element={<><NavbarItem/> <Home/></>} />
          <Route path="/jpeggler" element={<><NavbarItem/> <Jpeggler/></>} />
          <Route path="/cozy" element={<><NavbarItem/> <Cozy/></>} />
          <Route path="/angilo" element={<><NavbarItem/> <Angilo/></>} />
          <Route path="/ravers" element={<><NavbarItem/> <Ravers/></>} />
          <Route path="/rivers" element={<><NavbarItem/> <Rivers/></>} />
          <Route path="/jagoe" element={<><NavbarItem/> <Jagoe/></>} />
        </Routes>
      </Router>
    </>
  );
}

export default App;

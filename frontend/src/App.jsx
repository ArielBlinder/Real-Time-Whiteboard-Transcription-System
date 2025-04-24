import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import UI from './UI/UI';
import Navbar from './layout/Navbar';
import About from './pages/About';
import Footer from "./layout/Footer";

function App() {

  return (
    <>
      <Router>
        <Navbar></Navbar>
        <div className="content-container">
        <Routes>
          <Route path="/" element={<UI />}></Route>
          <Route path="/about" element={<About />}></Route>
        </Routes>
        </div>
        <Footer></Footer>
      </Router>
    </>
  );
}

export default App


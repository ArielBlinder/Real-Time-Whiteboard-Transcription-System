import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TranscriptionSystem from './components/TranscriptionSystem';
import Navbar from './layout/Navbar';
import About from './pages/About';
import UserManual from "./pages/UserManual";
import Footer from "./layout/Footer";

function App() {

  return (
    <>
      <Router>
        <Navbar></Navbar>
        <div className="content-container">
        <Routes>
          <Route path="/" element={<TranscriptionSystem />}></Route>
          <Route path="/user-manual" element={<UserManual />}></Route>
          <Route path="/about" element={<About />}></Route>
        </Routes>
        </div>
        <Footer></Footer>
      </Router>
    </>
  );
}

export default App


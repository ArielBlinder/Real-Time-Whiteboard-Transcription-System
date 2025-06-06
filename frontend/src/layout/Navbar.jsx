import { Link } from "react-router-dom";
import PropTypes from 'prop-types';
import { FaChalkboard, FaFileImport } from "react-icons/fa"

function Navbar({ title = 'BoardCast' }) {

    const icon = "src\Files\BoardCast_icon.jpeg"

    return (
        <nav className="navbar-outer">
            <div className="navbar">
                <div className="logo-section">
                    {/* <img src="src/Files/BoardCast_icon.jpeg" style={{maxWidth:"50px"}}></img> **icon option */}
                    <FaChalkboard style={{fontSize:"2rem", paddingRight:"0.5rem", marginLeft:"5px"}}></FaChalkboard>
                    <Link to="/" className="title">
                        {title}
                    </Link>
                </div>
                <div className="links">
                    <Link to="/user-manual" className="linkBtn">
                        User Manual
                    </Link>
                    <Link to="/about" className="linkBtn">
                        About
                    </Link>
                </div>
            </div>
        </nav>
    )
}

Navbar.defaultProps = {
    title: 'BoardCast',
};

Navbar.propTypes = {
    title: PropTypes.string,
}

export default Navbar


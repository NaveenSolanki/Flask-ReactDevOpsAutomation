import '../CSS/Header.css'

const Header = () => {
    return (        
        <header className="header">
            <h1 className="title">Algo Tradify</h1>
            <nav>
                <ul className="nav-links">
                    <li><a href="/" className="nav-link">Home</a></li>
                    <li><a href="/about" className="nav-link">About</a></li>
                    <li><a href="/contact" className="nav-link">Contact</a></li>
                    <li><a href="/execution_result" className='nav-link'>Exec Result</a></li>
                    <li><a href="/upload_option_parameters" className='nav-link'>Upload Option Params</a></li>
                    <li><a href="/option_parameters" className='nav-link'>Option Params</a></li>
                </ul>
            </nav>
            <div className="login-signup">
                <a href="/login" className="login-signup-link">Login</a>
                <a href="/signup" className="login-signup-link">Sign Up</a>
            </div>
        </header>
    );
}

export default Header;

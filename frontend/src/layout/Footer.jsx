function Footer() {
    const footerYear = new Date().getFullYear();


  return (
    <footer className="footer">
        <p>Copyright &copy; {footerYear} All rights reserved</p>
    </footer>
  )
}

export default Footer

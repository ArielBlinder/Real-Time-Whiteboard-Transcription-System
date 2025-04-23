function Footer() {
    const footerYear = new Date().getFullYear()


  return (
    <footer className="footer">
      <div>
        <p>Copyright &copy; {footerYear} All rights reserved</p>
      </div>
    </footer>
  )
}

export default Footer

import react, { useState, useRef } from 'react';
import FilleInputUI from "./FilleInputUI";
import FileOutputUI from "./FileOuputUI";


function UI() {

    const [inputOption, setInputOption] = useState("image");
    const [file, setFile] = useState("");
    const [showFile, setShowFile] = useState(false);
    const [generatedText, setGeneratedText] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [showLandingPage, setShowLandingPage] = useState(true);
    const [error, setError] = useState("");


    const appContentRef = useRef(null);

    // changes file based on input type
    function handleInputOptionChange(e) {
        const comfirmChange = window.confirm("Are you sure you want to change the type of input?")
        if (comfirmChange) {
            setInputOption(e.target.value);
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
            setError(""); 
        }
    }

    const handleGenerateText = async () => {
        if (!file) return;

        setIsLoading(true);
        setError(""); 

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            
            if (!response.ok) {
                setError(data.error || "An error occurred while processing your file");
                setGeneratedText("");
                setShowFile(false);
            } else {
                setGeneratedText(data.text);
                setShowFile(true);
                setShowLandingPage(false);
                setError(""); 
            }
        } catch (error) {
            console.error("Upload error:", error);
            setError("Upload error: Unable to upload file");
            setGeneratedText("");
            setShowFile(false);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFile = (file) => {
        console.log(inputOption);
        setFile(file)
        setError(""); 
    }

    function handleClearMedia() {
        const comfirmClear = window.confirm(`Are you sure you want to clear this ${inputOption}?`)
        if (comfirmClear) {
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
            setError(""); 
        }
    }

    const handleGetStarted = () => {
        if (appContentRef.current)
            appContentRef.current.scrollIntoView({ behavior: "smooth" })
    }

    // colors
    // #DDF8F2
    // #26A688
    // #B4EEE0




    return (

        <>
            {showLandingPage && (
                <div className='landing-page'>
                    <h1>Welcome to BoardCast</h1>
                    <h3>Your tool for transcribing written text</h3>
                    <p>Upload an image or video and we'll turn it into text!</p>
                    <button onClick={handleGetStarted}>Get Started</button>
                </div>
            )}

            <div className="app-content" ref={appContentRef}>
                {error && (
                    <div className="error-message" style={{
                        backgroundColor: '#ffebee',
                        border: '1px solid #f44336',
                        borderRadius: '4px',
                        padding: '16px',
                        margin: '16px 0',
                        color: '#c62828',
                        whiteSpace: 'pre-line',
                        fontFamily: 'monospace'
                    }}>
                        <strong>Error:</strong> {error}
                    </div>
                )}
                <FilleInputUI inputOption={inputOption} showFile={showFile} handleInputOptionChange={handleInputOptionChange} handleGenerateText={handleGenerateText} onFileChange={handleFile} handleClearMedia={handleClearMedia}></FilleInputUI>
                <FileOutputUI inputOption={inputOption} file={file} showFile={showFile} generatedText={generatedText} isLoading={isLoading}></FileOutputUI>
            </div>

        </>


    );


}

export default UI
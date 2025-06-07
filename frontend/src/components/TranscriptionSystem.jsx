import react, { useState, useRef } from 'react';
import FileInputSegment from "./FileInputSegment";
import FileOuputSegment from "./FileOuputSegment";


function TranscriptionSystem() {

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

    // recives the text from th backend
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
            
            if (!response.ok) { // if couldn't get the data sends an error messege and set all to be empty
                setError(data.error || "An error occurred while processing your file");
                setGeneratedText("");
                setShowFile(false);
            } else { // if recive data then set the text to be the data
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

    // set the file to be the input file
    const handleFile = (file) => {
        console.log(inputOption);
        setFile(file)
        setError(""); 
    }

    // set the file to be empty if pressing "clear data"
    function handleClearMedia() {
        const comfirmClear = window.confirm(`Are you sure you want to clear this ${inputOption}?`)
        if (comfirmClear) {
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
            setError(""); 
        }
    }

    // move the landing page when pressing "get started"
    const handleGetStarted = () => {
        if (appContentRef.current)
            appContentRef.current.scrollIntoView({ behavior: "smooth" })
    }

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
                    <div className="error-message">
                        <strong>Error:</strong> <p>{error}</p>
                    </div>
                )}
                <FileInputSegment inputOption={inputOption} showFile={showFile} handleInputOptionChange={handleInputOptionChange} handleGenerateText={handleGenerateText} onFileChange={handleFile} handleClearMedia={handleClearMedia}></FileInputSegment>
                <FileOuputSegment inputOption={inputOption} file={file} showFile={showFile} generatedText={generatedText} isLoading={isLoading}></FileOuputSegment>
            </div>

        </>


    );


}

export default TranscriptionSystem
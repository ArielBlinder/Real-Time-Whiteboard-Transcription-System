import react, {useState, useRef} from 'react';
import FilleInputUI from "./FilleInputUI";
import FileOutputUI from "./FileOuputUI";


function UI(){

    const [inputOption, setInputOption] = useState("image");
    const [file, setFile] = useState("");
    const [showFile, setShowFile] = useState(false);
    const [generatedText, setGeneratedText] = useState(""); 
    const [isLoading, setIsLoading] = useState(false);
    const [showLandingPage, setShowLandingPage] = useState(true);


    const appContentRef = useRef(null);

    // chnages file based on input type
    function handleInputOptionChange(e) {
        const comfirmChange = window.confirm("Are you sure you want to change the type?")
        if(comfirmChange){
            setInputOption(e.target.value);
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
        }
    }

    const handleGenerateText = async () => {
        if (!file) return;

        setIsLoading(true)


        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            setGeneratedText(data.text); // Show returned text
            setShowFile(true);
            setShowLandingPage(false)
        } catch (error) {
            console.error("Upload error:", error);
        } finally {
            setIsLoading(false);
        }
        
    };

    const handleFile = (file) => {
        console.log(inputOption);
        setFile(file)
    }

    function handleClearMedia() {
        const comfirmClear = window.confirm(`Are you sure you want to clear this ${inputOption}?`)
        if(comfirmClear){
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
        }
    } 

    const handleGetStarted = () => {
        if(appContentRef.current)
            appContentRef.current.scrollIntoView({behavior: "smooth"})
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
                    <h3>your tool for transcribing texts</h3>
                    <p>Upload an image or video and we'll turn it into text!</p>
                    <button onClick={handleGetStarted}>Get started</button>
                </div>
            )}

            <div className="app-content" ref={appContentRef}>
                <FilleInputUI inputOption={inputOption} showFile={showFile} handleInputOptionChange={handleInputOptionChange} handleGenerateText={handleGenerateText} onFileChange={handleFile} handleClearMedia={handleClearMedia}></FilleInputUI>
                <FileOutputUI inputOption={inputOption} file={file} showFile={showFile} generatedText={generatedText} isLoading={isLoading}></FileOutputUI>
            </div>

        </>


    );


}

export default UI
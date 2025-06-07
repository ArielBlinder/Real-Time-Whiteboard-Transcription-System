import react, {useEffect, useState, useRef} from 'react';
import { FaUpload } from "react-icons/fa"

function FileInputSegment({ inputOption, showFile, handleInputOptionChange, handleGenerateText, onFileChange, handleClearMedia}) {

    const [inputFile, setInputFile] = useState(null);
    const fileInputRef = useRef(null);

    
    // remove the current file when changing file option
    useEffect(() => {
        setInputFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    }, [inputOption]);

    // when reciving a file sets the input file as this file
    function handleFileChange(e){
        console.log("file uploaded")
        const selectedFile = e.target.files[0];
        if(selectedFile){
            setInputFile(selectedFile)
            onFileChange(selectedFile)  
        }
    }

    // set the type of input when pressing the types buttons
    function triggerFileInput() {
        fileInputRef.current.click();
    }

    // remove the current file when pressing "clear media"
    function clearInputFile() {
        setInputFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    }

   

    return(
        <div>
            <br></br><h2>Enter a file you want to see in text</h2>
            <div className='file-container'>
                <div className='input-container' onClick={triggerFileInput}>
                    {inputFile ? <span>Selected file: {inputFile.name}</span> : <><FaUpload style={{margin: "15px", width: "20px", height: "20px"}}></FaUpload> <span>insert {inputOption} to transcribe to text</span></>}
                    <input type='file' ref={fileInputRef}  style={{ display: 'none' }} accept={inputOption === "image" ? "image/*" : "video/*"} onChange={handleFileChange}/>
                </div>
                <label id="pictureOptn">
                <input type="radio" value="image" checked={inputOption === "image"} onChange={handleInputOptionChange}></input>
                    Image
                </label>
                <label id="videoOptn">
                <input type="radio" value="video" checked={inputOption === "video"} onChange={handleInputOptionChange}></input>
                    Video
                </label><br></br>
                <div id="GenerateText">
                    {showFile ?
                        <button className='generated-text-button' type='button' onClick={() => {handleClearMedia(); clearInputFile();}}>Clear Media</button>
                        :
                        <button className='generated-text-button' type='button' onClick={handleGenerateText}>Generate Text</button>}
                </div>
            </div><br></br><br></br>
        </div>
    );
}

export default FileInputSegment
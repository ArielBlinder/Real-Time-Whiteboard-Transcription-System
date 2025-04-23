import react, {useEffect, useState, useRef} from 'react';
import { FaUpload } from "react-icons/fa"

function FilleInputUI({ inputOption, file, handleInputOptionChange, handleGenerateText, onFileChange}) {

    const [inputFile, setInputFile] = useState(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        setInputFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    }, [inputOption]);

    function handleFileChange(e){
        console.log("file uploaded")
        const selectedFile = e.target.files[0];
        if(selectedFile){
            setInputFile(selectedFile)
            onFileChange(selectedFile)  
        }
    }

    function triggerFileInput() {
        fileInputRef.current.click();
    }

   



    return(
        <div>
            <h2>Enter a file you want to see in text</h2>
            <div className='file-container'>
                <div className='input-container' onClick={triggerFileInput}>
                    {inputFile ? <span>Selected file: {inputFile.name}</span> : <><FaUpload style={{margin: "15px", width: "20px", height: "20px"}}></FaUpload> <text>insert {inputOption} to transcribe to text</text></>}
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
                <button className='generated-text-button' type='submit' onClick={handleGenerateText}>Generate Text</button>
                </div>
            </div><br></br><br></br>
        </div>
    );
}

export default FilleInputUI
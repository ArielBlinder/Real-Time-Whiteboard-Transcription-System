import react, {useState, useEffect} from 'react';
import FilleInputUI from "./FilleInputUI";
import FileOutputUI from "./FileOuputUI";


function UI(){

    const [inputOption, setInputOption] = useState("image");
    const [file, setFile] = useState("");
    const [showFile, setShowFile] = useState(false);
    const [generatedText, setGeneratedText] = useState(""); 




    // chnages file based on input type
    function handleInputOptionChange(e) {
        const comfirmChange = window.confirm("are you sure you want to change type?")
        if(comfirmChange){
            setInputOption(e.target.value);
            setFile(null);
            setShowFile(false);
            setGeneratedText("");
        }
    }

    const handleGenerateText = async () => {
        if (!file) return;


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
        } catch (error) {
            console.error("Upload error:", error);
        }
    };

    const handleFile = (file) => {
        console.log(inputOption);
        setFile(file)
    }

    // colors
    // #DDF8F2
    // #26A688
    // #B4EEE0




    return (

        <>

                <FilleInputUI inputOption={inputOption} handleInputOptionChange={handleInputOptionChange} handleGenerateText={handleGenerateText} onFileChange={handleFile}></FilleInputUI>
                <FileOutputUI inputOption={inputOption} file={file} showFile={showFile} text={generatedText}></FileOutputUI>
        </>


    );


}

export default UI
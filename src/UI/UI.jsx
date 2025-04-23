npmimport react, {useState} from 'react';
import FilleInputUI from "./FilleInputUI";
import FileOutputUI from "./FileOuputUI";


function UI(){

    const [inputOption, setInputOption] = useState("image");
    const [file, setFile] = useState("");
    const [showFile, setShowFile] = useState(false);



    function handleInputOptionChange(e) {
        const comfirmChange = window.confirm("are you sure you want to change type?")
        if(comfirmChange){
            setInputOption(e.target.value);
            setFile(null);
            setShowFile(false);
        }
    }

    const handleGenerateText = () => {
        setShowFile(true);
    };

    const handleFile = (file) => {
        console.log(inputOption);

        const reader = new FileReader();
        reader.onload = () => {
            setFile(reader.result);
        };
        reader.readAsDataURL(file);
    }

    // colors
    // #DDF8F2
    // #26A688
    // #B4EEE0




    return (

        <>

                <FilleInputUI inputOption={inputOption} file={file} handleInputOptionChange={handleInputOptionChange} handleGenerateText={handleGenerateText} onFileChange={handleFile}></FilleInputUI>
                <FileOutputUI inputOption={inputOption} file={file} showFile={showFile}></FileOutputUI>
        </>


    );


}

export default UI